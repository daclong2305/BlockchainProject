# Independent human review

Do not read the other reviewer’s decisions. Verify the question, answer/SQL, source support, UTC scope and units independently.
The references below are MACHINE-GENERATED DRAFTS, not approved gold. If anything is wrong, use changes_requested and explain it; do not approve until corrected and reviewed again.
Fill your name and decisions in the companion JSON. This tool does not prove human identity and never supplies human labels.

## S001 · dev · metric

Dư nợ USDC trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_USDC_metric`

```json
{
  "id": "S001",
  "split": "dev",
  "family": "dev_USDC_metric",
  "error_type": "metric",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 2001158632.0983303
    }
  ]
}
```

## S002 · dev · aggregation

Dư nợ USDC trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_USDC_aggregation`

```json
{
  "id": "S002",
  "split": "dev",
  "family": "dev_USDC_aggregation",
  "error_type": "aggregation",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT sum(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 2001158632.0983303
    }
  ]
}
```

## S003 · dev · filter

Dư nợ USDC trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_USDC_filter`

```json
{
  "id": "S003",
  "split": "dev",
  "family": "dev_USDC_filter",
  "error_type": "filter",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 2001158632.0983303
    }
  ]
}
```

## S004 · dev · unit

Dư nợ USDC trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_USDC_unit`

```json
{
  "id": "S004",
  "split": "dev",
  "family": "dev_USDC_unit",
  "error_type": "unit",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(borrowed_usd)/1000000 AS value FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 2001158632.0983303
    }
  ]
}
```

## S005 · dev · join

Dư nợ USDC lúc 00:00 UTC 2026-08-01 là bao nhiêu USD?

Family: `dev_USDC_join`

```json
{
  "id": "S005",
  "split": "dev",
  "family": "dev_USDC_join",
  "error_type": "join",
  "correct_sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-01'",
  "wrong_sql": "SELECT sum(m.borrowed_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.asset=n.asset WHERE m.asset='USDC' AND m.hour=TIMESTAMPTZ '2026-08-01' AND n.hour>=TIMESTAMPTZ '2026-08-01' AND n.hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 1940447808.541687
    }
  ]
}
```

## S006 · dev · metric

Dư nợ WETH trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_WETH_metric`

```json
{
  "id": "S006",
  "split": "dev",
  "family": "dev_WETH_metric",
  "error_type": "metric",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 3667108875.975095
    }
  ]
}
```

## S007 · dev · aggregation

Dư nợ WETH trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_WETH_aggregation`

```json
{
  "id": "S007",
  "split": "dev",
  "family": "dev_WETH_aggregation",
  "error_type": "aggregation",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT sum(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 3667108875.975095
    }
  ]
}
```

## S008 · dev · filter

Dư nợ WETH trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_WETH_filter`

```json
{
  "id": "S008",
  "split": "dev",
  "family": "dev_WETH_filter",
  "error_type": "filter",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 3667108875.975095
    }
  ]
}
```

## S009 · dev · unit

Dư nợ WETH trung bình theo giờ tháng 8/2026 là bao nhiêu USD?

Family: `dev_WETH_unit`

```json
{
  "id": "S009",
  "split": "dev",
  "family": "dev_WETH_unit",
  "error_type": "unit",
  "correct_sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "wrong_sql": "SELECT avg(borrowed_usd)/1000000 AS value FROM market_hourly WHERE asset='WETH' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 3667108875.975095
    }
  ]
}
```

## S010 · dev · join

Dư nợ WETH lúc 00:00 UTC 2026-08-01 là bao nhiêu USD?

Family: `dev_WETH_join`

```json
{
  "id": "S010",
  "split": "dev",
  "family": "dev_WETH_join",
  "error_type": "join",
  "correct_sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-08-01'",
  "wrong_sql": "SELECT sum(m.borrowed_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.asset=n.asset WHERE m.asset='WETH' AND m.hour=TIMESTAMPTZ '2026-08-01' AND n.hour>=TIMESTAMPTZ '2026-08-01' AND n.hour<TIMESTAMPTZ '2026-09-01'",
  "reference_rows": [
    {
      "value": 3224504248.285001
    }
  ]
}
```

## S011 · test · metric

Giá trị tài sản cung cấp USDT lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_USDT_metric`

```json
{
  "id": "S011",
  "split": "test",
  "family": "test_USDT_metric",
  "error_type": "metric",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 8543331357.753431
    }
  ]
}
```

## S012 · test · aggregation

Giá trị tài sản cung cấp USDT lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_USDT_aggregation`

```json
{
  "id": "S012",
  "split": "test",
  "family": "test_USDT_aggregation",
  "error_type": "aggregation",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT sum(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 8543331357.753431
    }
  ]
}
```

## S013 · test · filter

Giá trị tài sản cung cấp USDT lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_USDT_filter`

```json
{
  "id": "S013",
  "split": "test",
  "family": "test_USDT_filter",
  "error_type": "filter",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 8543331357.753431
    }
  ]
}
```

## S014 · test · unit

Giá trị tài sản cung cấp USDT lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_USDT_unit`

```json
{
  "id": "S014",
  "split": "test",
  "family": "test_USDT_unit",
  "error_type": "unit",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(supplied_usd)/1000000 AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 8543331357.753431
    }
  ]
}
```

## S015 · test · join

Khoảng cách giữa giá trị tài sản cung cấp USDT lớn nhất và nhỏ nhất trong năm 2025 là bao nhiêu USD?

Family: `test_USDT_join`

```json
{
  "id": "S015",
  "split": "test",
  "family": "test_USDT_join",
  "error_type": "join",
  "correct_sql": "SELECT max(supplied_usd)-min(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(m.supplied_usd)-min(n.supplied_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.hour=n.hour WHERE m.asset='USDT' AND n.asset='USDe' AND m.hour>=TIMESTAMPTZ '2025-01-01' AND m.hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 6110198977.972517
    }
  ]
}
```

## S016 · test · metric

Giá trị tài sản cung cấp DAI lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_DAI_metric`

```json
{
  "id": "S016",
  "split": "test",
  "family": "test_DAI_metric",
  "error_type": "metric",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 190574906.70241314
    }
  ]
}
```

## S017 · test · aggregation

Giá trị tài sản cung cấp DAI lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_DAI_aggregation`

```json
{
  "id": "S017",
  "split": "test",
  "family": "test_DAI_aggregation",
  "error_type": "aggregation",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT sum(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 190574906.70241314
    }
  ]
}
```

## S018 · test · filter

Giá trị tài sản cung cấp DAI lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_DAI_filter`

```json
{
  "id": "S018",
  "split": "test",
  "family": "test_DAI_filter",
  "error_type": "filter",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 190574906.70241314
    }
  ]
}
```

## S019 · test · unit

Giá trị tài sản cung cấp DAI lớn nhất trong các quan sát giờ năm 2025 là bao nhiêu USD?

Family: `test_DAI_unit`

```json
{
  "id": "S019",
  "split": "test",
  "family": "test_DAI_unit",
  "error_type": "unit",
  "correct_sql": "SELECT max(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(supplied_usd)/1000000 AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 190574906.70241314
    }
  ]
}
```

## S020 · test · join

Khoảng cách giữa giá trị tài sản cung cấp DAI lớn nhất và nhỏ nhất trong năm 2025 là bao nhiêu USD?

Family: `test_DAI_join`

```json
{
  "id": "S020",
  "split": "test",
  "family": "test_DAI_join",
  "error_type": "join",
  "correct_sql": "SELECT max(supplied_usd)-min(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour>=TIMESTAMPTZ '2025-01-01' AND hour<TIMESTAMPTZ '2026-01-01'",
  "wrong_sql": "SELECT max(m.supplied_usd)-min(n.supplied_usd) AS value FROM market_hourly m JOIN market_hourly n ON m.hour=n.hour WHERE m.asset='DAI' AND n.asset='USDe' AND m.hour>=TIMESTAMPTZ '2025-01-01' AND m.hour<TIMESTAMPTZ '2026-01-01'",
  "reference_rows": [
    {
      "value": 39288476.32574871
    }
  ]
}
```
