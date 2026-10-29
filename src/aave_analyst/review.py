"""Prepare independent human review packets and import their explicit decisions."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import unicodedata

from .benchmark import load_benchmark, save_benchmark


def content_hash(row):
    content = {key: value for key, value in row.items() if key != 'review'}
    return hashlib.sha256(json.dumps(content, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def export_reviews(source, destination):
    source, destination = Path(source), Path(destination)
    rows = load_benchmark(source)
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    outputs = [destination / f'reviewer-{i}.{suffix}' for i in (1, 2) for suffix in ('json', 'md')]
    if any(path.exists() for path in outputs):
        raise FileExistsError('Review packets already exist; use a new directory to preserve decisions')
    destination.mkdir(parents=True, exist_ok=True)
    items = [{'id': row['id'], 'content_sha256': content_hash(row), 'verdict': None,
              'verified_answer': None, 'verified_sources': None, 'verified_scope': None, 'notes': ''} for row in rows]
    booklet = ['# Independent human review', '',
               'Do not read the other reviewer’s decisions. Verify the question, answer/SQL, source support, UTC scope and units independently.',
               'The references below are MACHINE-GENERATED DRAFTS, not approved gold. If anything is wrong, use changes_requested and explain it; do not approve until corrected and reviewed again.',
               'Fill your name and decisions in the companion JSON. This tool does not prove human identity and never supplies human labels.', '']
    for row in rows:
        booklet += [f"## {row['id']} · {row['split']} · {row.get('category', row.get('error_type', 'stress'))}", '',
                    row['question'], '', f"Family: `{row['family']}`", '',
                    '```json', json.dumps({key: value for key, value in row.items() if key not in {'review', 'question'}}, ensure_ascii=False, indent=2), '```', '']
    for reviewer in (1, 2):
        packet = {'schema_version': 1, 'source_sha256': sha, 'reviewer_name': '', 'items': items}
        (destination / f'reviewer-{reviewer}.json').write_text(json.dumps(packet, ensure_ascii=False, indent=2), encoding='utf-8')
        (destination / f'reviewer-{reviewer}.md').write_text('\n'.join(booklet), encoding='utf-8')
    return {'source_sha256': sha, 'records': len(rows), 'outputs': [str(path) for path in outputs]}


def import_reviews(source, first, second):
    source = Path(source)
    if source.with_suffix('.lock.json').exists():
        raise ValueError('Frozen gold cannot be changed by review import')
    rows = load_benchmark(source)
    sha = hashlib.sha256(source.read_bytes()).hexdigest()
    packets = [json.loads(Path(path).read_text(encoding='utf-8-sig')) for path in (first, second)]
    names = [packet.get('reviewer_name', '').strip() for packet in packets]
    canonical = [unicodedata.normalize('NFC', ' '.join(name.casefold().split())) for name in names]
    if not all(canonical) or canonical[0] == canonical[1]:
        raise ValueError('Two distinct named human reviewers must complete the packets')
    expected_ids = {row['id'] for row in rows}
    indexes = []
    for packet in packets:
        if packet.get('source_sha256') != sha:
            raise ValueError('Benchmark changed since review export; regenerate and re-review')
        items = packet.get('items', [])
        index = {item['id']: item for item in items}
        if len(index) != len(items) or set(index) != expected_ids:
            raise ValueError('Review IDs must match the complete source without duplicates')
        for row in rows:
            item = index[row['id']]
            if item.get('content_sha256') != content_hash(row):
                raise ValueError('Reviewed question content changed')
            if item.get('verdict') not in {None, 'approved', 'changes_requested'}:
                raise ValueError('Unknown review verdict')
        indexes.append(index)
    approved = 0
    for row in rows:
        decisions = [index[row['id']] for index in indexes]
        accepted = all(item.get('verdict') == 'approved' and all(item.get(key) is True for key in
                       ('verified_answer', 'verified_sources', 'verified_scope')) for item in decisions)
        row['review'] = {'reviewer_1': names[0], 'reviewer_2': names[1], 'approved': accepted,
                         'reviewed_at': datetime.now(timezone.utc).isoformat(),
                         'notes': json.dumps({names[i]: {'verdict': item.get('verdict'), 'notes': item.get('notes', '')}
                                              for i, item in enumerate(decisions)}, ensure_ascii=False)}
        approved += accepted
    save_benchmark(rows, source)
    return {'records': len(rows), 'approved': approved, 'pending_or_disputed': len(rows) - approved}
