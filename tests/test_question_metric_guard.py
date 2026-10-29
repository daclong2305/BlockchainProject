from aave_analyst.verification import semantic_rules


def test_original_debt_question_catches_wrong_plan_and_sql():
    issues=semantic_rules('SELECT avg(supplied_usd) FROM market_hourly',{'metric':'supplied_usd'},
                          question='Dư nợ USDC trung bình theo giờ là bao nhiêu USD?')
    assert any(issue.code=='question_metric' and issue.action=='sql' for issue in issues)


def test_original_supply_question_catches_wrong_debt_sql():
    issues=semantic_rules('SELECT max(borrowed_usd) FROM market_hourly',{'metric':'borrowed_usd'},
                          question='Giá trị tài sản cung cấp USDC lớn nhất là bao nhiêu USD?')
    assert any(issue.code=='question_metric' for issue in issues)


def test_multi_metric_and_negated_wording_do_not_force_single_metric():
    for question in ('So sánh dư nợ với giá trị tài sản cung cấp USDC.',
                     'Không hỏi dư nợ, hãy cho biết số giao dịch thanh lý.'):
        issues=semantic_rules('SELECT count(DISTINCT tx_hash) FROM liquidation_events',{'metric':'transactions'},question=question)
        assert not any(issue.code=='question_metric' for issue in issues)


def test_correct_debt_metric_and_legacy_calls_stay_valid():
    assert not semantic_rules('SELECT avg(borrowed_usd) FROM market_hourly',{'metric':'borrowed_usd'},question='Dư nợ USDC trung bình?')
    assert not semantic_rules('SELECT 1',{})


def test_correct_sql_is_not_rejected_for_wrong_extracted_metric_and_month_end():
    sql="SELECT avg(borrowed_usd) FROM market_hourly WHERE asset='USDC' AND hour>=TIMESTAMPTZ '2026-08-01' AND hour<TIMESTAMPTZ '2026-09-01'"
    wrong_plan={'metric':'supplied_usd','start':'2026-08-01T00:00:00Z','end':'2026-08-31T23:59:59Z'}
    assert not semantic_rules(sql,wrong_plan,question='Dư nợ USDC trung bình theo giờ tháng 8/2026 là bao nhiêu USD?')


def test_month_guard_handles_december_and_avoids_multi_interval_comparisons():
    from aave_analyst.intent_guards import question_anchors
    assert question_anchors('Dư nợ trong tháng 2025-12?')['end']=='2026-01-01'
    assert 'end' not in question_anchors('Dư nợ tháng 2026-08 trừ tháng 2026-07?')
    assert 'end' not in question_anchors('USD tháng 2026-08 trừ tổng từ 2026-05-01?')
    assert 'end' not in question_anchors('Dư nợ từ tháng 8/2026 đến tháng 9?')
    assert 'end' not in question_anchors('Dư nợ tháng 8/2026 đến 9/2026?')
