"""Build provisional gold from source SQL and reviewed-in-code topic outlines.

The output is deliberately NOT marked human-approved. Two independent people
must verify source selection, wording, units and answers before final runs.
"""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,re,unicodedata

CATEGORIES={"mechanism":(4,8),"lookup":(4,8),"analysis":(6,12),"mixed":(4,8),"unanswerable":(2,4)}


def _interval(column,start,end):return f"{column} >= TIMESTAMPTZ '{start}' AND {column} < TIMESTAMPTZ '{end}'"


def validate_benchmark(rows,final=False):
    seen={};ids=set();questions=set();templates={}
    for r in rows:
        if r["id"] in ids:raise ValueError("Duplicate question ID")
        ids.add(r["id"])
        question=r.get('question')
        if question:
            normalized=' '.join(unicodedata.normalize('NFKC',question).lower().split())
            if normalized in questions:raise ValueError('Duplicate question text')
            questions.add(normalized)
            template=re.sub(r'\b(usdc|usdt|usde|weth|dai)\b','ASSET',normalized)
            template=re.sub(r'\b\d{4}-\d{2}(?:-\d{2})?\b','DATE',template)
            if template in templates and templates[template]!=r['split']:raise ValueError('Question template leaked across splits')
            templates[template]=r['split']
        family=r["family"]
        if family in seen and seen[family]!=r["split"]:raise ValueError(f"Question family leaked across splits: {family}")
        seen[family]=r["split"]
        if final:
            review=r.get("review",{});a=review.get("reviewer_1","").strip();b=review.get("reviewer_2","").strip()
            if not a or not b or a==b or not review.get("approved"):
                raise ValueError(f"Independent human review required: {r['id']}")
            if not r.get("reference_answer") or not r.get("sources"):raise ValueError(f"Missing gold evidence: {r['id']}")


def create_benchmark(db,chunks):
    rows=[]
    def docs(key):return [dict(c) for c in chunks if c["id"].startswith("DOC_"+key+"_")]
    def add(category,family,split,q,sql="",unit="USD",concept="",source="",unanswerable=False):
        result=db.query(sql) if sql else None
        selected=docs(source) if source else []
        numbers=[]
        if result:
            for index,row in enumerate(result.rows):
                for column,value in row.items():
                    if isinstance(value,(int,float)) and not isinstance(value,bool):numbers.append({"row":index,"column":column,"value":value,"unit":unit,"decimals":2})
        reference={"required_points":[concept] if concept else [],"sql_result":result.rows if result else None,"limitation":concept if unanswerable else ""}
        sources=([{"id":"SQL1","sql":sql,"rows":result.rows}] if result else [])+selected
        if unanswerable:sources.append({"id":"POLICY","text":"Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."})
        rows.append({"id":f"Q{len(rows)+1:03d}","category":category,"family":family,"split":split,"question":q,"sql":sql,"reference_answer":reference,"expected_numeric":numbers,"sources":sources,"expected_refusal":unanswerable,"requires_judge":category in {"mechanism","mixed","unanswerable"},"scope":{"chain":"Ethereum","protocol":"Aave V3","start":"2025-01-01","end_exclusive":"2026-09-01"},"review":{"reviewer_1":"","reviewer_2":"","approved":False,"notes":"Provisional SQL/reference; independently verify before approval."}})

    topics=[
      ("supply_mechanism","dev","SUPPLY","Cung cấp tài sản trên Aave V3 là gì?","Cung cấp token vào pool; phân biệt cung cấp với vay, không bảo đảm mức lãi cố định."),
      ("collateral_mechanism","dev","BORROW","Tài sản thế chấp có vai trò gì khi vay trên Aave V3?","Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."),
      ("health_factor","test","LIQ","Health factor thể hiện điều gì và khi nào vị thế có nguy cơ thanh lý?","Health factor phản ánh mức an toàn của vị thế; dưới 1 có thể bị thanh lý, không đồng nghĩa chắc chắn bị thanh lý ngay lập tức."),
      ("liquidation_process","test","LIQ","Cơ chế thanh lý trên Aave V3 hoạt động như thế nào?","Thanh lý hoàn trả một phần nợ và nhận tài sản thế chấp theo cơ chế/điều kiện của giao thức; phân biệt điều kiện đủ với thời điểm thực hiện."),
      ("borrow_interest","test","BORROW","Người vay trên Aave V3 phải lưu ý gì về lãi vay?","Nợ vay chịu lãi; cần kiểm tra chính xác nội dung trang nguồn, không suy diễn lãi suất lịch sử từ tài liệu cơ chế."),
      ("withdraw_supply","test","SUPPLY","Việc rút tài sản đã cung cấp phụ thuộc vào điều kiện nào?","Rút phụ thuộc thanh khoản và mức an toàn nếu tài sản đang bảo đảm khoản vay; xác minh điều kiện theo nguồn."),
    ]
    for family,split,key,q,concept in topics:
        for suffix in [""," Hãy trả lời ngắn gọn và dẫn nguồn."]:add("mechanism",family,split,q+suffix,concept=concept,source=key)
    for i,(family,split) in enumerate([("supply_snapshot","dev"),("debt_snapshot","dev"),("transaction_count","test"),("event_count","test"),("liquidation_value","test"),("debt_peak","test")]):
        for j in range(2):
            asset=["USDC","WETH"][j];month=["2026-08","2025-08"][j];start=month+"-01";end=["2026-09-01","2025-09-01"][j]
            unit="USD"
            if family in {"supply_snapshot","debt_snapshot"}:
                col="supplied_usd" if family=="supply_snapshot" else "borrowed_usd"
                when=["2026-08-15","2025-08-15"][j]
                sql=f"SELECT {col} AS value FROM market_hourly WHERE asset='{asset}' AND hour=TIMESTAMPTZ '{when} 00:00:00+00'"
                q=f"{'Giá trị tài sản cung cấp' if col=='supplied_usd' else 'Dư nợ'} {asset} lúc 00:00 UTC ngày {when} là bao nhiêu USD?"
            elif family in {"transaction_count","event_count","liquidation_value"}:
                expression={"transaction_count":"count(DISTINCT tx_hash)","event_count":"count(*)","liquidation_value":"sum(amount_usd)"}[family]
                label={"transaction_count":"giao dịch thanh lý","event_count":"sự kiện thanh lý","liquidation_value":"giá trị thanh lý USD"}[family]
                sql=f"SELECT {expression} AS value FROM liquidation_events WHERE {_interval('time',start,end)}";q=f"Trong tháng {month} UTC có bao nhiêu {label} trên Aave V3 Ethereum?";unit="USD" if family=="liquidation_value" else "count"
            else:
                sql=f"SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='{asset}' AND {_interval('hour',start,end)}";q=f"Dư nợ {asset} lớn nhất theo quan sát giờ trong tháng {month} là bao nhiêu USD?"
            add("lookup",family,split,q,sql,unit)
    families=[("avg_debt","dev"),("avg_supply","dev"),("asset_gap","test"),("quarter_change","test"),("peak_month_tx","test"),("liquidation_change","test")]
    for family,split in families:
        for j,asset in enumerate(["DAI","USDT","USDe"]):
            month=["2026-06","2026-07","2026-08"][j];end=["2026-07-01","2026-08-01","2026-09-01"][j];where=_interval("hour",month+"-01",end);unit="USD"
            if family in {"avg_debt","avg_supply"}:
                col="borrowed_usd" if family=="avg_debt" else "supplied_usd"
                sql=f"SELECT avg({col}) AS value FROM market_hourly WHERE asset='{asset}' AND {where}";q=f"Giá trị {'dư nợ' if col=='borrowed_usd' else 'tài sản cung cấp'} trung bình theo giờ của {asset} trong tháng {month} là bao nhiêu USD?"
            elif family=="asset_gap":
                sql=f"SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='{asset}' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','{asset}') AND hour=TIMESTAMPTZ '{month}-15 00:00:00+00'";q=f"Lúc 00:00 UTC ngày {month}-15, dư nợ USDC trừ dư nợ {asset} bằng bao nhiêu USD?"
            elif family=="quarter_change":
                sql=f"SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='{asset}' AND {_interval('hour','2026-01-01','2026-07-01')}";q=f"Dư nợ {asset} trung bình theo giờ quý II trừ quý I năm 2026 là bao nhiêu USD?"
            elif family=="peak_month_tx":
                start=["2025-01-01","2026-01-01","2025-07-01"][j];stop=["2026-01-01","2026-09-01","2026-07-01"][j]
                sql=f"SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE {_interval('time',start,stop)} GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1";q=f"Từ {start} đến trước {stop} UTC, tháng nào có nhiều giao dịch thanh lý nhất và có bao nhiêu giao dịch? Nếu bằng nhau chọn tháng sớm nhất.";unit="count"
            else:
                sql=f"SELECT sum(CASE WHEN time>=TIMESTAMPTZ '{month}-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '{month}-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE {_interval('time','2026-05-01',end)}";q=f"Tổng USD thanh lý tháng {month} trừ tổng USD từ 2026-05-01 đến trước {month}-01 UTC bằng bao nhiêu?"
            add("analysis",family,split,q,sql,unit)
    for family,split,key,concept in [("debt_explanation","dev","BORROW","Dư nợ là số dư tại thời điểm; không coi là tổng số tiền vay mới trong tháng."),("supply_explanation","dev","SUPPLY","Giá trị cung cấp là số dư, không phải lợi nhuận thu được."),("liquidation_explanation","test","LIQ","Số sự kiện không chứng minh mọi vị thế có health factor dưới 1 đều đã được thanh lý."),("transactions_explanation","test","LIQ","Một giao dịch có thể có nhiều sự kiện thanh lý; số đếm khác nhau không nhất thiết là lỗi dữ liệu."),("debt_change_explanation","test","BORROW","Biến động dư nợ USD không đủ kết luận nguyên nhân từ lãi vay hoặc hành vi người dùng."),("supply_risk_explanation","test","SUPPLY","Giá trị tài sản cung cấp không chứng minh tài sản đó không có rủi ro hoặc luôn rút được ngay.")]:
        for j,asset in enumerate(["USDC","WETH"]):
            when=["2026-08-15","2026-07-15"][j]
            if family in {"liquidation_explanation","transactions_explanation"}:
                expr="count(*)" if family=="liquidation_explanation" else "count(DISTINCT tx_hash)"
                month,stop=('2026-08','2026-09-01') if j==0 else ('2026-07','2026-08-01')
                sql=f"SELECT {expr} AS value FROM liquidation_events WHERE {_interval('time',month+'-01',stop)}";unit="count"
                q=f"Tháng {month} có bao nhiêu {'sự kiện' if family=='liquidation_explanation' else 'giao dịch'} thanh lý? Giải thích: {concept}"
            else:
                col="supplied_usd" if "supply" in family else "borrowed_usd";unit="USD"
                sql=f"SELECT {col} AS value FROM market_hourly WHERE asset='{asset}' AND hour=TIMESTAMPTZ '{when} 00:00:00+00'"
                explanation={
                    'debt_explanation':'Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?',
                    'supply_explanation':'Có thể coi đây là lợi nhuận người cung cấp đã thu được không? Vì sao?',
                    'debt_change_explanation':'Số liệu này có đủ chứng minh lãi vay là nguyên nhân làm tăng dư nợ không? Giải thích căn cứ.',
                    'supply_risk_explanation':'Số liệu này có chứng minh tài sản không có rủi ro và luôn rút ngay được không? Giải thích điều kiện.'
                }[family]
                q=f"{'Giá trị tài sản cung cấp' if col=='supplied_usd' else 'Dư nợ'} {asset} lúc 00:00 UTC {when} là bao nhiêu USD? {explanation}"
            add("mixed",family,split,q,sql,unit,concept,key)
    for family,split,questions,reason in [
        ("unavailable_fields","dev",["Phí gas tổng cộng của các giao dịch thanh lý tháng 8/2026 là bao nhiêu USD?","Lợi nhuận USD thực của người thanh lý tháng 8/2026 là bao nhiêu?"],"Gas/profit chưa được xác minh và bị loại khỏi dữ liệu thực nghiệm."),
        ("unverified_liquidation_asset","test",["Có bao nhiêu giao dịch thanh lý riêng USDC tháng 8/2026?","Tổng USD thanh lý riêng WETH tháng 7/2026 là bao nhiêu?"],"Chưa xác minh ánh xạ market sang tài sản thanh lý; không thể kết luận theo token."),
        ("unavailable_live_or_forecast","test",["Dư nợ USDC ngay bây giờ là bao nhiêu USD?","Dư nợ WETH tháng 12/2027 chắc chắn sẽ là bao nhiêu USD?"],"Bộ dữ liệu lịch sử cố định không cung cấp dữ liệu trực tiếp hoặc kết quả dự báo tương lai.")]:
        for q in questions:add("unanswerable",family,split,q,concept=reason,unanswerable=True)
    validate_benchmark(rows)
    return rows


def save_benchmark(rows,path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text("\n".join(json.dumps(r,ensure_ascii=False,default=str) for r in rows)+"\n",encoding="utf-8")


def load_benchmark(path):return [json.loads(s) for s in Path(path).read_text(encoding="utf-8").splitlines() if s.strip()]


def freeze_benchmark(path):
    path=Path(path);rows=load_benchmark(path);validate_benchmark(rows,final=True)
    for category,(dev,test) in CATEGORIES.items():
        if sum(r['category']==category and r['split']=='dev' for r in rows)!=dev or sum(r['category']==category and r['split']=='test' for r in rows)!=test:raise ValueError(f"Wrong benchmark distribution: {category}")
    manifest={"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),"frozen_at":datetime.now(timezone.utc).isoformat(),"records":len(rows)}
    path.with_suffix(".lock.json").write_text(json.dumps(manifest,indent=2),encoding="utf-8")
    return manifest
