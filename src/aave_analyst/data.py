from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,zipfile
import requests
import pandas as pd
from .database import build_database

RELEASE="data-2026-09-15"
DOWNLOAD=f"https://github.com/MSCA-DN-Digital-Finance/stablecoin-onchain-data/releases/download/{RELEASE}/aave_data.zip"
ASSETS=["DAI","USDC","USDT","USDe","WETH"]

DICTIONARY={
 "market_hourly":{"grain":"one asset per UTC hour","key":["asset","hour"],"fields":{"hour":"UTC grid timestamp, not necessarily a new on-chain observation","source_timestamp":"time of source observation","is_carried":"source observation already used at an earlier grid hour","source_age_hours":"age of observation at grid timestamp","supplied_usd":"USD stock at hour, never SUM over time","borrowed_usd":"USD debt stock at hour, never SUM over time","asset":"DAI, USDC, USDT, USDe or WETH"}},
 "liquidation_events":{"grain":"one liquidation event, not one transaction","key":["event_id"],"fields":{"tx_hash":"transaction identifier; COUNT(DISTINCT tx_hash) for transactions","event_id":"COUNT(*) for events after deduplication","amount_usd":"source-reported USD amount, SUM permitted over events","market":"unverified source market identifier; not a confirmed collateral/debt token mapping","time":"event time UTC"}},
 "policy":{"missing":"not zero","profitUSD":"excluded","gas_apr":"excluded pending verification","liquidation_asset_filter":"unsupported pending verified mapping","benchmark_start":"2025-01-01T00:00:00Z","benchmark_end_exclusive":"2026-09-01T00:00:00Z"}}


def download_data(root):
    root=Path(root);raw=root/"data/raw";raw.mkdir(parents=True,exist_ok=True)
    archive=raw/"aave_data.zip"
    if not archive.exists():
        response=requests.get(DOWNLOAD,timeout=(15,180),stream=True);response.raise_for_status()
        part=archive.with_suffix(".part")
        with part.open("wb") as f:
            for chunk in response.iter_content(1024*1024):f.write(chunk)
        part.replace(archive)
    with zipfile.ZipFile(archive) as z:
        for info in z.infolist():
            if not (raw/info.filename).resolve().is_relative_to(raw.resolve()):raise ValueError("Unsafe archive member")
        z.extractall(raw)
    sha=hashlib.sha256(archive.read_bytes()).hexdigest()
    (raw/"manifest.json").write_text(json.dumps({"release":RELEASE,"url":DOWNLOAD,"sha256":sha,"collected_at":datetime.now(timezone.utc).isoformat(),"redistribution":"Check upstream license before redistribution"},indent=2),encoding="utf-8")
    return raw/"data/AAVE"


def normalize_market(df,asset,source):
    if "__index_level_0__" not in df:
        if not isinstance(df.index,pd.DatetimeIndex):raise ValueError("Expected hourly datetime index")
        df=df.reset_index(names="__index_level_0__")
    else:df=df.reset_index(drop=True)
    hour=pd.to_datetime(df["__index_level_0__"],utc=True)
    source_time=pd.to_datetime(df["timestamp"],unit="s",utc=True)
    result=pd.DataFrame({"asset":asset,"hour":hour,"supplied_usd":pd.to_numeric(df.supplied_USD,errors="coerce"),"borrowed_usd":pd.to_numeric(df.borrowed_USD,errors="coerce"),"source_timestamp":source_time,"source_file":source})
    result=result.sort_values("hour").reset_index(drop=True)
    result["is_carried"]=result.source_timestamp.duplicated()
    result["source_age_hours"]=(result.hour-result.source_timestamp).dt.total_seconds()/3600
    if result.duplicated(["asset","hour"]).any():raise ValueError(f"Duplicate hours for {asset}")
    if (result.source_age_hours.dropna()<0).any():raise ValueError(f"Future observations for {asset}")
    return result


def prepare_data(root,source=None):
    root=Path(root);source=Path(source) if source else download_data(root)
    out=root/"data/processed";out.mkdir(parents=True,exist_ok=True)
    frames=[];audit=[]
    for asset in ASSETS:
        file=source/f"aave_v3_{asset.lower()}_eth.parquet"
        frame=normalize_market(pd.read_parquet(file),asset,str(file.relative_to(source)))
        frames.append(frame)
        subset=frame[(frame.hour>=pd.Timestamp("2025-01-01",tz="UTC"))&(frame.hour<pd.Timestamp("2026-09-01",tz="UTC"))]
        audit.append({"asset":asset,"rows":len(frame),"start":str(frame.hour.min()),"end":str(frame.hour.max()),"benchmark_rows":len(subset),"benchmark_start":str(subset.hour.min()),"benchmark_end":str(subset.hour.max()),"benchmark_missing_hours":len(pd.date_range("2025-01-01","2026-09-01",freq="h",inclusive="left",tz="UTC"))-len(subset),"missing_values":{k:int(v) for k,v in frame.isna().sum().items()},"carried_hours":int(frame.is_carried.sum())})
    file=source/"liquidations/aave_v3_eth_liquidation_events.parquet"
    df=pd.read_parquet(file)
    events=pd.DataFrame({"event_id":df.id.astype(str),"tx_hash":df.hash.astype(str),"time":pd.to_datetime(df.timestamp,unit="s",utc=True),"amount_usd":pd.to_numeric(df.amountUSD,errors="coerce"),"market":df.market.astype(str),"log_index":df.logIndex,"source_file":str(file.relative_to(source))})
    if events.event_id.duplicated().any() or events.duplicated(["tx_hash","log_index"]).any():raise ValueError("Duplicate liquidation event identifiers")
    markets=pd.concat(frames,ignore_index=True)
    markets.to_parquet(out/"market_hourly.parquet",index=False);events.to_parquet(out/"liquidation_events.parquet",index=False)
    build_database(markets,events,out/"aave.duckdb")
    subset=events[(events.time>=pd.Timestamp("2025-01-01",tz="UTC"))&(events.time<pd.Timestamp("2026-09-01",tz="UTC"))]
    report={"release":RELEASE,"market_rows":len(markets),"assets":audit,"liquidation_events":len(events),"liquidation_transactions":int(events.tx_hash.nunique()),"benchmark_liquidation_events":len(subset),"benchmark_liquidation_transactions":int(subset.tx_hash.nunique()),"excluded":["profitUSD","gas","APR","liquidation asset mapping"]}
    (out/"audit.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
    (out/"dictionary.json").write_text(json.dumps(DICTIONARY,indent=2,ensure_ascii=False),encoding="utf-8")
    return report
