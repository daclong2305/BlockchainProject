from copy import deepcopy

import pytest

from aave_analyst.models import Draft, QueryResult, QuerySpec
from aave_analyst.verification import evidence_payload, response_issues, semantic_rules


def test_observations_do_not_trigger_repair_or_erase_real_findings():
    raw = {'issues': [
        {'code': 'CLAIM_SUPPORTED', 'message': 'Supported by D1', 'action': 'answer'},
        {'code': 'COMPLETE_ANSWER', 'message': 'Answers the question', 'action': 'answer'},
        {'code': 'ANSWER_COMPLETE', 'message': 'Sufficient answer', 'action': 'answer'},
        {'code': 'CITATION_VALID', 'message': 'The linked document supports the claim'},
        {'kind': 'confirmation', 'code': 'definition_ok', 'message': 'Definition supported'},
        {'kind': 'defect', 'code': 'unsupported_claim', 'message': 'Second claim lacks evidence', 'action': 'retrieve'},
    ]}
    assert [i.code for i in response_issues(raw)] == ['unsupported_claim']


def make_draft():
    spec = QuerySpec(kind='data', assets=['USDe'], start='2026-08-01', end='2026-09-01',
                     metric='supplied_usd', aggregation='average', unit='USD')
    return Draft(question='Giá trị tài sản cung cấp USDe tháng 8/2026?', spec=spec,
                 sql="select avg(supplied_usd) as v from market_hourly where asset='USDe'",
                 query_result=QueryResult(['v'], [{'v': 749295298.141774}]),
                 claims=[{'text': '749295298.14 USD', 'citations': ['SQL1'], 'numeric': {
                     'row': 0, 'column': 'v', 'value': 749295298.14, 'unit': 'USD', 'evidence_id': 'SQL1'}}],
                 planning={'availability': {'market_hourly': [
                     {'asset': 'USDC', 'start_utc': '2025-01-01', 'end_utc': '2025-08-01'},
                     {'asset': 'USDe', 'start_utc': '2024-06-06', 'end_utc': '2026-09-15T14:00:00+07:00'}]}})


@pytest.mark.parametrize('start,end,expected', [
    ('2026-08-01', '2026-09-01', 'within_observed_bounds'),
    ('2026-09-15T07:00:00Z', '2026-09-15T08:00:00Z', 'within_observed_bounds'),
    ('2026-09-01', '2026-10-01', 'overlaps_observed_bounds'),
    ('2026-10-01', '2026-11-01', 'after_last_observation'),
])
def test_market_interval_uses_requested_asset_and_half_open_hours(start, end, expected):
    draft = make_draft()
    draft.spec.start, draft.spec.end = start, end
    checks = evidence_payload(draft, specialist=True)['interval_checks']['market_hourly']
    assert 'market_hourly' not in evidence_payload(draft)['interval_checks']
    assert list(checks) == ['USDe']
    assert checks['USDe'] == {'relation': expected, 'proves_complete_collection': False}


def test_numeric_evidence_identifies_result_cell_and_wrong_asset_sql():
    draft = make_draft()
    facts = evidence_payload(draft, specialist=True)['numeric_evidence']
    assert facts == [{'claim_index': 0, 'evidence_id': 'SQL1', 'row': 0, 'column': 'v',
                      'cell_value': 749295298.141774}]
    wrong = deepcopy(draft)
    wrong.sql = "select 'USDe' as label, avg(supplied_usd) as v from market_hourly where asset='WETH'"
    assert 'asset_filter' in {i.code for i in semantic_rules(wrong.sql, vars(wrong.spec), wrong.question)}
    draft.claims[0]['numeric']['row'] = -1
    assert not evidence_payload(draft, specialist=True)['numeric_evidence']


def test_market_coverage_measures_slots_per_asset_and_detects_an_actual_gap(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.verification import coverage_rules
    draft = make_draft()
    draft.spec.assets = ['USDC', 'DAI']
    draft.spec.start, draft.spec.end = '2026-08-01T00:00Z', '2026-08-01T01:00Z'
    db = fixture_db(tmp_path)
    issues = coverage_rules(db, draft.spec, draft=draft)
    assert len(db.calls) == 1
    assert [issue.code for issue in issues] == ['coverage']
    sample = evidence_payload(draft, specialist=True)['market_sample']
    assert sample['assets']['USDC']['one_row_per_hour'] is True
    assert sample['assets']['DAI']['observed_slots'] == 0
    assert sample['assets']['DAI']['one_row_per_hour'] is False
    draft.spec.end = '2026-08-01T02:00Z'
    coverage_rules(db, draft.spec, draft=draft)
    assert not draft.planning['market_sample']['assets']['USDC']['one_row_per_hour']


def test_specialist_findings_respect_sql_evidence_and_observed_hours():
    from aave_analyst.verification import specialist_findings

    draft = make_draft()
    draft.planning['market_sample'] = {'assets': {'USDe': {'one_row_per_hour': True}}}
    review = {'issues': [
        {'code': 'future_interval', 'message': 'The requested period is in the future', 'action': 'stop'},
        {'code': 'no_supporting_documents', 'message': 'No documents present for the value', 'action': 'retrieve'},
        {'code': 'unsupported_claim', 'message': 'A separate statement is unsupported', 'action': 'answer'},
    ]}
    assert [issue.code for issue in specialist_findings(draft, review)] == ['unsupported_claim']

    draft.spec.kind = 'mixed'
    draft.planning['market_sample']['assets']['USDe']['one_row_per_hour'] = False
    assert [issue.code for issue in specialist_findings(draft, review)] == [
        'future_interval', 'no_supporting_documents', 'unsupported_claim',
    ]
