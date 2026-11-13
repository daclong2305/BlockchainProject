"""Immutable, resumable DEV runs. Never reads test answers into runtime prompts."""
import argparse, json, sys, time, hashlib
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from aave_analyst.cli import analyst_at, code_hashes
from aave_analyst.benchmark import load_benchmark
from aave_analyst.models import Draft, QuerySpec, QueryResult, Issue

def restore(value):
    value=dict(value);value['spec']=QuerySpec(**value['spec'])
    if value.get('query_result'):value['query_result']=QueryResult(**value['query_result'])
    value['issues']=[Issue(**i) for i in value.get('issues',[])]
    return Draft(**value)

def main():
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--candidates',type=Path)
    p.add_argument('--modes',nargs='+',default=['B0','B1','P']);p.add_argument('--limit',type=int,default=20)
    p.add_argument('--pace',type=float,default=6.)
    p.add_argument('--rotate-modes',action='store_true')
    p.add_argument('--cooldown',type=float,default=0.)
    args=p.parse_args();root=Path(__file__).resolve().parents[1];out=args.out;out.mkdir(parents=True,exist_ok=True)
    a=analyst_at(root,provider='bedrock');records=[r for r in load_benchmark(root/'data/benchmark/questions.jsonl') if r['split']=='dev'][:args.limit]
    from aave_analyst.research_runtime import MeteredLLM
    a.llm=MeteredLLM(a.llm,out/'api_calls.jsonl',pace=args.pace)
    manifest=out/'config.json';config={'llm':a.llm.config(),'code_hashes':code_hashes(),'split':'dev','final':False,'deadline_seconds':120,'modes':args.modes,'pace_seconds':args.pace,'reference_status':'provisional; no human approval','benchmark_sha256':hashlib.sha256((root/'data/benchmark/questions.jsonl').read_bytes()).hexdigest()}
    config.update(selected_ids=[r['id'] for r in records],limit=args.limit,candidate_source_sha256=hashlib.sha256(args.candidates.read_bytes()).hexdigest() if args.candidates else None,
                  source_hashes={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [root/'data/processed/aave.duckdb',root/'data/documents/chunks.json']})
    config.update(rotate_modes=args.rotate_modes,cooldown_seconds=args.cooldown)
    if manifest.exists() and json.loads(manifest.read_text())!=config:raise ValueError('Run config changed; use a new directory')
    manifest.write_text(json.dumps(config,indent=2),encoding='utf-8')
    snapshot=out/'benchmark_snapshot.jsonl';serialized=''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in records)
    if snapshot.exists() and snapshot.read_text(encoding='utf-8')!=serialized:raise ValueError('Benchmark snapshot changed')
    if not snapshot.exists():snapshot.write_text(serialized,encoding='utf-8')
    candidates=out/'candidates.jsonl';source=args.candidates or candidates
    existing={r['question_id']:r for r in [json.loads(s) for s in source.read_text(encoding='utf-8').splitlines()]} if source.exists() else {}
    results=out/'results.jsonl';done={(r['question_id'],r['mode']) for r in [json.loads(s) for s in results.read_text(encoding='utf-8').splitlines()]} if results.exists() else set()
    for index,q in enumerate(records):
        if q['id'] in existing:draft=restore(existing[q['id']]['draft'])
        else:
            draft=a.make_draft(q['question']);row={'question_id':q['id'],'draft':asdict(draft)}
            with candidates.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
        offset=index%len(args.modes) if args.rotate_modes else 0
        ordered_modes=args.modes[offset:]+args.modes[:offset]
        for mode in ordered_modes:
            if (q['id'],mode) in done:continue
            if args.cooldown:time.sleep(args.cooldown)
            result=a.continue_draft(draft,mode);row=dict(asdict(result),question_id=q['id'],category=q['category'],repeat=0,shared_draft_id=q['id']+'-R0')
            with results.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
            print(q['id'],mode,result.status,round(result.elapsed,2),result.error,flush=True)
        # Slow scheduling between cases is outside each case's end-to-end timer.
        time.sleep(1)

if __name__=='__main__':main()
