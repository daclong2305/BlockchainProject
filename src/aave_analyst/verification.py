from dataclasses import asdict
import sqlglot
from sqlglot import exp
from .models import Issue
from .evaluation import numeric_equal
from .planning import runtime_dictionary
from datetime import datetime,timedelta,timezone


def coverage_rules(db,spec,timeout=15.):
    if not spec.assets or not spec.start:return []
    def date(x):
        value=datetime.fromisoformat(x.replace("Z","+00:00"))
        return value.replace(tzinfo=timezone.utc) if value.tzinfo is None else value
    try:
        start=date(spec.start);end=date(spec.end) if spec.end else start+timedelta(hours=1)
        if end<=start:return [Issue("time_range","End must be after start","stop")]
        assets=','.join("'"+a.replace("'","''")+"'" for a in spec.assets)
        rows=db.query(f"SELECT * FROM coverage WHERE asset IN ({assets})",timeout=timeout).rows
        available={r['asset']:r for r in rows};issues=[]
        for asset in spec.assets:
            r=available.get(asset)
            if not r or start<date(r['start_utc']) or end>date(r['end_utc'])+timedelta(hours=1):issues.append(Issue("coverage",f"Requested interval for {asset} exceeds available observations","stop"))
        return issues
    except (ValueError,TypeError) as e:return [Issue("time_range",f"Invalid time requirement: {e}","stop")]


def semantic_rules(sql,spec):
    if not sql:return []
    try:tree=sqlglot.parse_one(sql,read="duckdb")
    except Exception as e:return [Issue("sql_syntax",str(e),"sql")]
    issues=[];cols={c.name.lower() for c in tree.find_all(exp.Column)}
    for node in tree.find_all(exp.Sum):
        if any(c.name.lower() in {"borrowed_usd","supplied_usd"} for c in node.find_all(exp.Column)):
            # A sum across assets is valid at one explicit snapshot only.
            snapshot=any(isinstance(eq.left,exp.Column) and eq.left.name=="hour" for eq in tree.find_all(exp.EQ))
            if not snapshot:issues.append(Issue("stock_sum","Stock values must not be summed across hours","sql"))
    if spec.get("metric")=="transactions":
        good=any(isinstance(n.this,exp.Distinct) and any(c.name=="tx_hash" for c in n.find_all(exp.Column)) for n in tree.find_all(exp.Count))
        if not good:issues.append(Issue("transaction_count","Transactions require COUNT(DISTINCT tx_hash), not event rows","sql"))
    metric=spec.get("metric")
    if metric in {"borrowed_usd","supplied_usd"} and metric not in cols:issues.append(Issue("metric","Requested measure missing from SQL","sql"))
    literals={x.this for x in tree.find_all(exp.Literal) if x.is_string}
    assets=spec.get("assets",[])
    tables={t.name for t in tree.find_all(exp.Table)}
    if "market_hourly" in tables and assets and not set(assets).issubset(literals):issues.append(Issue("asset_filter","Requested asset literals missing from query","sql"))
    if "liquidation_events" in tables and assets:issues.append(Issue("unverified_mapping","Liquidation filtering by token is not verified","stop"))
    for field in ("start","end"):
        target=spec.get(field)
        if target and not any(str(target)[:10] in value for value in literals):issues.append(Issue("time_filter",f"Missing requested {field} boundary {target}","sql"))
    return issues


def response_issues(value):
    out=[]
    if not isinstance(value.get("issues"),list):raise ValueError("Reviewer must return issues list")
    for i in value["issues"]:
        action=i.get("action","answer")
        out.append(Issue(str(i.get("code","review")),str(i.get("message","Unspecified issue")),action if action in {"sql","answer","retrieve","stop"} else "answer"))
    return out


def interval_checks(draft):
    """Compute chronology explicitly; observed bounds never prove complete collection."""
    relation='unknown'
    bounds=draft.planning.get('availability',{}).get('liquidation_events',{})
    def date(value):
        parsed=datetime.fromisoformat(value.replace('Z','+00:00'))
        return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed
    try:
        start,end=date(draft.spec.start),date(draft.spec.end)
        first,last=date(bounds.get('first_event_utc')),date(bounds.get('last_event_utc'))
        if end>start and last>=first:
            if start>last:relation='after_last_observation'
            elif end<=first:relation='before_first_observation'
            elif start>=first and end<=last:relation='within_observed_bounds'
            else:relation='overlaps_observed_bounds'
    except (ValueError,TypeError,AttributeError):pass
    return {'liquidation_events':{'relation':relation,'proves_complete_collection':False}}


def evidence_payload(draft):
    documents=[{key:doc[key] for key in ('id','title','url','text') if key in doc}
               for doc in draft.documents]
    return {"question":draft.question,"requirements":asdict(draft.spec),"sql":draft.sql,"sql_result":asdict(draft.query_result) if draft.query_result else None,"documents":documents,"answer":draft.answer,"claims":draft.claims,"refused":draft.refused,
            "dictionary":runtime_dictionary(),"availability":draft.planning.get('availability',{}),
            "interval_checks":interval_checks(draft),
            "retrieval_runs":[call for call in draft.tools if call.get('tool')=='retrieve']}


def sql_review_payload(draft):
    payload=evidence_payload(draft)
    # Protocol prose belongs to claim review, not SQL semantics or event coverage.
    result={key:payload[key] for key in ('question','requirements','sql','sql_result',
                                       'dictionary','availability','interval_checks')}
    result['document_review']={'handled_by':'claim_review',
                               'retrieved_ids':[doc['id'] for doc in draft.documents]}
    return result


def verify_claims(draft,llm,timeout=60.):
    issues=[]
    docs={d["id"]:d for d in draft.documents};valid=set(docs)
    if draft.query_result:valid.add("SQL1")
    if not draft.claims and draft.answer and not draft.refused:issues.append(Issue("missing_claims","No evidence-linked factual claims supplied","answer"))
    for claim in draft.claims:
        cites=claim.get("citations",[])
        if not cites or any(c not in valid for c in cites):issues.append(Issue("citation_id","Missing or invalid citation ID","answer"))
        numeric=claim.get("numeric")
        if numeric:
            if draft.spec.unit and numeric.get('unit')!=draft.spec.unit:
                issues.append(Issue('numeric_unit','Numeric claim unit differs from requested unit','answer'))
            try:
                if numeric.get("evidence_id")!="SQL1" or "SQL1" not in cites:raise ValueError("numeric citation")
                value=draft.query_result.rows[int(numeric["row"])][numeric["column"]]
                if not numeric_equal(numeric.get("value"),value,numeric.get("unit","USD"),numeric.get("decimals",2)):
                    issues.append(Issue("numeric_mismatch","Claim value does not match executed result cell","answer"))
            except (KeyError,IndexError,TypeError,ValueError,AttributeError):issues.append(Issue("numeric_link","Numeric claim points to invalid SQL result cell","answer"))
    issues.extend(response_issues(llm.complete("claim_review",evidence_payload(draft),timeout=timeout)))
    return issues
