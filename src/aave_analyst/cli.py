import argparse,hashlib,json,os,sys,uuid
from datetime import datetime,timezone
from pathlib import Path
from dataclasses import asdict
from .database import Database
from .retrieval import Retriever,collect_documents
from .data import prepare_data
from .llm import BedrockLLM
from .config import read_settings
from .pipeline import Analyst,MODES
from .benchmark import create_benchmark,save_benchmark,load_benchmark,freeze_benchmark,validate_benchmark
from .experiments import run_experiments,score_results,summarize,human_audit_sample
from .stress import create_stress,evaluate_stress
from .reporting import human_report


def write_json(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2,default=str),encoding="utf-8")


def analyst_at(root):
    return Analyst(Database(root/"data/processed/aave.duckdb"),Retriever.load(root/"data/documents/chunks.json"),BedrockLLM())


def source_hashes(root):
    paths=[root/"data/processed/aave.duckdb",root/"data/processed/dictionary.json",root/"data/documents/chunks.json",root/"data/benchmark/questions.jsonl"]
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def code_hashes():
    return {p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))}


def doctor(live=False):
    llm=BedrockLLM();result=llm.config()
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
    p=sub.add_parser("stress");p.add_argument("--split",choices=["dev","test"],default="dev");p.add_argument("--out",type=Path)
    p=sub.add_parser("human-report");p.add_argument("audit_file",type=Path)
    args=parser.parse_args(argv);root=args.root.resolve();bench=root/"data/benchmark/questions.jsonl"
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
        value=freeze_benchmark(bench);value["source_hashes"]=source_hashes(root);value["llm_config"]=BedrockLLM().config();value['code_hashes']=code_hashes()
        write_json(bench.with_suffix(".lock.json"),value);print(json.dumps(value,indent=2));return value
    if args.command=="ask":
        result=analyst_at(root).answer(args.question,args.mode)
        print(json.dumps(asdict(result),ensure_ascii=False,indent=2));return result
    if args.command=="run":
        if args.repeats<1:raise ValueError("repeats must be positive")
        if args.split=="test" and not args.final:raise ValueError("Use only dev during development; test requires --final and approved frozen benchmark")
        if args.final:
            if args.split!="test" or args.limit or args.repeats!=3 or set(args.modes)!=set(MODES):raise ValueError("Final protocol requires all 40 test questions, six modes, three repeats")
            lock=json.loads(bench.with_suffix(".lock.json").read_text(encoding="utf-8"))
            if lock.get("source_hashes")!=source_hashes(root):raise ValueError("Source/benchmark changed since freeze")
            if lock.get("llm_config")!=BedrockLLM().config():raise ValueError("Model configuration changed since freeze")
            if lock.get('code_hashes')!=code_hashes():raise ValueError('Runtime/evaluation code changed since freeze')
        rows=[r for r in load_benchmark(bench) if r["split"]==args.split]
        if args.limit:rows=rows[:args.limit]
        out=args.out or root/"runs"/(datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")+"-"+uuid.uuid4().hex[:6])
        instance=analyst_at(root)
        results=run_experiments(instance,rows,out,args.repeats,args.final,args.modes)
        save_benchmark(rows,out/"benchmark_snapshot.jsonl")
        write_json(out/"config.json",{"llm":instance.llm.config(),"source_hashes":source_hashes(root),"code_hashes":code_hashes(),"final":args.final,"modes":args.modes,"repeats":args.repeats,"deadline_seconds":120,"repair_limit":2,"retrieval_top_k":5,"chunk_words":400,"chunk_overlap":60})
        print(f"Saved {len(results)} outputs to {out}");return results
    if args.command=="score":
        folder=args.run_dir;rows=load_benchmark(folder/"benchmark_snapshot.jsonl");results=load_benchmark(folder/"results.jsonl")
        llm=BedrockLLM() if args.judge else None;scores=score_results(rows,results,llm)
        save_benchmark(scores,folder/"scores.jsonl");write_json(folder/"summary.json",summarize(scores))
        write_json(folder/"human_audit.json",human_audit_sample(scores));write_json(folder/"judge_usage.json",llm.calls if llm else [])
        print(json.dumps(summarize(scores),ensure_ascii=False,indent=2));return scores
    if args.command=="stress":
        rows=[r for r in load_benchmark(bench.with_name("stress.jsonl")) if r["split"]==args.split]
        if args.split=="test":
            for r in rows:
                review=r['review']
                if not review.get('approved') or not review.get('reviewer_1') or not review.get('reviewer_2') or review['reviewer_1']==review['reviewer_2']:raise ValueError("Independent review required before stress test")
        results=evaluate_stress(rows,analyst_at(root));out=args.out or root/"runs"/("stress-"+uuid.uuid4().hex[:8]+".jsonl")
        save_benchmark(results,out);print(f"Saved {len(results)} stress outputs to {out}");return results


if __name__=="__main__":
    try:main()
    except Exception as exc:
        print(f"ERROR: {type(exc).__name__}: {exc}",file=sys.stderr)
        sys.exit(1)
