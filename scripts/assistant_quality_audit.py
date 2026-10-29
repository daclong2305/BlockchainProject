"""Recompute provisional numeric gold and create supplemental dev-only SQL cases.

This is automated technical evidence, never independent human approval.
Only existing dev average-debt families are expanded; no test model inference.
"""
from pathlib import Path
import hashlib
import json
import pandas as pd
from aave_analyst.benchmark import load_benchmark,save_benchmark
from aave_analyst.database import Database
from aave_analyst.evaluation import benchmark_numeric_equal


def main():
    root=Path(__file__).resolve().parents[1]
    destination=root/'runs/assistant-quality-audit-v1'
    destination.mkdir(exist_ok=False)
    db=Database(root/'data/processed/aave.duckdb')
    market=pd.read_parquet(root/'data/processed/market_hourly.parquet')
    market['hour']=pd.to_datetime(market['hour'],utc=True)
    checks=[]
    for row in load_benchmark(root/'data/benchmark/questions.jsonl'):
        if not row.get('sql'):
            checks.append({'id':row['id'],'status':'requires_document_semantic_review','human_approved':False})
            continue
        actual=db.query(row['sql']).rows
        reference=next(source['rows'] for source in row['sources'] if source['id']=='SQL1')
        checks.append({'id':row['id'],'status':'recomputed_exact_match' if actual==reference else 'mismatch',
                       'actual':actual,'reference':reference,'human_approved':False,
                       'limitation':'Reexecuting the same SQL checks reproducibility, not semantic correctness'})
    stress_checks=[]
    for row in load_benchmark(root/'data/benchmark/stress.jsonl'):
        good=db.query(row['correct_sql']).rows;bad=db.query(row['wrong_sql']).rows
        stress_checks.append({'id':row['id'],'reference_matches':good==row['reference_rows'],
                              'mutation_changes_result':good!=bad,'correct_rows':good,'wrong_rows':bad,
                              'human_approved':False})
    extra=[]
    for asset in ('DAI','USDC','USDT','USDe','WETH'):
        for month in (6,7,8):
            start=f'2026-{month:02d}-01';end=f'2026-{month+1:02d}-01'
            subset=market[(market['asset']==asset)&(market['hour']>=pd.Timestamp(start,tz='UTC'))&(market['hour']<pd.Timestamp(end,tz='UTC'))]
            expected=float(subset['borrowed_usd'].mean())
            where=f"asset='{asset}' AND hour>=TIMESTAMPTZ '{start}' AND hour<TIMESTAMPTZ '{end}'"
            correct=f'SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE {where}'
            reference=db.query(correct).rows
            independent_ok=benchmark_numeric_equal(reference[0]['value'],expected,relative_tolerance='0.000000001')
            other='USDC' if asset!='USDC' else 'DAI'
            mutations={'metric':correct.replace('borrowed_usd','supplied_usd'),
                       'aggregation':correct.replace('avg(','sum('),
                       'asset':correct.replace(f"asset='{asset}'",f"asset='{other}'"),
                       'unit':correct.replace('avg(borrowed_usd)','avg(borrowed_usd)/1000000'),
                       'time':correct.replace(f"'{end}'",f"'2026-{month:02d}-15'")}
            for kind,wrong in mutations.items():
                wrong_rows=db.query(wrong).rows
                extra.append({'id':f'X{len(extra)+1:03d}','split':'supplemental_dev','family':'avg_debt',
                              'asset':asset,'start':start,'end_exclusive':end,'unit':'USD','error_type':kind,
                              'question':f'Dư nợ {asset} trung bình theo giờ tháng {month}/2026 là bao nhiêu USD?',
                              'correct_sql':correct,'wrong_sql':wrong,'reference_rows':reference,
                              'pandas_reference':expected,'pandas_observations':len(subset),
                              'independent_engine_agreement':independent_ok,'mutation_changes_result':wrong_rows!=reference,
                              'wrong_rows':wrong_rows,'human_approved':False})
    save_benchmark(extra,destination/'supplemental_dev.jsonl')
    report={'kind':'assistant technical audit; not two-human review','benchmark_checks':checks,'stress_checks':stress_checks,
            'supplemental_cases':len(extra),'supplemental_independent_engine_agreement':sum(r['independent_engine_agreement'] for r in extra),
            'supplemental_mutations_change_result':sum(r['mutation_changes_result'] for r in extra),
            'source_hashes':{str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest() for path in
                             [root/'data/benchmark/questions.jsonl',root/'data/benchmark/stress.jsonl',root/'data/processed/market_hourly.parquet']},
            'limitations':['No model inference or quality score produced','Document semantics not verified by numeric recomputation',
                           'Supplemental dev uses existing avg_debt development family; excluded from primary 60 and 720 outputs',
                           'No human approvals modified; expanded quantity does not guarantee quality']}
    (destination/'audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps({'benchmark_sql_recomputed':sum(r['status']=='recomputed_exact_match' for r in checks),
                      'benchmark_mismatches':sum(r['status']=='mismatch' for r in checks),
                      'stress_reference_matches':sum(r['reference_matches'] for r in stress_checks),
                      'stress_changed_results':sum(r['mutation_changes_result'] for r in stress_checks),
                      'supplemental_cases':len(extra),'pandas_agreement':report['supplemental_independent_engine_agreement'],
                      'supplemental_changed_results':report['supplemental_mutations_change_result']},indent=2))


if __name__=='__main__':main()
