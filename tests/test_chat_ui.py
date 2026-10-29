from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from aave_analyst.models import Draft, QuerySpec, QueryResult, RunResult, Issue


@pytest.fixture
def chat(monkeypatch, tmp_path):
    import aave_analyst.cli
    import aave_analyst.config

    for name in ('data/processed/aave.duckdb', 'data/documents/chunks.json'):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch()
    monkeypatch.setattr(aave_analyst.config, 'read_settings', lambda: {'AAVE_PROJECT_ROOT': str(tmp_path)})

    class Analyst:
        def answer(self, question, mode):
            if question == 'simulate failure':
                raise RuntimeError('Test service unavailable')
            draft = Draft(question=question, spec=QuerySpec(kind='data'),
                          answer=f'Phản hồi: {question} [SQL1]', sql='SELECT 107 AS value',
                          query_result=QueryResult(['value'], [{'value': 107}]))
            if question == 'unverified answer':
                return RunResult(mode, draft, 'unverified', issues=[Issue('metric_unit_mismatch', 'Internal diagnostic', 'answer')], elapsed=1.2)
            return RunResult(mode, draft, 'checks_passed', elapsed=1.2)

    monkeypatch.setattr(aave_analyst.cli, 'analyst_at', lambda root, **kwargs: Analyst())
    return AppTest.from_file(str(Path(__file__).resolve().parents[1] / 'app.py')).run(timeout=15)


def test_chat_keeps_history_and_message_evidence(chat):
    assert not chat.exception
    chat.chat_input[0].set_value('Câu hỏi thứ nhất').run()
    chat.chat_input[0].set_value('Câu hỏi thứ hai').run()
    assert not chat.exception
    assert len(chat.chat_message) == 4
    assert 'Câu hỏi thứ nhất' in chat.chat_message[1].markdown[0].value
    assert 'Câu hỏi thứ hai' in chat.chat_message[3].markdown[0].value
    assert len(chat.dataframe) == 2
    assert len(chat.code) == 2


def test_new_chat_clears_messages(chat):
    chat.chat_input[0].set_value('Một câu hỏi').run()
    chat.button(key='new_chat').click().run()
    assert not chat.exception
    assert len(chat.chat_message) == 0
    assert len(chat.session_state['messages']) == 0


def test_suggested_question_submits_a_chat_turn(chat):
    chat.button(key='suggestion_0').click().run()
    assert not chat.exception
    assert len(chat.chat_message) == 2
    assert 'thanh lý' in chat.chat_message[0].markdown[0].value


@pytest.mark.parametrize('index', range(4))
def test_starter_opens_conversation_before_backend_call(chat, monkeypatch, index):
    """The starter screen must be gone while a slow request is processing."""
    import aave_analyst.cli
    from streamlit.runtime.scriptrunner import get_script_run_ctx

    original_factory = aave_analyst.cli.analyst_at  # fixture's fake, never the real analyst
    observed = []

    class ObservedAnalyst:
        def answer(self, question, mode):
            ctx = get_script_run_ctx()
            # AppTest finishes only after answer(); inspect the actual widget set
            # at call time to catch the entry-screen/loading regression.
            observed.append(any(f'suggestion_{i}' in ctx.shared.widget_user_keys_this_run for i in range(4)))
            return original_factory(None).answer(question, mode)

    monkeypatch.setattr(aave_analyst.cli, 'analyst_at', lambda root, **kwargs: ObservedAnalyst())
    chat.button(key=f'suggestion_{index}').click().run()
    assert not chat.exception
    assert observed == [False]
    assert len(chat.chat_message) == 2
    assert len(chat.session_state['messages']) == 2
    chat.run()
    assert observed == [False]  # repainting must not send the question twice


def test_service_error_is_visible_and_next_question_still_works(chat):
    chat.chat_input[0].set_value('simulate failure').run()
    assert not chat.exception
    assert any('Test service unavailable' in item.value for item in chat.error)
    chat.chat_input[0].set_value('Thử lại').run()
    assert not chat.exception
    assert len(chat.chat_message) == 4
    assert 'Thử lại' in chat.chat_message[-1].markdown[0].value


def test_unverified_answer_explains_metric_mismatch_in_vietnamese(chat):
    chat.chat_input[0].set_value('unverified answer').run()
    assert not chat.exception
    assert len(chat.warning) == 1
    assert len(chat.success) == 0
    text = '\n'.join(item.value for item in chat.markdown)
    assert 'Chỉ số và đơn vị chưa nhất quán' in text


def test_verification_warnings_are_separate_from_answer_and_preserve_record(chat):
    from copy import deepcopy

    answer = 'Trong bộ dữ liệu hiện có, có 107 giao dịch thanh lý [SQL1].'
    issues = [
        {'code': 'metric_unit_mismatch', 'message': 'Metric diagnostic; keep both clauses.', 'action': 'answer'},
        {'code': 'new_reviewer_code', 'message': 'Documents DOC_BORROW_* do not support the claim.', 'action': 'answer'},
    ]
    result = {'mode': 'P', 'status': 'unverified', 'elapsed': 1, 'repairs': 2,
              'issues': issues, 'trace': [], 'draft': {
                  'answer': answer + '\n\nChưa thể xác minh đầy đủ: ' + '; '.join(i['message'] for i in issues),
                  'spec': {}, 'claims': [], 'documents': []}}
    original = deepcopy(result)
    chat.session_state['messages'] = [{'role': 'assistant', 'result': result}]
    chat.run()

    assert not chat.exception
    assert chat.chat_message[0].markdown[0].value == answer
    assert len(chat.warning) == 1
    assert '2 điểm cần kiểm tra' in chat.warning[0].value
    text = '\n'.join(item.value for item in chat.markdown)
    assert '1. Chỉ số và đơn vị chưa nhất quán' in text
    assert '2. Điểm cần kiểm tra' in text
    assert [item.value for item in chat.text] == [issue['message'] for issue in issues]
    assert any(item.label == 'Thông báo kỹ thuật' and not item.proto.expanded for item in chat.expander)
    assert chat.session_state['messages'][0]['result'] == original


def test_warning_like_answer_text_is_not_removed_without_matching_diagnostics(chat):
    answer = 'Giải thích cảnh báo.\n\nChưa thể xác minh đầy đủ: nội dung thuộc câu trả lời.'
    result = {'mode': 'P', 'status': 'unverified', 'elapsed': 1, 'repairs': 0,
              'issues': [{'code': 'other', 'message': 'A different diagnostic', 'action': 'answer'}],
              'trace': [], 'draft': {'answer': answer, 'spec': {}, 'claims': [], 'documents': []}}
    chat.session_state['messages'] = [{'role': 'assistant', 'result': result}]
    chat.run()
    assert not chat.exception
    assert chat.chat_message[0].markdown[0].value == answer


def test_switching_mode_updates_help_without_resubmitting_question(chat):
    chat.chat_input[0].set_value('Một câu hỏi').run()
    chat.selectbox(key='analysis_mode').select('B0').run()
    assert not chat.exception
    assert len(chat.chat_message) == 2
    assert any('không chạy bộ kiểm chứng' in item.value for item in chat.caption)


def test_research_desk_exposes_evidence_beside_recorded_answer(chat, monkeypatch):
    import aave_analyst.cli
    from copy import deepcopy
    chat.chat_input[0].set_value('Một câu hỏi').run()
    before = deepcopy(chat.session_state['messages'])
    monkeypatch.setattr(aave_analyst.cli, 'analyst_at', lambda root, **kwargs: pytest.fail('UI rerun must not call analyst'))
    chat.selectbox(key='analysis_mode').select('B0').run()
    assert not chat.exception
    assert [tab.label for tab in chat.tabs] == ['Dữ liệu & SQL', 'Tài liệu', 'Dẫn chứng']
    assert chat.session_state['messages'] == before
    assert any('P ·' in item.value for item in chat.caption)


@pytest.mark.parametrize('claims', [None, ['bad claim'], [{'text': 'claim', 'citations': 4, 'numeric': 7}]])
def test_malformed_recorded_claims_do_not_break_history(chat, claims):
    result = {'mode': 'P', 'status': 'error', 'error': 'Recorded service error',
              'elapsed': 1, 'repairs': 0, 'issues': [], 'trace': [], 'draft': {
                  'answer': 'Recorded answer', 'spec': {}, 'claims': claims, 'documents': []}}
    chat.session_state['messages'] = [{'role': 'assistant', 'result': result}]
    chat.run()
    assert not chat.exception
    assert any('Recorded service error' in item.value for item in chat.error)
    assert any('định dạng' in item.value for item in chat.caption)
    assert chat.session_state['messages'][0]['result'] == result
    assert not chat.success


def test_scope_truncation_and_claim_reference_are_truthful(chat):
    result = {'mode': 'P', 'status': 'unverified', 'elapsed': 1, 'repairs': 1,
              'issues': [], 'trace': [{'event': 'repair', 'repair': 1}], 'draft': {
                  'answer': 'Recorded answer [SQL1]', 'sql': 'SELECT 0 AS value',
                  'spec': {'assets': ['USDC'], 'start': '2026-08-01', 'end': '2026-09-01', 'unit': 'count'},
                  'query_result': {'columns': ['value'], 'rows': [{'value': 0}], 'truncated': True, 'total_rows': 201},
                  'documents': [], 'claims': [{'text': 'Recorded zero', 'citations': ['SQL1'],
                      'numeric': {'evidence_id': 'SQL1', 'row': 0, 'column': 'value', 'value': 0}}]}}
    chat.session_state['messages'] = [{'role': 'assistant', 'result': result}]
    chat.run()
    assert not chat.exception and not chat.success
    text = '\n'.join(item.value for item in chat.caption)
    assert 'USDC' in text and '2026-08-01' in text and '2026-09-01' in text
    assert '1 dòng hiển thị' in text and '201 dòng' not in text
    assert 'SQL1' in text and 'cột value' in text
    assert any('Vòng sửa 1' in item.value for item in chat.markdown)
    assert chat.dataframe[0].value.iloc[0]['value'] == 0
    assert any('giới hạn' in item.value for item in chat.warning)


def test_empty_query_is_explicit_and_has_no_false_verified_label(chat):
    chat.session_state['messages'] = [{'role': 'assistant', 'result': {
        'mode': 'B0', 'status': 'unchecked', 'elapsed': 0, 'repairs': 0,
        'issues': [], 'trace': [], 'draft': {'answer': '', 'spec': {},
            'sql': 'SELECT 1 WHERE FALSE', 'claims': [], 'documents': [],
            'query_result': {'columns': ['value'], 'rows': [], 'truncated': False}}}}]
    chat.run()
    assert not chat.exception and not chat.success
    assert any('không trả về dòng' in item.value for item in chat.info)


def test_missing_file_disables_question_and_starters(chat, tmp_path, monkeypatch):
    missing = tmp_path / 'data/documents/chunks.json'
    original_exists = Path.exists
    monkeypatch.setattr(Path, 'exists', lambda path: False if path == missing else original_exists(path))
    chat.run()
    assert not chat.exception
    assert chat.chat_input[0].disabled
    assert all(chat.button(key=f'suggestion_{i}').disabled for i in range(4))


def test_source_attribution_reads_fixture_manifest(chat, tmp_path):
    import json
    path = tmp_path / 'data/raw/manifest.json'
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({'release': 'fixture-release', 'collected_at': 'fixture-date'}), encoding='utf-8')
    chat.chat_input[0].set_value('Một câu hỏi').run()
    assert not chat.exception
    text = '\n'.join(item.value for item in chat.caption)
    assert 'fixture-release' in text and 'fixture-date' in text
    assert 'không phải snapshot' in text


@pytest.mark.parametrize('sql', [12, ['SELECT 1']])
def test_non_string_sql_in_error_result_does_not_block_history(chat, sql):
    result = {'mode': 'P', 'status': 'error', 'error': 'Recorded SQL error',
              'elapsed': 1, 'repairs': 0, 'issues': [], 'trace': [], 'draft': {
                  'answer': 'Recorded answer', 'spec': {}, 'sql': sql, 'claims': [], 'documents': []}}
    chat.session_state['messages'] = [{'role': 'assistant', 'result': result}]
    chat.run()
    assert not chat.exception
    assert any('Recorded SQL error' in item.value for item in chat.error)
    assert chat.session_state['messages'][0]['result'] == result
    assert chat.code[0].value == str(sql)
