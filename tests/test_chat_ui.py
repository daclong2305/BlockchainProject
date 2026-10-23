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

    monkeypatch.setattr(aave_analyst.cli, 'analyst_at', lambda root: Analyst())
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


def test_switching_mode_updates_help_without_resubmitting_question(chat):
    chat.chat_input[0].set_value('Một câu hỏi').run()
    chat.selectbox(key='analysis_mode').select('B0').run()
    assert not chat.exception
    assert len(chat.chat_message) == 2
    assert any('không chạy bộ kiểm chứng' in item.value for item in chat.caption)
