from datetime import datetime, timezone
import pandas as pd
import pytest


def test_counts_deduplicate_transactions_and_preserve_events(tmp_path):
    from aave_analyst.database import Database, build_database
    markets = pd.DataFrame([dict(asset="USDC", hour="2026-08-01T00:00:00Z", supplied_usd=100., borrowed_usd=40., source_timestamp="2026-08-01T00:00:00Z", is_carried=False)])
    events = pd.DataFrame([dict(event_id=f"e{i}", tx_hash="0x1", time="2026-08-01T00:00:00Z", amount_usd=10., market="x", log_index=i) for i in range(2)])
    path = tmp_path / "aave.duckdb"
    build_database(markets, events, path)
    db = Database(path)
    assert db.query("SELECT count(*) AS events, count(DISTINCT tx_hash) AS transactions FROM liquidation_events").rows == [{"events": 2, "transactions": 1}]


@pytest.mark.parametrize("sql", ["DROP TABLE market_hourly", "SELECT * FROM read_csv('secret.csv')", "SELECT 1; SELECT 2", "COPY (SELECT 1) TO 'leak.csv'", "SELECT * FROM duckdb_settings()", "SELECT * FROM unknown", "ATTACH 'x' AS y"])
def test_query_guard_rejects_unsafe_sql(sql):
    from aave_analyst.database import validate_sql
    with pytest.raises(ValueError):
        validate_sql(sql)


def test_query_guard_accepts_readonly_cte():
    from aave_analyst.database import validate_sql
    validate_sql("WITH t AS (SELECT tx_hash FROM liquidation_events) SELECT count(DISTINCT tx_hash) FROM t")


def test_normalization_retains_source_age_and_utc():
    from aave_analyst.data import normalize_market
    frame = pd.DataFrame({"__index_level_0__": pd.to_datetime(["2026-08-01T07:00:00+07:00", "2026-08-01T08:00:00+07:00"]), "timestamp": [1785542400,1785542400], "supplied_USD": [100.,100.], "borrowed_USD": [40.,40.]})
    result = normalize_market(frame, "USDC", "source.parquet")
    assert str(result.hour.iloc[0]) == "2026-08-01 00:00:00+00:00"
    assert result.is_carried.tolist() == [False, True]


def test_parquet_datetime_index_is_supported():
    from aave_analyst.data import normalize_market
    frame=pd.DataFrame({"timestamp":[1785542400],"supplied_USD":[100.],"borrowed_USD":[40.]},index=pd.to_datetime(["2026-08-01T00:00:00Z"]))
    result=normalize_market(frame,"USDC","source.parquet")
    assert len(result)==1
    assert result.borrowed_usd.iloc[0]==40.


def test_semantic_rules_reject_stock_sum_and_wrong_count():
    from aave_analyst.verification import semantic_rules
    spec = {"metric":"borrowed_usd", "aggregation":"average", "assets":["USDC"], "start":"2026-08-01", "end":"2026-09-01", "unit":"USD"}
    issues = semantic_rules("SELECT sum(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour >= '2026-08-01' AND hour < '2026-09-01'", spec)
    assert any(i.code == "stock_sum" for i in issues)
    issues = semantic_rules("SELECT count(*) AS value FROM liquidation_events", {"metric":"transactions", "aggregation":"count_distinct", "assets":[]})
    assert any(i.code == "transaction_count" for i in issues)
