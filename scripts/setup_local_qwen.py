"""Download the user-selected, pinned GGUF and a pinned llama.cpp runtime."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib
import json
import time
import zipfile
import requests

ROOT = Path(__file__).resolve().parents[1]
REVISION = '579ae3d2f0db23dd25fd83076a57dbab79f68dd9'
MODEL_HASH = 'b34a028bc6c18d738b57552423bb75ca555d823c19722c4261acc792547a4cd2'
MODEL_SIZE = 1929902496
BUILD = 'b11962'


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def main():
    folder = ROOT / 'models/qwen-vitext2sql-3b'
    folder.mkdir(parents=True, exist_ok=True)
    model = folder / 'model-q4_k_m.gguf'
    url = f'https://huggingface.co/zhenlong54/qwen-vitext2sql-3b-GGUF/resolve/{REVISION}/model-q4_k_m.gguf'
    if not model.exists():
        part = model.with_suffix('.part')
        if not part.exists() or part.stat().st_size != MODEL_SIZE:
            with part.open('wb') as stream:
                stream.truncate(MODEL_SIZE)
        block = 16 * 1024 * 1024
        # Range writes are sequential within each block. A nonzero tail can be
        # reused provisionally after interruption; the WHOLE file hash remains
        # the final authority before promotion from .part to .gguf.
        pending = []
        total = 0
        with part.open('rb') as stream:
            for start in range(0, MODEL_SIZE, block):
                end = min(start + block, MODEL_SIZE)
                stream.seek(end - 32)
                if any(stream.read(32)):
                    total += end - start
                else:
                    pending.append(start)
        print(f'Reusing provisional ranges: {total / MODEL_SIZE:.0%}; final hash required', flush=True)

        def download(start):
            end = min(start + block, MODEL_SIZE) - 1
            for attempt in range(3):
                try:
                    with requests.get(url + f'?download=true&offset={start}', headers={'Range': f'bytes={start}-{end}'}, timeout=(20, 120), stream=True) as response:
                        response.raise_for_status()
                        if response.status_code != 206 or response.headers.get('Content-Range') != f'bytes {start}-{end}/{MODEL_SIZE}':
                            raise ValueError('Unexpected range response')
                        written = 0
                        with part.open('r+b') as stream:
                            stream.seek(start)
                            for chunk in response.iter_content(1024 * 1024):
                                written += len(chunk)
                                if written > end - start + 1:
                                    raise ValueError('Range exceeded requested length')
                                stream.write(chunk)
                        if written != end - start + 1:
                            raise ValueError('Incomplete range')
                    return written
                except (requests.RequestException, ValueError):
                    if attempt == 2:
                        raise
                    time.sleep(2)

        with ThreadPoolExecutor(max_workers=12) as pool:
            futures = [pool.submit(download, start) for start in pending]
            try:
                for future in as_completed(futures):
                    total += future.result()
                    print(f'Model: {total / MODEL_SIZE:.0%}', flush=True)
            except Exception:
                for future in futures:
                    future.cancel()
                raise
        if sha256(part) != MODEL_HASH:
            part.unlink()
            raise ValueError('Model SHA-256 mismatch; discarded unverified partial file. Run setup again to redownload.')
        part.replace(model)
    if sha256(model) != MODEL_HASH:
        raise ValueError('Existing model SHA-256 mismatch')

    runtime = ROOT / '.tools' / f'llama-{BUILD}'
    runtime.mkdir(parents=True, exist_ok=True)
    asset_name = f'llama-{BUILD}-bin-win-vulkan-x64.zip'
    release = requests.get(f'https://api.github.com/repos/ggml-org/llama.cpp/releases/tags/{BUILD}', timeout=30)
    release.raise_for_status()
    asset = next(a for a in release.json()['assets'] if a['name'] == asset_name)
    archive = runtime / asset_name
    if not archive.exists():
        with requests.get(asset['browser_download_url'], timeout=(20, 120), stream=True) as response:
            response.raise_for_status()
            with archive.open('wb') as stream:
                for chunk in response.iter_content(1024 * 1024):
                    stream.write(chunk)
    runtime_hash = sha256(archive)
    if asset.get('digest') != 'sha256:' + runtime_hash:
        raise ValueError('Runtime archive SHA-256 mismatch or missing upstream digest')
    with zipfile.ZipFile(archive) as zipped:
        for item in zipped.infolist():
            if not (runtime / item.filename).resolve().is_relative_to(runtime.resolve()):
                raise ValueError('Unsafe archive member')
        zipped.extractall(runtime)
    manifest = {'model_repo': 'zhenlong54/qwen-vitext2sql-3b-GGUF', 'revision': REVISION, 'model_sha256': MODEL_HASH, 'model_bytes': model.stat().st_size, 'runtime_build': BUILD, 'runtime_url': asset['browser_download_url'], 'runtime_sha256': runtime_hash, 'finetune_status': 'User states this model was fine-tuned by another developer; training provenance not independently verified'}
    (folder / 'manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2), flush=True)


if __name__ == '__main__':
    main()
