from dataclasses import asdict
import sqlglot
from sqlglot import exp
from .models import Issue
from .evaluation import numeric_equal
from .planning import runtime_dictionary
from datetime import datetime,timedelta,timezone
from .intent_guards import question_anchors


def utc_datetime(value):
    parsed = datetime.fromisoformat(value.replace('Z', '+00:00'))
    return parsed.replace(tzinfo=timezone.utc) if parsed.tzinfo is None else parsed.astimezone(timezone.utc)


def coverage_rules(db, spec, timeout=15., *, draft=None):
    if draft is not None:
        draft.planning.pop('market_sample', None)
    if not spec.assets or not spec.start:
        return []
    try:
        start = utc_datetime(spec.start)
        end = utc_datetime(spec.end) if spec.end else start + timedelta(hours=1)
        if end <= start:
            return [Issue("time_range", "End must be after start", "stop")]
        assets = ', '.join("'" + asset.replace("'", "''") + "'" for asset in spec.assets)
        measure_hours = (draft is not None and spec.end and 'market_hourly' in draft.sql.lower()
                         and all((value.minute, value.second, value.microsecond) == (0, 0, 0)
                                 for value in (start, end)))
        if measure_hours:
            sample = (
                "SELECT asset, count(*) AS n, count(DISTINCT date_trunc('hour',hour)) AS slots, "
                "count(*) FILTER (WHERE hour <> date_trunc('hour',hour)) AS off_grid "
                f"FROM market_hourly WHERE asset IN ({assets}) AND hour >= TIMESTAMPTZ '{start.isoformat()}' "
                f"AND hour < TIMESTAMPTZ '{end.isoformat()}' GROUP BY asset"
            )
            query = (f"SELECT coverage.*, sample.n, sample.slots, sample.off_grid FROM coverage "
                     f"LEFT JOIN ({sample}) AS sample USING (asset) WHERE coverage.asset IN ({assets})")
        else:
            query = f"SELECT * FROM coverage WHERE asset IN ({assets})"
        available = {row['asset']: row for row in db.query(query, timeout=timeout).rows}
        if measure_hours:
            record_market_sample(draft, available, start, end)
        issues = []
        for asset in spec.assets:
            row = available.get(asset)
            if (not row or start < utc_datetime(row['start_utc'])
                    or end > utc_datetime(row['end_utc']) + timedelta(hours=1)):
                issues.append(Issue("coverage", f"Requested interval for {asset} exceeds available observations", "stop"))
        return issues
    except (ValueError, TypeError, AttributeError) as exc:
        return [Issue("time_range", f"Invalid time requirement: {exc}", "stop")]


def record_market_sample(draft, rows, start, end):
    expected = (end - start) // timedelta(hours=1)
    checks = {}
    for asset in draft.spec.assets:
        row = rows.get(asset, {})
        count = row.get('n') or 0
        slots = row.get('slots') or 0
        checks[asset] = {'rows': count, 'observed_slots': slots,
                         'one_row_per_hour': count == slots == expected and row.get('off_grid') == 0}
    draft.planning['market_sample'] = {'table': 'market_hourly', 'from_inclusive': start.isoformat(),
                                       'to_exclusive': end.isoformat(), 'expected_slots_per_asset': expected,
                                       'assets': checks}


def semantic_rules(sql,spec,question=None):
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
    anchors=question_anchors(question)
    metric=anchors.get('metric',spec.get("metric"))
    if metric in {"borrowed_usd","supplied_usd"} and metric not in cols:
        issues.append(Issue('question_metric' if 'metric' in anchors else 'metric',f"Original question requires {metric}; that column is missing from SQL" if 'metric' in anchors else 'Requested measure missing from SQL','sql'))
    literals={x.this for x in tree.find_all(exp.Literal) if x.is_string}
    assets=spec.get("assets",[])
    tables={t.name for t in tree.find_all(exp.Table)}
    if "market_hourly" in tables and assets:
        # A token name in the projection can label a different token's observations.
        filters = set()
        for where in tree.find_all(exp.Where):
            for condition in where.find_all(exp.EQ, exp.In):
                column = condition.this
                values = condition.expressions if isinstance(condition, exp.In) else [condition.expression]
                if isinstance(condition, exp.EQ) and isinstance(condition.expression, exp.Column):
                    column, values = condition.expression, [condition.this]
                if isinstance(column, exp.Column) and column.name.lower() == 'asset':
                    filters.update(v.this for v in values if isinstance(v, exp.Literal) and v.is_string)
        if not set(assets).issubset(filters or literals):
            issues.append(Issue("asset_filter","Requested asset differs from market_hourly filter","sql"))
    if "liquidation_events" in tables and assets:issues.append(Issue("unverified_mapping","Liquidation filtering by token is not verified","stop"))
    for field in ("start","end"):
        target=anchors.get(field,spec.get(field))
        if target and not any(str(target)[:10] in value for value in literals):issues.append(Issue("time_filter",f"Missing requested {field} boundary {target}","sql"))
    return issues


def response_issues(value):
    out=[]
    if not isinstance(value.get("issues"),list):raise ValueError("Reviewer must return issues list")
    for i in value["issues"]:
        # Archived reviews use success codes without a finding kind. New specialists
        # distinguish a confirmed check from an actionable mismatch explicitly.
        kind = i.get('kind')
        if kind == 'confirmation' or (kind is None and str(i.get('code','')).casefold() in
                                      {'claim_supported', 'complete_answer', 'answer_complete',
                                       'citation_valid'}):
            continue
        if kind not in (None, 'defect'):
            raise ValueError('Unknown reviewer finding kind')
        action=i.get("action","answer")
        out.append(Issue(str(i.get("code","review")),str(i.get("message","Unspecified issue")),action if action in {"sql","answer","retrieve","stop"} else "answer"))
    return out


def interval_checks(draft, *, include_markets=False):
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
    result = {'liquidation_events':{'relation':relation,'proves_complete_collection':False}}
    if not include_markets:
        return result
    market_rows = draft.planning.get('availability', {}).get('market_hourly', [])
    markets = {r['asset']: r for r in market_rows}
    checks = {}
    for asset in draft.spec.assets:
        row = markets.get(asset, {})
        market_relation = 'unknown'
        try:
            start = date(draft.spec.start)
            end = date(draft.spec.end) if draft.spec.end else start + timedelta(hours=1)
            first = date(row['start_utc'])
            # Each hourly observation covers the hour starting at its timestamp.
            upper = date(row['end_utc']) + timedelta(hours=1)
            if start < end and first < upper:
                if end <= first: market_relation = 'before_first_observation'
                elif start >= upper: market_relation = 'after_last_observation'
                elif first <= start and end <= upper: market_relation = 'within_observed_bounds'
                else: market_relation = 'overlaps_observed_bounds'
        except (ValueError, TypeError, KeyError, AttributeError):
            pass
        checks[asset] = {'relation': market_relation, 'proves_complete_collection': False}
    result['market_hourly'] = checks
    return result


def numeric_cell(draft, claim):
    numeric = claim['numeric']
    if (not draft.query_result or numeric.get('evidence_id') != 'SQL1' or
            'SQL1' not in claim.get('citations', [])):
        raise ValueError('Missing SQL citation or result')
    index = numeric['row']
    if isinstance(index, str) and index.isdecimal():
        index = int(index)
    if type(index) is not int or index < 0:
        raise ValueError('Invalid result row')
    return draft.query_result.rows[index][numeric['column']]


def numeric_evidence(draft):
    cells = []
    for index, claim in enumerate(draft.claims):
        if not claim.get('numeric'):
            continue
        try:
            value = numeric_cell(draft, claim)
            numeric = claim['numeric']
            cells.append({'claim_index': index, 'evidence_id': 'SQL1', 'row': numeric['row'],
                          'column': numeric['column'], 'cell_value': value})
        except (KeyError,IndexError,TypeError,ValueError,AttributeError):
            # claim_rules reports a broken link. Do not advertise it as evidence.
            continue
    return cells


def evidence_payload(draft, *, specialist=False):
    documents=[{key:doc[key] for key in ('id','title','url','text') if key in doc}
               for doc in draft.documents]
    payload = {"question":draft.question,"requirements":asdict(draft.spec),"sql":draft.sql,"sql_result":asdict(draft.query_result) if draft.query_result else None,"documents":documents,"answer":draft.answer,"claims":draft.claims,"refused":draft.refused}
    if specialist:
        payload['numeric_evidence'] = numeric_evidence(draft)
        if 'market_sample' in draft.planning:
            payload['market_sample'] = draft.planning['market_sample']
    payload.update(dictionary=runtime_dictionary(), availability=draft.planning.get('availability',{}),
                   interval_checks=interval_checks(draft, include_markets=specialist),
                   retrieval_runs=[call for call in draft.tools if call.get('tool')=='retrieve'])
    return payload


def sql_review_payload(draft):
    payload=evidence_payload(draft, specialist=True)
    # Protocol prose belongs to claim review, not SQL semantics or event coverage.
    result={key:payload[key] for key in ('question','requirements','sql','sql_result',
                                       'dictionary','availability','interval_checks')}
    result['document_review']={'handled_by':'claim_review',
                               'retrieved_ids':[doc['id'] for doc in draft.documents]}
    result['question_anchors']=question_anchors(draft.question)
    if 'market_sample' in payload:
        result['market_sample'] = payload['market_sample']
    return result


def claim_rules(draft):
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
                value=numeric_cell(draft, claim)
                if not numeric_equal(numeric.get("value"),value,numeric.get("unit","USD"),numeric.get("decimals",2)):
                    issues.append(Issue("numeric_mismatch","Claim value does not match executed result cell","answer"))
            except (KeyError,IndexError,TypeError,ValueError,AttributeError):issues.append(Issue("numeric_link","Numeric claim points to invalid SQL result cell","answer"))
    return issues


def specialist_findings(draft, response):
    issues = response_issues(response)
    measured = draft.planning.get('market_sample', {}).get('assets', {})
    observed = bool(draft.spec.assets) and all(measured.get(asset, {}).get('one_row_per_hour') is True
                                               for asset in draft.spec.assets)
    numeric_only = (draft.spec.kind == 'data' and bool(draft.claims)
                    and all(claim.get('numeric') and claim.get('citations') == ['SQL1']
                            for claim in draft.claims)
                    and not claim_rules(draft))

    # These two findings have precise, independently checkable premises. Keep
    # other findings, including failures about SQL meaning and unsupported prose.
    contradicted = set()
    if observed:
        contradicted.add('future_interval')
    if numeric_only:
        contradicted.add('no_supporting_documents')
    return [issue for issue in issues if issue.code.casefold() not in contradicted]


def verify_claims(draft,llm,timeout=60.):
    response = llm.complete("claim_review", evidence_payload(draft, specialist=True), timeout=timeout)
    return claim_rules(draft) + specialist_findings(draft, response)
