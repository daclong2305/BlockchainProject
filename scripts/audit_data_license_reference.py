"""Compare pinned processed observations against a licensed Zenodo version.

Reference artifacts stay in .tools; the pinned runtime snapshot is never replaced.
"""
from pathlib import Path
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import zipfile
import time
import requests
import pandas as pd
import duckdb

from aave_analyst.data import prepare_data, ASSETS
from aave_analyst.comparison import input_hashes

ROOT = Path(__file__).resolve().parents[1]
RECORD = 22994363


def digest(path, algorithm='sha256'):
    h = hashlib.new(algorithm)
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def compare_frames(pinned, reference, keys):
    pinned = pinned.set_index(keys).sort_index()
    reference = reference.set_index(keys).sort_index()
    if pinned.index.has_duplicates or reference.index.has_duplicates:
        raise ValueError('Duplicate keys prevent an identity comparison')
    missing = pinned.index.difference(reference.index)
    aligned = reference.reindex(pinned.index)[pinned.columns]
    counts = {}
    for column in pinned.columns:
        equal = pinned[column].eq(aligned[column]) | (pinned[column].isna() & aligned[column].isna())
        counts[column] = int((~equal.fillna(False)).sum())
    return {'pinned_rows': len(pinned), 'reference_rows': len(reference), 'missing_pinned_keys': len(missing),
            'unequal_cells_by_column': counts,
            'all_pinned_observations_match': len(missing) == 0 and not any(counts.values())}


def compare(pinned_path, reference_path, keys):
    return compare_frames(pd.read_parquet(pinned_path), pd.read_parquet(reference_path), keys)


def main():
    before = input_hashes(ROOT)
    folder = ROOT / '.tools/data-license-reference' / str(RECORD)
    folder.mkdir(parents=True, exist_ok=True)
    url = f'https://zenodo.org/api/records/{RECORD}'
    response = requests.get(url, timeout=(15, 60))
    response.raise_for_status()
    record = response.json()
    file = next(item for item in record['files'] if item['key'] == 'aave_data.zip')
    archive = folder / 'aave_data.zip'
    if not archive.exists():
        part = archive.with_suffix('.part')
        pieces = folder / 'download-parts'
        pieces.mkdir(exist_ok=True)
        block_size = 1024 * 1024
        # Reuse only complete, sequential blocks from an interrupted full stream.
        if part.exists():
            with part.open('rb') as stream:
                for index in range(part.stat().st_size // block_size):
                    block = stream.read(block_size)
                    target = pieces / str(index)
                    if not target.exists():
                        target.write_bytes(block)

        def fetch(index):
            start = index * block_size
            end = min(start + block_size, file['size']) - 1
            target = pieces / str(index)
            if target.exists() and target.stat().st_size == end - start + 1:
                return
            for attempt in range(3):
                try:
                    with requests.get(file['links']['self'], headers={'Range': f'bytes={start}-{end}'},
                                      timeout=(30, 120)) as download:
                        download.raise_for_status()
                        if download.status_code != 206 or download.headers.get('Content-Range') != f'bytes {start}-{end}/{file["size"]}':
                            raise ValueError('Unexpected Zenodo range response')
                        if len(download.content) != end - start + 1:
                            raise ValueError('Incomplete Zenodo range')
                        target.write_bytes(download.content)
                    return
                except requests.RequestException:
                    if attempt == 2:
                        raise
                    time.sleep(2 * (attempt + 1))

        count = (file['size'] + block_size - 1) // block_size
        with ThreadPoolExecutor(max_workers=8) as pool:
            futures = [pool.submit(fetch, index) for index in range(count)]
            for done, future in enumerate(as_completed(futures), 1):
                future.result()
                print(f'Reference archive blocks: {done}/{count}', flush=True)
        with part.open('wb') as stream:
            for index in range(count):
                stream.write((pieces / str(index)).read_bytes())
        part.replace(archive)
    if archive.stat().st_size != file['size'] or 'md5:' + digest(archive, 'md5') != file['checksum']:
        raise ValueError('Zenodo archive differs from its published size/checksum')
    names = [f'data/AAVE/aave_v3_{asset.lower()}_eth.parquet' for asset in ASSETS]
    names.append('data/AAVE/liquidations/aave_v3_eth_liquidation_events.parquet')
    extracted = folder / 'extracted'
    with zipfile.ZipFile(archive) as zipped:
        for name in names:
            if not (extracted / name).resolve().is_relative_to(extracted.resolve()):
                raise ValueError('Unsafe archive path')
            zipped.extract(name, extracted)
    prepare_data(folder, source=extracted / 'data/AAVE')
    with duckdb.connect(str(ROOT / 'data/processed/aave.duckdb'), read_only=True) as connection:
        connection.execute("SET TimeZone='UTC'")
        market_db = connection.execute('SELECT * FROM market_hourly').df()
        events_db = connection.execute('SELECT * FROM liquidation_events').df()
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'zenodo_record': RECORD, 'record_url': url,
              'publication_date': record['metadata'].get('publication_date'),
              'license_as_declared': record['metadata'].get('license'),
              'reference_archive': {'sha256': digest(archive), 'published_md5': file['checksum'], 'bytes': archive.stat().st_size},
              'pinned_archive_sha256': digest(ROOT / 'data/raw/aave_data.zip'),
              'market': compare(ROOT / 'data/processed/market_hourly.parquet', folder / 'data/processed/market_hourly.parquet', ['asset', 'hour']),
              'events': compare(ROOT / 'data/processed/liquidation_events.parquet', folder / 'data/processed/liquidation_events.parquet', ['event_id']),
              'runtime_db_vs_parquet': {
                  'market': compare_frames(market_db, pd.read_parquet(ROOT / 'data/processed/market_hourly.parquet'), ['asset', 'hour']),
                  'events': compare_frames(events_db, pd.read_parquet(ROOT / 'data/processed/liquidation_events.parquet'), ['event_id']),
              },
              'runtime_input_hashes': before,
              'compared_parquet_sha256': {name: digest(ROOT / 'data/processed' / name)
                                         for name in ('market_hourly.parquet', 'liquidation_events.parquet')},
              'runtime_inputs_unchanged': before == input_hashes(ROOT),
              'scope': 'Exact value comparison of processed runtime observations only. Does not claim byte-identical ZIPs, upstream raw fields not used by runtime, model training provenance or third-party rights.'}
    output = ROOT / 'docs/phase12-evidence/data-license-content-audit.json'
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
