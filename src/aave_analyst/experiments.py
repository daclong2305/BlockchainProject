from pathlib import Path
from datetime import datetime,timezone
from dataclasses import asdict
import json,hashlib,statistics,random
from .models import Draft,QuerySpec,RunResult
from .pipeline import MODES
from .benchmark import validate_benchmark
from .evaluation import factual_score,citation_metrics,percentile


def run_experiments(analyst,records,outdir,repeats=3,final=True,modes=None):
    validate_benchmark(records,final=final)
    modes=modes or list(MODES)
    if any(m not in MODES for m in modes):raise ValueError("Unknown experiment mode")
    outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True)
    output=outdir/"results.jsonl"
    if output.exists():raise FileExistsError("Use a new run directory; results are immutable")
    results=[]
    with output.open("w",encoding="utf-8") as f:
        for repeat in range(repeats):
            for question in records:
                try:
                    shared=analyst.make_draft(question["question"])
                    draft_error=None
                except Exception as exc:
                    shared=Draft(question=question["question"],spec=QuerySpec(),answer="")
                    draft_error=f"{type(exc).__name__}: {exc}"
                for mode in modes:
                    if draft_error:result=RunResult(mode,shared,"error",error=draft_error)
                    else:result=analyst.continue_draft(shared,mode)
                    row=dict(asdict(result),question_id=question["id"],category=question.get("category",""),repeat=repeat,shared_draft_id=f"{question['id']}-R{repeat}")
                    results.append(row);f.write(json.dumps(row,ensure_ascii=False,default=str)+"\n");f.flush()
    return results


def score_results(records,results,llm=None):
    gold={r["id"]:r for r in records};scores=[]
    for result in results:
        record=gold[result["question_id"]];factual=factual_score(record,result)
        judge=None;error="";draft=result["draft"]
        # Judge also audits factual wording/scope and all citations; numbers alone
        # cannot prove the answer names the correct asset/time or supports a claim.
        if llm and not result.get("error"):
            try:
                judge=llm.complete("judge",{"question":record["question"],"source_data":record["sources"],"reference_answer":record["reference_answer"],"system_answer":draft["answer"],"system_claims":draft.get("claims",[]),"candidate_sources":{"documents":draft.get("documents",[]),"sql":draft.get("sql"),"result":draft.get("query_result")}},timeout=120)
                for key in ("answer_correctness","faithfulness","citation_quality"):
                    if judge.get(key) not in (0,1):raise ValueError(f"Invalid judge score {key}")
            except Exception as exc:error=f"{type(exc).__name__}: {exc}";judge=None
        judge_pass=all(judge[k]==1 for k in ("answer_correctness","faithfulness","citation_quality")) if judge else None
        correctness=False if result.get("error") else ((judge_pass and factual is not False) if judge else None)
        citation=citation_metrics(judge.get("claim_checks",[])) if judge else {"precision":None,"completeness":None}
        scores.append({"question_id":record["id"],"category":record["category"],"mode":result["mode"],"repeat":result["repeat"],"numeric_correct":factual,"correct":correctness,"judge":judge,"judge_error":error,"citation":citation,"refused":draft.get("refused",False),"expected_refusal":record.get("expected_refusal",False),"elapsed":result["elapsed"],"input_tokens":sum(u.get("input_tokens",0) for u in result.get("usage",[])),"output_tokens":sum(u.get("output_tokens",0) for u in result.get("usage",[])),"sql_calls":sum(t['tool']=='sql' for t in result.get('tools',[])),"retrieval_calls":sum(t['tool']=='retrieve' for t in result.get('tools',[])),"runtime_error":bool(result.get("error"))})
    return scores


def summarize(scores):
    summary={}
    for mode in sorted({r['mode'] for r in scores}):
        subset=[r for r in scores if r['mode']==mode];n=len(subset);known=[r for r in subset if r['correct'] is not None];numeric=[r for r in subset if r['numeric_correct'] is not None]
        lat=[r['elapsed'] for r in subset]
        summary[mode]={"outputs":n,"scored_outputs":len(known),"correct":sum(bool(r['correct']) for r in known),"correct_rate":sum(bool(r['correct']) for r in known)/len(known) if known else None,"numeric_correct":sum(bool(r['numeric_correct']) for r in numeric),"numeric_total":len(numeric),"correct_refusals":sum(bool(r['refused'] and r['expected_refusal'] and r['judge'] and r['judge'].get('refusal_correct') and r['judge'].get('answer_correctness')==1) for r in subset),"wrong_refusals":sum(r['refused'] and not r['expected_refusal'] for r in subset),"unscored_refusals":sum(r['refused'] and r['expected_refusal'] and not r['judge'] for r in subset),"unsupported_answers":sum(r['judge'] is not None and r['judge']['faithfulness']==0 for r in subset),"median_seconds":statistics.median(lat) if lat else None,"p95_seconds":percentile(lat,.95),"input_tokens":sum(r['input_tokens'] for r in subset),"output_tokens":sum(r['output_tokens'] for r in subset),"runtime_errors":sum(r['runtime_error'] for r in subset),"judge_errors":sum(bool(r['judge_error']) for r in subset),"api_cost_usd":None,"cost_note":"Use your account pricing; judge tokens recorded separately. Shared draft cost is included in every mode."}
        for key in ['precision','completeness']:
            vals=[r['citation'][key] for r in subset if r['citation'][key] is not None]
            summary[mode]['citation_'+key]=statistics.mean(vals) if vals else None
        # Question is the unit; report its mean score over repeats.
        summary[mode]['per_question']={qid:{'correct_runs':sum(bool(r['correct']) for r in known if r['question_id']==qid),'scored_runs':sum(r['question_id']==qid for r in known)} for qid in sorted({r['question_id'] for r in subset})}
        summary[mode]['by_category']={cat:{'correct':sum(bool(r['correct']) for r in known if r['category']==cat),'scored':sum(r['category']==cat for r in known)} for cat in sorted({r['category'] for r in subset})}
    pairs={}
    for control in ['B0','B1','P-SQL','P-Evidence','P-Repair']:
        other={(r['question_id'],r['repeat']):r for r in scores if r['mode']==control}
        matched=[(other[(r['question_id'],r['repeat'])],r) for r in scores if r['mode']=='P' and (r['question_id'],r['repeat']) in other]
        pairs[control]={'wrong_to_right':sum(a['correct'] is False and b['correct'] is True for a,b in matched),'right_to_wrong':sum(a['correct'] is True and b['correct'] is False for a,b in matched),'paired_scored':sum(a['correct'] is not None and b['correct'] is not None for a,b in matched)}
    return {'configurations':summary,'paired_P_vs':pairs,'unit':'question; repeated outputs are not independent questions'}


def human_audit_sample(scores,seed=2026):
    rng=random.Random(seed);selected=[]
    for key in sorted({(r['mode'],r['category']) for r in scores}):
        group=[r for r in scores if (r['mode'],r['category'])==key and r.get('judge')]
        count=max(1,round(len(group)*.2)) if group else 0
        selected.extend(rng.sample(group,count))
    return [dict(r,reviewer_1={"name":"","answer_correctness":None,"faithfulness":None,"citation_quality":None},reviewer_2={"name":"","answer_correctness":None,"faithfulness":None,"citation_quality":None}) for r in selected]
