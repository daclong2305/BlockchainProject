from copy import deepcopy
import pytest

from aave_analyst.llm import ScriptedLLM
from aave_analyst.pipeline import Analyst
from aave_analyst.retrieval import Retriever
from test_pipeline import fixture_db


DOC = {'id': 'DOC_LIQ_000', 'title': 'Health Factor & Liquidations',
       'url': 'https://aave.com/help/borrowing/liquidations', 'collected_at': '2026-09-15',
       'text': 'Health factor measures the safety of a borrow position. Below 1 a position is eligible for liquidation.'}


class RecordingLLM(ScriptedLLM):
    def __init__(self, responses):
        super().__init__(responses)
        self.payloads = []

    def complete(self, role, payload, timeout=60.):
        self.payloads.append((role, deepcopy(payload)))
        return super().complete(role, payload, timeout)


def test_false_health_factor_clarification_is_reviewed_and_documents_reach_answer(tmp_path):
    llm = RecordingLLM({
        'plan': [{'kind': 'unanswerable', 'clarification': 'Provide a wallet address'}],
        'plan_review': [{'kind': 'docs', 'metric': 'other', 'unit': 'other', 'retrieval_query': 'health factor', 'clarification': ''}],
        'answer': [{'answer': 'Health factor đo độ an toàn của vị thế vay [DOC_LIQ_000].', 'claims': []}],
    })
    draft = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).make_draft('Health factor là gì?')
    assert not draft.error
    assert draft.spec.kind == 'docs'
    assert not draft.refused
    assert not draft.sql
    assert draft.documents[0]['id'] == 'DOC_LIQ_000'
    assert [role for role, _ in llm.payloads] == ['plan', 'plan_review', 'answer']
    assert llm.payloads[-1][1]['documents'][0]['id'] == 'DOC_LIQ_000'
    assert draft.planning['initial']['clarification'] == 'Provide a wallet address'


def test_mixed_question_recovers_from_false_benchmark_refusal(tmp_path):
    question = 'Giải thích cơ chế thanh lý và cho biết số giao dịch thanh lý trong tháng 8 năm 2026.'
    llm = RecordingLLM({
        'plan': [{'kind': 'mixed', 'clarification': 'August is outside benchmark; split the question'}],
        'plan_review': [{'kind': 'mixed', 'metric': 'transactions', 'unit': 'count', 'aggregation': 'count_distinct',
                         'start': '2026-08-01T00:00:00Z', 'end': '2026-09-01T00:00:00Z', 'retrieval_query': 'liquidation health factor'}],
        'sql': [{'sql': "SELECT COUNT(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= '2026-08-01' AND time < '2026-09-01'"}],
        'answer': [{'answer': 'Giải thích [DOC_LIQ_000]. Có 1 giao dịch [SQL1].', 'claims': []}],
    })
    draft = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).make_draft(question)
    assert not draft.error
    assert draft.spec.kind == 'mixed'
    assert draft.query_result.rows == [{'value': 1}]
    answer_payload = llm.payloads[-1][1]
    assert answer_payload['documents']
    assert answer_payload['sql_result']['rows'] == [{'value': 1}]
    context = llm.payloads[0][1]
    assert 'benchmark_start' not in context['dictionary']['policy']
    assert context['availability']['market_hourly'][0]['asset'] == 'USDC'
    assert context['availability']['liquidation_events']['event_rows'] == 2
    assert context['document_evidence'][0]['id'] == 'DOC_LIQ_000'
    from aave_analyst.verification import evidence_payload
    evidence = evidence_payload(draft)
    assert evidence['availability'] == context['availability']
    assert evidence['retrieval_runs'][-1]['document_ids'] == [DOC['id']]
    assert 'benchmark_end' not in evidence['dictionary']['policy']


def test_inconsistent_metric_is_replanned_before_sql(tmp_path):
    llm = RecordingLLM({
        'plan': [{'kind': 'data', 'metric': 'liquidation_usd', 'unit': 'count', 'aggregation': 'count_distinct'}],
        'plan_review': [{'kind': 'data', 'metric': 'transactions', 'unit': 'count', 'aggregation': 'count_distinct'}],
        'sql': [{'sql': 'SELECT COUNT(DISTINCT tx_hash) AS value FROM liquidation_events'}],
        'answer': [{'answer': 'Có 1 giao dịch [SQL1].', 'claims': []}],
    })
    draft = Analyst(fixture_db(tmp_path), Retriever([]), llm).make_draft('Có bao nhiêu giao dịch thanh lý?')
    assert not draft.error
    assert draft.spec.metric == 'transactions'
    sql_payload = next(payload for role, payload in llm.payloads if role == 'sql')
    assert sql_payload['requirements']['metric'] == 'transactions'


def test_genuine_missing_year_is_preserved_and_review_is_bounded(tmp_path):
    clarification = {'kind': 'data', 'clarification': 'Bạn muốn hỏi tháng 8 năm nào?'}
    llm = RecordingLLM({'plan': [clarification], 'plan_review': [clarification]})
    draft = Analyst(fixture_db(tmp_path), Retriever([]), llm).make_draft('Có bao nhiêu giao dịch trong tháng 8?')
    assert not draft.error
    assert draft.spec.clarification == clarification['clarification']
    assert draft.refused
    assert not draft.sql
    assert len(llm.calls) == 2


def test_still_inconsistent_plan_does_not_execute_sql(tmp_path):
    bad = {'kind': 'data', 'metric': 'transactions', 'unit': 'USD', 'aggregation': 'sum'}
    llm = RecordingLLM({'plan': [bad], 'plan_review': [bad]})
    draft = Analyst(fixture_db(tmp_path), Retriever([]), llm).make_draft('Đếm giao dịch thanh lý')
    assert 'Invalid analysis' in draft.error
    assert not draft.sql
    assert len(llm.calls) == 2


def test_valid_docs_plan_does_not_need_extra_model_review(tmp_path):
    llm = RecordingLLM({'plan': [{'kind': 'docs', 'retrieval_query': 'health factor'}],
                        'answer': [{'answer': 'Định nghĩa [DOC_LIQ_000].', 'claims': []}]})
    draft = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).make_draft('Health factor là gì?')
    assert not draft.error
    assert [call['role'] for call in llm.calls] == ['plan', 'answer']
    assert 'availability' in llm.payloads[0][1]


@pytest.mark.parametrize('fields', [
    {'kind': []}, {'assets': 'USDC'}, {'retrieval_query': None},
    {'start': 'not-a-date'}, {'start': '2026-09-01', 'end': '2026-08-01'},
])
def test_invalid_plan_fields_are_detected_without_crashing(fields):
    from aave_analyst.models import QuerySpec
    from aave_analyst.planning import analysis_errors
    assert analysis_errors(QuerySpec(**fields))


def test_account_level_request_stays_unsupported_after_review(tmp_path):
    unsupported = {'kind': 'unanswerable', 'metric': 'other', 'clarification': ''}
    llm = RecordingLLM({'plan': [unsupported], 'plan_review': [unsupported],
                        'answer': [{'answer': 'Không có dữ liệu health factor của từng tài khoản.', 'refused': True, 'claims': []}]})
    draft = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).make_draft('Health factor của ví 0x123 hiện tại là bao nhiêu?')
    assert not draft.error
    assert draft.refused
    assert not draft.sql
    assert not draft.spec.clarification


def test_supported_concept_with_unsupported_account_value_uses_only_documents(tmp_path):
    llm = RecordingLLM({
        'plan': [{'kind': 'unanswerable', 'clarification': 'Provide your wallet'}],
        'plan_review': [{'kind': 'docs', 'metric': 'other', 'unit': 'other', 'retrieval_query': 'health factor'}],
        'answer': [{'answer': 'Health factor đo độ an toàn [DOC_LIQ_000]. Không có dữ liệu chỉ số hiện tại của ví.', 'claims': []}],
    })
    draft = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).make_draft('Giải thích health factor và cho biết chỉ số hiện tại của ví tôi.')
    assert not draft.error
    assert draft.documents
    assert not draft.sql
    assert all(role != 'sql' for role, _ in llm.payloads)
    assert 'chỉ số hiện tại của ví' in llm.payloads[-1][1]['question']


@pytest.mark.parametrize('start,end,expected', [
    ('2026-08-01T00:00:00Z', '2026-09-01T00:00:00Z', 'within_observed_bounds'),
    ('2026-09-16T00:00:00Z', '2026-10-01T00:00:00Z', 'after_last_observation'),
    ('2022-01-01', '2023-01-01', 'before_first_observation'),
    ('2026-09-01', '2026-10-01', 'overlaps_observed_bounds'),
    (None, None, 'unknown'),
])
def test_evidence_compares_requested_interval_with_observations(start, end, expected):
    from aave_analyst.models import Draft, QuerySpec
    from aave_analyst.verification import evidence_payload
    draft = Draft(question='q', spec=QuerySpec(start=start, end=end), planning={'availability': {
        'liquidation_events': {'first_event_utc': '2023-01-30T19:11:47+00:00',
                               'last_event_utc': '2026-09-15T05:53:59+00:00'}}})
    check = evidence_payload(draft)['interval_checks']['liquidation_events']
    assert check['relation'] == expected
    assert check['proves_complete_collection'] is False


def test_sql_review_receives_only_sql_sources_while_claim_review_keeps_documents(tmp_path):
    llm = RecordingLLM({
        'plan': [{'kind': 'mixed', 'metric': 'transactions', 'unit': 'count',
                  'aggregation': 'count_distinct', 'retrieval_query': 'health factor'}],
        'sql': [{'sql': 'SELECT COUNT(DISTINCT tx_hash) AS value FROM liquidation_events'}],
        'answer': [{'answer': 'Một giao dịch [SQL1]; định nghĩa [DOC_LIQ_000].', 'claims': [
            {'text': 'Một giao dịch', 'citations': ['SQL1'], 'numeric': {
                'value': 1, 'unit': 'count', 'evidence_id': 'SQL1', 'row': 0, 'column': 'value'}}]}],
        'sql_review': [{'issues': []}], 'claim_review': [{'issues': []}],
    })
    result = Analyst(fixture_db(tmp_path), Retriever([DOC]), llm).answer('Giải thích health factor và đếm giao dịch.')
    assert result.status == 'checks_passed'
    sql_payload = next(payload for role, payload in llm.payloads if role == 'sql_review')
    assert 'documents' not in sql_payload
    assert 'answer' not in sql_payload
    assert sql_payload['sql_result']['rows'] == [{'value': 1}]
    assert sql_payload['dictionary']['liquidation_events']['fields']['tx_hash']
    assert sql_payload['document_review']['handled_by'] == 'claim_review'
    assert sql_payload['document_review']['retrieved_ids'] == ['DOC_LIQ_000']
    claim_payload = next(payload for role, payload in llm.payloads if role == 'claim_review')
    assert claim_payload['documents'][0]['id'] == 'DOC_LIQ_000'
    assert claim_payload['documents'][0]['text'] == DOC['text']
    assert 'collected_at' not in claim_payload['documents'][0]
    assert result.draft.documents[0]['collected_at'] == '2026-09-15'
