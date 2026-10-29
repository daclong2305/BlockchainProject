import argparse,hashlib,json,os,sys,uuid
from datetime import datetime,timezone
from pathlib import Path
from dataclasses import asdict
from .database import Database
from .retrieval import Retriever,collect_documents
from .data import prepare_data
from .llm import BedrockLLM
from .local_llm import configured_llm
from .config import read_settings
from .pipeline import Analyst,MODES
from .benchmark import create_benchmark,save_benchmark,load_benchmark,freeze_benchmark,validate_benchmark
from .experiments import run_experiments,score_results,summarize,human_audit_sample
from .stress import create_stress,evaluate_stress
from .reporting import human_report,experiment_markdown
from .review import export_reviews,import_reviews,content_hash
from .protocol import trace_selection,trace_forms,coverage_report,evaluation_protocol
from .scoring import checkpointed_scores
from .costs import experiment_costs
from .supplementary import trace_report,stress_report
from .audit_review import export_audit,import_audit


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str),encoding="utf-8")


def analyst_at(root,provider=None,deadline=120.):
    return Analyst(Database(root/"data/processed/aave.duckdb"),Retriever.load(root/"data/documents/chunks.json"),configured_llm(provider),deadline=deadline)


def source_hashes(root):
    paths=[root/"data/processed/aave.duckdb",root/"data/processed/dictionary.json",root/"data/documents/chunks.json",root/"data/benchmark/questions.jsonl",root/"data/benchmark/stress.jsonl",root/"data/benchmark/trace_registration.json"]
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def code_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))}


def doctor(live=False):
    llm=configured_llm();result=llm.config()
    if result['provider'] != 'bedrock':
        if live:
            result['live_response']=llm.complete('plan',{'question':'Health factor là gì?'})
            result['usage']=llm.calls
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return result
    try:
        session=llm.session()
        result["credentials_available"]=session.get_credentials() is not None
    except Exception as exc:result.update(credentials_available=False,credential_error=type(exc).__name__)
    if live:
        try:result["live_response"]=llm.complete("plan",{"question":"Health factor là gì?"});result["usage"]=llm.calls
        except Exception as exc:result["live_error"]=f"{type(exc).__name__}: {exc}"
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result


def main(argv=None):
    parser=argparse.ArgumentParser(description="Aave V3 evidence analyst and experiment runner")
    parser.add_argument("--root",type=Path,default=Path(read_settings().get("AAVE_PROJECT_ROOT") or "."))
    sub=parser.add_subparsers(dest="command",required=True)
    p=sub.add_parser("prepare",help="Download release, audit and build local DuckDB");p.add_argument("--source",type=Path)
    sub.add_parser("documents",help="Snapshot official Aave documents and build chunks")
    p=sub.add_parser("benchmark",help="Create 60 provisional questions + separate stress cases");p.add_argument("--overwrite",action="store_true")
    sub.add_parser("freeze",help="Require two human reviewers and lock gold + data hashes")
    p=sub.add_parser("doctor",help="Check Bedrock configuration without exposing credentials");p.add_argument("--live",action="store_true")
    p=sub.add_parser("ask");p.add_argument("question");p.add_argument("--mode",choices=list(MODES),default="P")
    p=sub.add_parser("run");p.add_argument("--split",choices=["dev","test"],default="dev");p.add_argument("--repeats",type=int,default=3);p.add_argument("--limit",type=int);p.add_argument("--modes",nargs="+",choices=list(MODES),default=list(MODES));p.add_argument("--out",type=Path);p.add_argument("--final",action="store_true")
    p=sub.add_parser("score");p.add_argument("run_dir",type=Path);p.add_argument("--judge",action="store_true",help="Calls Bedrock for independent evaluation; incurs API usage")
    p.add_argument('--resume',action='store_true',help='Continue an interrupted scoring journal with identical inputs/judge/code')
    p=sub.add_parser("stress");p.add_argument("--split",choices=["dev","test"],default="dev");p.add_argument("--out",type=Path)
    p=sub.add_parser("human-report");p.add_argument("audit_file",type=Path)
    p=sub.add_parser('review-export');p.add_argument('source',type=Path);p.add_argument('destination',type=Path)
    p=sub.add_parser('review-import');p.add_argument('source',type=Path);p.add_argument('reviewer_1',type=Path);p.add_argument('reviewer_2',type=Path)
    sub.add_parser('trace-register',help='Select ten test IDs before final inference; never overwrite registration')
    p=sub.add_parser('coverage');p.add_argument('run_dir',type=Path)
    p=sub.add_parser('trace-report');p.add_argument('measurements',type=Path)
    p=sub.add_parser('stress-report');p.add_argument('results',type=Path)
    p=sub.add_parser('audit-export');p.add_argument('run_dir',type=Path);p.add_argument('destination',type=Path)
    p=sub.add_parser('audit-import');p.add_argument('run_dir',type=Path);p.add_argument('reviewer_1',type=Path);p.add_argument('reviewer_2',type=Path)
    args=parser.parse_args(argv);root=args.root.resolve();bench=root/"data/benchmark/questions.jsonl"
    if args.command=='review-export':
        value=export_reviews(args.source,args.destination);print(json.dumps(value,indent=2));return value
    if args.command=='audit-export':
        value=export_audit(args.run_dir/'human_audit.json',args.destination);print(json.dumps(value,indent=2));return value
    if args.command=='audit-import':
        output=args.run_dir/'human_audit_completed.json'
        if output.exists():raise FileExistsError('Preserve existing completed human audit')
        completed=import_audit(args.run_dir/'human_audit.json',args.reviewer_1,args.reviewer_2)
        value=human_report(completed);write_json(output,completed);write_json(args.run_dir/'human_agreement.json',value)
        print(json.dumps(value,indent=2));return value
    if args.command=='review-import':
        value=import_reviews(args.source,args.reviewer_1,args.reviewer_2);print(json.dumps(value,indent=2));return value
    if args.command=='trace-register':
        destination=bench.with_name('trace_registration.json')
        if destination.exists():raise FileExistsError('Trace registration already exists')
        rows=load_benchmark(bench)
        value=trace_selection(rows);value['benchmark_sha256']=hashlib.sha256(bench.read_bytes()).hexdigest()
        value['content_hashes']={r['id']:content_hash(r) for r in rows}
        write_json(destination,value);write_json(bench.with_name('trace_measurements.json'),trace_forms(value))
        print(f'Registered {len(value["selected"])} test IDs; no inference performed');return value
    if args.command=='coverage':
        value=coverage_report(load_benchmark(args.run_dir/'benchmark_snapshot.jsonl'),load_benchmark(args.run_dir/'results.jsonl'))
        write_json(args.run_dir/'coverage.json',value);print(json.dumps(value,indent=2));return value
    if args.command=='trace-report':
        value=trace_report(json.loads(args.measurements.read_text(encoding='utf-8')),json.loads(bench.with_name('trace_registration.json').read_text(encoding='utf-8')))
        write_json(args.measurements.with_suffix('.report.json'),value);print(json.dumps(value,indent=2));return value
    if args.command=='stress-report':
        rows=load_benchmark(args.results);value=stress_report(rows)
        write_json(args.results.with_suffix('.report.json'),value)
        review_path=args.results.with_suffix('.human-review.jsonl')
        if not review_path.exists():
            save_benchmark([dict(row,reviewer_1=row.get('reviewer_1',{'name':'','final_correct':None}),reviewer_2=row.get('reviewer_2',{'name':'','final_correct':None})) for row in rows],review_path)
        print(json.dumps(value,indent=2));return value
    if args.command=="doctor":return doctor(args.live)
    if args.command=="human-report":
        value=human_report(json.loads(args.audit_file.read_text(encoding='utf-8')))
        write_json(args.audit_file.with_name('human_agreement.json'),value);print(json.dumps(value,indent=2));return value
    if args.command=="prepare":value=prepare_data(root,args.source);print(json.dumps(value,ensure_ascii=False,indent=2));return value
    if args.command=="documents":value=collect_documents(root);print(f"Saved {len(value)} source chunks");return value
    if args.command=="benchmark":
        if bench.exists() and not args.overwrite:raise FileExistsError("Benchmark exists; use --overwrite only if intentionally discarding reviews")
        chunks=json.loads((root/"data/documents/chunks.json").read_text(encoding="utf-8"));db=Database(root/"data/processed/aave.duckdb")
        rows=create_benchmark(db,chunks);save_benchmark(rows,bench);save_benchmark(create_stress(db),bench.with_name("stress.jsonl"))
        print(f"Created {len(rows)} PROVISIONAL questions. Two independent human approvals required before final runs.");return rows
    if args.command=="freeze":
        if bench.with_suffix('.lock.json').exists():raise FileExistsError('Benchmark already frozen; preserve lock history')
        # Resolve every prerequisite before creating a lock, so a missing artifact
        # cannot leave an incomplete lock file behind.
        frozen_sources=source_hashes(root);frozen_llm=configured_llm().config();frozen_judge=BedrockLLM().config()
        registration=json.loads(bench.with_name('trace_registration.json').read_text(encoding='utf-8'))
        if registration.get('content_hashes')!={r['id']:content_hash(r) for r in load_benchmark(bench)}:
            raise ValueError('Question content changed since trace registration; re-register before any final inference')
        value=freeze_benchmark(bench);value["source_hashes"]=frozen_sources;value["llm_config"]=frozen_llm;value['code_hashes']=code_hashes()
        value['judge_config']=frozen_judge;value['evaluation_protocol']=evaluation_protocol()
        write_json(bench.with_suffix(".lock.json"),value);print(json.dumps(value,indent=2));return value
    if args.command=="ask":
        result=analyst_at(root).answer(args.question,args.mode)
        print(json.dumps(asdict(result),ensure_ascii=False,indent=2));return result
    if args.command=="run":
        if args.repeats<1:raise ValueError("repeats must be positive")
        if args.split=="test" and not args.final:raise ValueError("Use only dev during development; test requires --final and approved frozen benchmark")
        if args.final:
            if args.split!="test" or args.limit or args.repeats!=3 or len(args.modes)!=len(MODES) or set(args.modes)!=set(MODES):raise ValueError("Final protocol requires all 40 test questions, six modes, three repeats")
            lock=json.loads(bench.with_suffix(".lock.json").read_text(encoding="utf-8"))
            if lock.get("source_hashes")!=source_hashes(root):raise ValueError("Source/benchmark changed since freeze")
            if lock.get("llm_config")!=configured_llm().config():raise ValueError("Model configuration changed since freeze")
            if lock.get('code_hashes')!=code_hashes():raise ValueError('Runtime/evaluation code changed since freeze')
            if lock.get('judge_config')!=BedrockLLM().config() or lock.get('evaluation_protocol')!=evaluation_protocol():raise ValueError('Judge or evaluation protocol changed since freeze')
        rows=[r for r in load_benchmark(bench) if r["split"]==args.split]
        if args.limit:rows=rows[:args.limit]
        out=args.out or root/"runs"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:6])
        instance=analyst_at(root)
        if out.exists():raise FileExistsError("Use a new run directory to preserve experiment provenance")
        out.mkdir(parents=True)
        save_benchmark(rows,out/"benchmark_snapshot.jsonl")
        manifest={"llm":instance.llm.config(),"source_hashes":source_hashes(root),"code_hashes":code_hashes(),"final":args.final,"modes":args.modes,"repeats":args.repeats,"deadline_seconds":120,"repair_limit":2,"retrieval_top_k":5,"chunk_words":400,"chunk_overlap":60}
        manifest['judge_config']=BedrockLLM().config();manifest['evaluation_protocol']=evaluation_protocol()
        write_json(out/"config.json",manifest)
        try:
            results=run_experiments(instance,rows,out,args.repeats,args.final,args.modes)
        finally:
            after_sources,after_code=source_hashes(root),code_hashes()
            write_json(out/'integrity.json',{'source_hashes_after':after_sources,'code_hashes_after':after_code,
                       'sources_unchanged':manifest['source_hashes']==after_sources,'code_unchanged':manifest['code_hashes']==after_code})
        if args.final and (manifest['source_hashes']!=after_sources or manifest['code_hashes']!=after_code):
            raise ValueError('Sources/code changed during final run; results preserved but protocol invalid')
        print(f"Saved {len(results)} outputs to {out}");return results
    if args.command=="score":
        folder=args.run_dir;rows=load_benchmark(folder/"benchmark_snapshot.jsonl");results=load_benchmark(folder/"results.jsonl")
        if any((folder/name).exists() for name in ('scores.jsonl','summary.json','human_audit.json','judge_usage.json','report.md')):
            raise FileExistsError('Scoring artifacts already exist; preserve human labels and previous evaluations')
        llm=BedrockLLM() if args.judge else None
        manifest=json.loads((folder/'config.json').read_text(encoding='utf-8'))
        if manifest.get('final'):
            if not args.judge:raise ValueError('Final scoring requires the preregistered independent judge')
            if manifest.get('judge_config')!=llm.config() or manifest.get('code_hashes')!=code_hashes():raise ValueError('Judge/code differs from final run manifest')
            if not coverage_report(rows,results)['complete']:raise ValueError('Final scoring requires complete coverage; preserve incomplete results for diagnostics')
            integrity=json.loads((folder/'integrity.json').read_text(encoding='utf-8'))
            if not integrity.get('sources_unchanged') or not integrity.get('code_unchanged') or integrity.get('source_hashes_after')!=manifest.get('source_hashes') or integrity.get('code_hashes_after')!=manifest.get('code_hashes'):
                raise ValueError('Final run integrity was not verified; do not score as a valid final run')
        scores,judge_usage=checkpointed_scores(rows,results,llm,folder/'scoring_journal.jsonl',
                                             {'judge':llm.config() if llm else None,'code_hashes':code_hashes(),'run_manifest':manifest},resume=args.resume)
        save_benchmark(scores,folder/"scores.jsonl");write_json(folder/"summary.json",summarize(scores))
        audit=human_audit_sample(scores)
        write_json(folder/"human_audit.json",audit);write_json(folder/"judge_usage.json",judge_usage)
        eligible=sum(bool(row.get('judge')) for row in scores)
        write_json(folder/'audit_sampling.json',{'seed':2026,'population_outputs':len(scores),'eligible_judge_outputs':eligible,
                   'sampled':len(audit),'fraction_of_judged':len(audit)/eligible if eligible else None,
                   'fraction_of_all_outputs':len(audit)/len(scores) if scores else None,
                   'rule':evaluation_protocol()['audit_rule'],'note':'Runtime failures and failed judge calls are not successful judge labels; they remain in benchmark/error denominators.'})
        write_json(folder/'costs.json',experiment_costs(results,judge_usage,manifest))
        coverage=coverage_report(rows,results);write_json(folder/'coverage.json',coverage)
        (folder/'report.md').write_text(experiment_markdown(summarize(scores),coverage,json.loads((folder/'config.json').read_text(encoding='utf-8'))),encoding='utf-8')
        print(json.dumps(summarize(scores),ensure_ascii=False,indent=2));return scores
    if args.command=="stress":
        rows=[r for r in load_benchmark(bench.with_name("stress.jsonl")) if r["split"]==args.split]
        if args.split=="test":
            for r in rows:
                review=r['review']
                if not review.get('approved') or not review.get('reviewer_1') or not review.get('reviewer_2') or review['reviewer_1']==review['reviewer_2']:raise ValueError("Independent review required before stress test")
        out=args.out or root/"runs"/("stress-"+uuid.uuid4().hex[:8]+".jsonl")
        out.parent.mkdir(parents=True,exist_ok=True)
        with out.open('x',encoding='utf-8') as stream:
            def record_stress(result):
                stream.write(json.dumps(result,ensure_ascii=False,default=str)+'\n');stream.flush()
            results=evaluate_stress(rows,analyst_at(root),on_result=record_stress)
        print(f"Saved {len(results)} stress outputs to {out}");return results


if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}",file=sys.stderr)
        sys.exit(1)
