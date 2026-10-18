from dataclasses import asdict
from copy import deepcopy
import time
from .models import QuerySpec,Draft
from .verification import semantic_rules,response_issues
from .data import DICTIONARY


def create_stress(db):
    rows=[]
    for split,assets in [('dev',['USDC','WETH']),('test',['USDT','DAI'])]:
        for asset in assets:
            measure='borrowed_usd' if split=='dev' else 'supplied_usd'
            operation='avg' if split=='dev' else 'max'
            start,stop=('2026-08-01','2026-09-01') if split=='dev' else ('2025-01-01','2026-01-01')
            where=f"asset='{asset}' AND hour>=TIMESTAMPTZ '{start}' AND hour<TIMESTAMPTZ '{stop}'"
            q=f"Dư nợ {asset} trung bình theo giờ tháng 8/2026 là bao nhiêu USD?" if split=='dev' else f"Giá trị tài sản cung cấp {asset} lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?"
            expression=f'{operation}({measure})'
            correct=f"SELECT {expression} AS value FROM market_hourly WHERE {where}"
            for kind,wrong in [
                ('metric',correct.replace(measure,'supplied_usd' if split=='dev' else 'borrowed_usd')),
                ('aggregation',correct.replace(expression,f'sum({measure})')),
                ('filter',correct.replace("asset='"+asset+"'","asset='USDe'")),
                ('unit',correct.replace(expression,expression+'/1000000')),
                ('join',f"SELECT avg(m.borrowed_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.asset=n.asset WHERE m.{where.replace(' AND hour',' AND m.hour')}")
            ]:
                # A join stress case must have an unequal grouping/aggregation,
                # not a duplicated average that happens to preserve the answer.
                if kind=='join':
                    if split=='dev':
                        wrong=f"SELECT sum(m.borrowed_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.asset=n.asset WHERE m.asset='{asset}' AND m.hour=TIMESTAMPTZ '2026-08-01' AND n.hour>=TIMESTAMPTZ '2026-08-01' AND n.hour<TIMESTAMPTZ '2026-09-01'";correct_join=f"SELECT borrowed_usd AS value FROM market_hourly WHERE asset='{asset}' AND hour=TIMESTAMPTZ '2026-08-01'";question=f"Dư nợ {asset} lúc 00:00 UTC 2026-08-01 là bao nhiêu USD?"
                    else:
                        correct_join=f"SELECT max(supplied_usd)-min(supplied_usd) AS value FROM market_hourly WHERE {where}"
                        wrong=f"SELECT max(m.supplied_usd)-min(n.supplied_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.hour=n.hour WHERE m.asset='{asset}' AND n.asset='USDe' AND m.hour>=TIMESTAMPTZ '{start}' AND m.hour<TIMESTAMPTZ '{stop}'";question=f"Khoảng cách giữa giá trị tài sản cung cấp {asset} lớn nhất và nhỏ nhất trong năm 2025 là bao nhiêu USD?"
                else:correct_join=correct;question=q
                rows.append({'id':f'S{len(rows)+1:03d}','split':split,'family':f'{split}_{asset}_{kind}','question':question,'error_type':kind,'correct_sql':correct_join,'wrong_sql':wrong,'reference_rows':db.query(correct_join).rows,'review':{'reviewer_1':'','reviewer_2':'','approved':False}})
    return rows


def evaluate_stress(rows,analyst):
    results=[]
    for row in rows:
        for label,sql in [('wrong',row['wrong_sql']),('correct',row['correct_sql'])]:
            started=time.perf_counter();usage_start=len(analyst.llm.calls);tools_start=len(analyst.db.calls)
            req=analyst.llm.complete('plan',{'question':row['question'],'dictionary':DICTIONARY})
            spec=QuerySpec(**{k:v for k,v in req.items() if k in QuerySpec.__dataclass_fields__})
            draft=Draft(question=row['question'],spec=spec,sql=sql,query_result=analyst.db.query(sql))
            analyst._answer(draft,started+analyst.deadline)
            draft.elapsed=time.perf_counter()-started
            draft.usage=deepcopy(analyst.llm.calls[usage_start:]);draft.tools=deepcopy(analyst.db.calls[tools_start:])
            for mode in ['B1','P']:
                # Detection/repaired answer are logged separately. Gold is not
                # passed to the runtime checker or repair loop.
                result=analyst.continue_draft(draft,mode)
                results.append(dict(asdict(result),stress_id=row['id'],error_type=row['error_type'],injected=label,reference_rows=row['reference_rows']))
    return results
