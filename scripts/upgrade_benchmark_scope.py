"""One-time pre-review scope migration; preserves old gold and selected trace IDs."""
from pathlib import Path
import hashlib
import json
import shutil

from aave_analyst.benchmark import load_benchmark, save_benchmark, question_scope
from aave_analyst.review import content_hash, export_reviews


def main():
    root=Path(__file__).resolve().parents[1]
    source=root/'data/benchmark/questions.jsonl'
    registration=source.with_name('trace_registration.json')
    backup=source.with_name('questions.scope-v1.jsonl')
    registration_backup=registration.with_name('trace_registration.scope-v1.json')
    destination=source.parent/'review/questions-v2'
    rows=load_benchmark(source)
    if source.with_suffix('.lock.json').exists() or backup.exists() or registration_backup.exists() or destination.exists():
        raise ValueError('Migration requires unfrozen input and fresh backup/review paths')
    if any(r.get('review',{}).get(key) for r in rows for key in ('reviewer_1','reviewer_2','approved')):
        raise ValueError('Preserve human decisions; migration cannot silently replace reviewed gold')
    trace=json.loads(registration.read_text(encoding='utf-8'))
    if trace.get('content_hashes')!={r['id']:content_hash(r) for r in rows}:
        raise ValueError('Unexpected registration mismatch')
    for row in rows:
        unit=row['expected_numeric'][0]['unit'] if row['expected_numeric'] else 'other'
        row['scope']=question_scope(row['question'],row['sql'],row['family'],unit)
    shutil.copy2(source,backup)
    shutil.copy2(registration,registration_backup)
    save_benchmark(rows,source)
    trace['content_hashes']={r['id']:content_hash(r) for r in rows}
    trace['benchmark_sha256']=hashlib.sha256(source.read_bytes()).hexdigest()
    trace['scope_migration']='Question IDs and selection unchanged; metadata clarified before review/final inference; prior registration preserved in trace_registration.scope-v1.json'
    registration.write_text(json.dumps(trace,ensure_ascii=False,indent=2),encoding='utf-8')
    export_reviews(source,destination)
    print('Updated 60 provisional scopes; preserved v1, trace IDs and all empty decisions; exported questions-v2')


if __name__=='__main__':main()
