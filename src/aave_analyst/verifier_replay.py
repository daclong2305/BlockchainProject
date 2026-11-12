"""Reference-free detection, followed by offline metrics against provisional labels."""
from copy import deepcopy
from dataclasses import asdict
import hashlib, json, time
from botocore.exceptions import ReadTimeoutError, ConnectTimeoutError
from .verification import semantic_rules, coverage_rules, claim_rules, response_issues, evidence_payload, sql_review_payload

VARIANTS=('rules','generic','full','no_sql','no_evidence')

def verify_candidate(candidate,analyst,variant='full',deadline=120.):
    if variant not in VARIANTS:raise ValueError('Unknown verifier')
    draft=deepcopy(candidate);start=time.perf_counter();end=start+deadline
    calls=len(analyst.llm.calls);issues=[];error='';execution='completed';verdict=None
    def call(role,payload):
        return analyst.llm.complete(role,payload,timeout=analyst.remaining(end))
    try:
        if draft.error:raise ValueError('Candidate generation failed: '+draft.error)
        if variant=='generic':issues=response_issues(call('generic_review',evidence_payload(draft)))
        else:
            if variant!='no_sql' and draft.sql:
                issues.extend(semantic_rules(draft.sql,asdict(draft.spec),question=draft.question))
                issues.extend(coverage_rules(analyst.db,draft.spec,timeout=min(15,analyst.remaining(end))))
                if variant!='rules':issues.extend(response_issues(call('sql_review',sql_review_payload(draft))))
            # Independent detection examines prose even when SQL has an issue.
            if variant!='no_evidence':
                issues.extend(claim_rules(draft))
                if variant!='rules':issues.extend(response_issues(call('claim_review',evidence_payload(draft))))
        analyst.remaining(end)
        verdict='insufficient' if any(i.action=='stop' for i in issues) else ('fail' if issues else 'pass')
    except Exception as exc:
        error=f'{type(exc).__name__}: {exc}';execution='timeout' if isinstance(exc,(TimeoutError,ReadTimeoutError,ConnectTimeoutError)) else 'error'
    usage=deepcopy(analyst.llm.calls[calls:])
    return {'variant':variant,'candidate_sha256':hashlib.sha256(json.dumps(asdict(candidate),sort_keys=True,default=str).encode()).hexdigest(),
            'verdict':verdict,'execution_status':execution,'issues':[asdict(i) for i in issues],
            'elapsed':time.perf_counter()-start,'usage':usage,'inference_seconds':sum(c.get('elapsed',0) for c in usage),'error':error}

ALIASES={'metric':{'metric','question_metric'},'aggregation':{'stock_sum','aggregation'},'filter':{'asset_filter','time_filter','filter'},'unit':{'numeric_unit','unit'},'join':{'join','join_duplication'}}
def detection_metrics(rows):
    labeled=[r for r in rows if type(r.get('has_error')) is bool]
    completed=[r for r in labeled if r['execution_status']=='completed' and r['verdict'] in {'pass','fail'}]
    tp=sum(r['has_error'] and r['verdict']=='fail' for r in completed)
    fp=sum(not r['has_error'] and r['verdict']=='fail' for r in completed)
    fn=sum(r['has_error'] and r['verdict']=='pass' for r in completed)
    tn=sum(not r['has_error'] and r['verdict']=='pass' for r in completed)
    def ratio(a,b):return a/b if b else None
    target=[r for r in labeled if r.get('target_error')]
    hits=sum(any(i['code'] in ALIASES.get(r['target_error'],{r['target_error']}) for i in r['issues']) for r in target if r['execution_status']=='completed')
    precision=ratio(tp,tp+fp);recall=ratio(tp,tp+fn)
    return {'scheduled':len(rows),'labeled':len(labeled),'tp':tp,'fp':fp,'fn':fn,'tn':tn,
            'precision':precision,'recall_completed':recall,'f1_completed':ratio(2*tp,2*tp+fp+fn),
            'false_positive_rate_completed':ratio(fp,fp+tn),'recall_all_scheduled_errors':ratio(tp,sum(r['has_error'] for r in labeled)),
            'target_hits':hits,'target_total':len(target),'completion_rate':ratio(sum(r['execution_status']=='completed' for r in rows),len(rows)),
            'insufficient':sum(r['verdict']=='insufficient' for r in rows),'timeouts':sum(r['execution_status']=='timeout' for r in rows),'errors':sum(r['execution_status']=='error' for r in rows),
            'label_status':'provisional; no independent human validation'}
