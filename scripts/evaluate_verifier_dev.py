"""Score immutable dev outputs, then replay controlled detection cases."""
import sys,json,argparse
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from aave_analyst.cli import analyst_at,write_json,code_hashes
from aave_analyst.benchmark import load_benchmark
from aave_analyst.experiments import score_results,summarize,human_audit_sample
from aave_analyst.models import Draft,QuerySpec
from aave_analyst.verifier_replay import verify_candidate,detection_metrics,VARIANTS
from aave_analyst.research_runtime import MeteredLLM
from aave_analyst.scoring import checkpointed_scores
from run_verifier_dev import restore

root=Path(__file__).resolve().parents[1]
def read(path):return [json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip()]
def candidate_error_label(score):
    # Includes numerical value/scope and evidence-contract failures, not just judge prose.
    return None if score.get('correct') is None else not score['correct']

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True)
    parser.add_argument('--expected',type=int,default=120)
    parser.add_argument('--score-only',action='store_true')
    args=parser.parse_args();out=args.out
    if not (out/'results.jsonl').exists() or len(read(out/'results.jsonl'))!=args.expected:
        raise ValueError('Runtime results incomplete; finish runtime before evaluation')
    a=analyst_at(root,provider='bedrock');a.llm=MeteredLLM(a.llm,out/'evaluation_api_calls.jsonl',pace=12.,cap=4.)
    records=read(out/'benchmark_snapshot.jsonl');results=read(out/'results.jsonl')
    journal=out/'scoring_journal_v2.jsonl'
    scores,usage=checkpointed_scores(records,results,a.llm,journal,{'code':code_hashes(),'judge':a.llm.config()},resume=journal.exists())
    write_json(out/'scores.json',scores);write_json(out/'summary.json',summarize(scores));write_json(out/'human_audit.json',human_audit_sample(scores))
    print('SCORED',len(scores),flush=True)
    if args.score_only:return
    cases=[];byid={r['question_id']:r for r in scores if r['mode']=='B0'}
    for r in read(out/'candidates.jsonl'):
        score=byid[r['question_id']]
        # The label is independently evaluated, never inferred from checker status.
        bad=candidate_error_label(score) if not r['draft'].get('error') else None
        cases.append({'id':r['question_id'],'group':'natural','draft':r['draft'],'has_error':bad,'target_error':None})
    stress=[r for r in load_benchmark(root/'data/benchmark/stress.jsonl') if r['split']=='dev']
    for row in stress:
        # Independently specified requirement; never send gold SQL or row labels to runtime.
        spec=QuerySpec(kind='data',metric='borrowed_usd',assets=['USDC' if 'USDC' in row['question'] else 'WETH'],start='2026-08-01T00:00:00Z',end='2026-09-01T00:00:00Z',unit='USD',aggregation='average')
        if row['error_type']=='join':spec.end=None;spec.aggregation='snapshot'
        for label in ('correct','wrong'):
            sql=row[label+'_sql'];result=a.db.query(sql)
            value=result.rows[0]['value'];answer=f'{value:.2f} USD [SQL1]'
            claim={'text':answer,'citations':['SQL1'],'numeric':{'value':value,'unit':'USD','evidence_id':'SQL1','row':0,'column':'value'}}
            d=Draft(question=row['question'],spec=spec,sql=sql,query_result=result,answer=answer,claims=[claim])
            cases.append({'id':row['id']+'-'+label,'group':'sql_stress','draft':asdict(d),'has_error':label=='wrong','target_error':row['error_type'] if label=='wrong' else None})
    chunks=json.loads((root/'data/documents/chunks.json').read_text(encoding='utf-8'));liq=next(d for d in chunks if d['id']=='DOC_LIQ_000')
    for kind in ('missing_citation','irrelevant_source','contradiction','scope','causation'):
        for n in range(2):
            text=('Health factor dưới 1 báo hiệu rủi ro thanh lý.' if n==0 else 'Có thể tăng health factor bằng bổ sung tài sản thế chấp hoặc trả bớt nợ.')
            question=('Health factor dưới 1 có ý nghĩa gì?' if n==0 else 'Có thể cải thiện health factor như thế nào?')
            for label in ('correct','wrong'):
                docs=[liq];cites=[liq['id']];answer=text
                if label=='wrong':
                    if kind=='missing_citation':cites=[]
                    elif kind=='irrelevant_source':docs=[next(d for d in chunks if d['id']=='DOC_SUPPLY_001')];cites=[docs[0]['id']]
                    elif kind=='contradiction':answer='Health factor dưới 1 bảo đảm vị thế không bị thanh lý.'
                    elif kind=='scope':answer='Mọi ví USDC trong tháng 8/2026 đều có health factor dưới 1.'
                    else:answer='Health factor giảm là nguyên nhân duy nhất khiến giá ETH giảm trong tháng 8/2026.'
                d=Draft(question=question,spec=QuerySpec(kind='docs'),answer=answer+(' ['+cites[0]+']' if cites else ''),claims=[{'text':answer,'citations':cites}],documents=docs)
                cases.append({'id':f'E-{kind}-{n}-{label}','group':'evidence_stress','draft':asdict(d),'has_error':label=='wrong','target_error':None})
    fixture=out/'replay_candidates.jsonl'
    import hashlib
    replay_manifest={'code_hashes':code_hashes(),'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                     'model':a.llm.config(),'pace_seconds':12.,'deadline_seconds':120,'variants':list(VARIANTS),
                     'source_hashes':{str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'data/processed/aave.duckdb',root/'data/documents/chunks.json',root/'data/benchmark/stress.jsonl']},
                     'candidate_hash':hashlib.sha256(json.dumps(cases,sort_keys=True,ensure_ascii=False,default=str).encode()).hexdigest()}
    manifest_path=out/'replay_manifest.json'
    if manifest_path.exists() and json.loads(manifest_path.read_text(encoding='utf-8'))!=replay_manifest:raise ValueError('Replay protocol changed; use a new run')
    if not manifest_path.exists():write_json(manifest_path,replay_manifest)
    if not fixture.exists():fixture.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in cases),encoding='utf-8')
    elif read(fixture)!=cases:raise ValueError('Replay inputs changed')
    target=out/'replay_results.jsonl';done={(r['case_id'],r['variant']) for r in read(target)} if target.exists() else set()
    for c in cases:
        for variant in VARIANTS:
            if (c['id'],variant) in done:continue
            verdict=verify_candidate(restore(c['draft']),a,variant)
            row=dict(verdict,case_id=c['id'],group=c['group'],has_error=c['has_error'],target_error=c['target_error'],candidate_generation_failed=bool(c['draft'].get('error')))
            with target.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
            print('REPLAY',c['id'],variant,row['verdict'],row['execution_status'],flush=True)
    rows=read(target)
    detection={group:{v:detection_metrics([r for r in rows if r['variant']==v and r['group']==group]) for v in VARIANTS} for group in ('natural','sql_stress','evidence_stress')}
    for group,variants in detection.items():
        for v,metrics in variants.items():metrics['candidate_generation_failures']=sum(bool(r.get('candidate_generation_failed')) for r in rows if r['variant']==v and r['group']==group)
    write_json(out/'detection_summary.json',detection)
    write_json(out/'completed.json',{'results':len(results),'scores':len(scores),'replay_verdicts':len(rows),'reference_status':'provisional; human audit pending'})

if __name__=='__main__':main()
