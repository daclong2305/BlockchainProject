from aave_analyst.benchmark import question_scope


def test_scope_exposes_real_predicates_not_entire_benchmark_window():
    sql="SELECT avg(borrowed_usd) FROM market_hourly WHERE asset='USDC' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'"
    scope=question_scope('USDC in August?',sql,'avg_debt','USD')
    assert scope['assets']==['USDC']
    assert scope['gold_time_literals']==['2026-08-01','2026-09-01']
    assert '2026-08-01' in scope['gold_where_predicates'][0]
    assert scope['benchmark_window']['start']=='2025-01-01'
    assert 'start' not in scope


def test_scope_unsupported_request_does_not_invent_sql_interval():
    scope=question_scope('USDC wallet health factor?', '', 'wallet_hf','USD')
    assert scope['assets']==['USDC'] and scope['gold_time_literals']==[]
    assert scope['gold_where_predicates']==[]
