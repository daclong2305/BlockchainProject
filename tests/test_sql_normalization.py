import pytest
from aave_analyst.sql_normalization import normalize_datetime_quotes
from test_pipeline import fixture_db


def test_quoted_iso_dates_execute_without_changing_count_or_interval(tmp_path):
    raw = 'SELECT COUNT(DISTINCT tx_hash) AS value FROM liquidation_events WHERE "time" >= "2026-08-01T00:00:00Z" AND "time" < "2026-09-01T00:00:00Z"'
    sql, changes = normalize_datetime_quotes(raw)
    assert len(changes) == 2
    assert 'COUNT(DISTINCT tx_hash)' in sql
    assert fixture_db(tmp_path).query(sql).rows == [{'value': 1}]
    assert normalize_datetime_quotes(sql) == (sql, [])


@pytest.mark.parametrize('sql', [
    'SELECT "2026-08-01" FROM liquidation_events',
    'SELECT * FROM market_hourly WHERE asset = "2026-08-01"',
    'SELECT * FROM market_hourly WHERE hour >= "not_a_date"',
    'SELECT * FROM market_hourly WHERE hour >= "2026-02-30"',
    'WITH t("2026-08-01", time) AS (SELECT time, time FROM liquidation_events) SELECT * FROM t WHERE time >= "2026-08-01"',
    'SELECT time AS "2026-08-01" FROM liquidation_events WHERE time >= "2026-08-01"',
    "SELECT * FROM read_csv('secret.csv') WHERE hour >= \"2026-08-01\"",
])
def test_only_valid_datetime_operands_are_normalized(sql):
    assert normalize_datetime_quotes(sql) == (sql, [])
