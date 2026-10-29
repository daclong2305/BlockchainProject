from pathlib import Path
import json
import pytest
from aave_analyst.models import Draft, QuerySpec, RunResult
from aave_analyst.comparison import run_comparison
from test_chat_ui import chat


def test_models_overlap_and_progress_stays_on_caller_thread(tmp_path,monkeypatch):
    import threading
    import aave_analyst.comparison as module
    for name in ('data/processed/aave.duckdb','data/processed/dictionary.json','data/documents/chunks.json'):
        path=tmp_path/name;path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('[]' if name.endswith('chunks.json') else '{}')
    barrier=threading.Barrier(2)
    caller=threading.get_ident();events=[]
    class LLM:
        def __init__(self):self.calls=[]
        def config(self):return {'model_id':'fixture'}
    class Fake:
        def __init__(self,db,retriever,llm,deadline):pass
        def answer(self,question,mode):
            barrier.wait(timeout=3)  # Sequential execution cannot pass this barrier.
            self.progress({'event':'call_started','role':'answer','remaining_seconds':100})
            return RunResult(mode,Draft(question=question,spec=QuerySpec(),answer='fixture'),'unchecked')
    monkeypatch.setattr(module,'LocalQwenLLM',LLM)
    monkeypatch.setattr(module,'BedrockLLM',LLM)
    monkeypatch.setattr(module,'Analyst',Fake)
    def progress(event):
        assert threading.get_ident()==caller
        events.append(event)
    result=run_comparison(tmp_path,'q','B0',progress=progress)
    assert all('result' in item for item in result['results'].values())
    assert {event['provider'] for event in events}=={'local_qwen','bedrock'}
    assert len([event for event in events if event['event']=='model_finished'])==2


@pytest.mark.parametrize('deadline', [0, -1, float('inf'), float('nan')])
def test_invalid_comparison_deadline_is_rejected_before_running(tmp_path, deadline):
    with pytest.raises(ValueError, match='finite positive'):
        run_comparison(tmp_path, 'Question', 'P', deadline=deadline)


@pytest.mark.parametrize('change_source', [True, False])
def test_comparison_isolates_model_failure_and_tracks_snapshot(tmp_path, monkeypatch, change_source):
    import aave_analyst.comparison as module
    for name, content in [('data/processed/aave.duckdb', 'fixture'),
                          ('data/processed/dictionary.json', '{}'), ('data/documents/chunks.json', '[]')]:
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content)
    calls = []

    class Local:
        def __init__(self): self.calls = []
        def config(self): return {'model_id': 'qwen-fixture'}

    class Cloud(Local):
        def config(self): return {'model_id': 'claude-fixture'}

    class FakeAnalyst:
        def __init__(self, db, retriever, llm, deadline):
            self.llm = llm
            assert deadline == 600.
        def answer(self, question, mode):
            calls.append((type(self.llm).__name__, question, mode))
            self.llm.calls.append({'input_tokens': 10, 'output_tokens': 3})
            if type(self.llm) is Local:
                raise RuntimeError('private service error must not be exported')
            # Detect a changed source rather than silently claiming comparability.
            if change_source:
                (tmp_path / 'data/processed/dictionary.json').write_text('{"changed":true}')
            return RunResult(mode, Draft(question=question, spec=QuerySpec(), answer='fixture answer'), 'unchecked')

    monkeypatch.setattr(module, 'LocalQwenLLM', Local)
    monkeypatch.setattr(module, 'BedrockLLM', Cloud)
    monkeypatch.setattr(module, 'Analyst', FakeAnalyst)
    record = run_comparison(tmp_path, ' Same question ', 'B0')
    assert sorted(calls) == sorted([('Local', 'Same question', 'B0'), ('Cloud', 'Same question', 'B0')])
    assert record['execution']=='parallel'
    assert record['results']['local_qwen']['error'] == 'RuntimeError'
    assert record['results']['bedrock']['result']['draft']['answer'] == 'fixture answer'
    assert record['results']['local_qwen']['input_tokens'] == 10
    assert record['inputs_unchanged'] is (not change_source)
    assert 'private service error' not in json.dumps(record)
    saved = json.loads((tmp_path / 'runs/comparisons' / (record['id'] + '.json')).read_text(encoding='utf-8'))
    assert saved['results']['local_qwen']['calls'] == [{'input_tokens': 10, 'output_tokens': 3}]
    assert saved['input_hashes'] == record['input_hashes']


def test_comparison_ui_runs_only_on_submit_and_retains_results(chat, monkeypatch):
    import aave_analyst.comparison as module
    calls = []

    def fake_run(root, question, mode, deadline, progress=None):
        assert deadline == 900.
        assert callable(progress)
        progress({'provider':'local_qwen','event':'model_started','elapsed_seconds':0})
        progress({'provider':'local_qwen','event':'call_started','role':'sql','elapsed_seconds':2,'remaining_seconds':898})
        progress({'provider':'local_qwen','event':'call_finished','role':'sql','elapsed_seconds':3,'remaining_seconds':897})
        progress({'provider':'local_qwen','event':'model_finished','status':'unchecked','elapsed_seconds':4})
        calls.append((question, mode))
        result = {'mode': mode, 'status': 'unchecked', 'elapsed': 1, 'repairs': 0,
                  'issues': [], 'trace': [], 'draft': {'question': question, 'answer': 'Qwen fixture',
                  'sql': 'SELECT 107 AS value', 'query_result': {'columns': ['value'], 'rows': [{'value': 107}]},
                  'spec': {}, 'documents': [], 'claims': []}}
        return {'id': 'fixture-id', 'created_at': 'fixture-time', 'question': question, 'mode': mode,
                'deadline_seconds_per_model': 900., 'input_hashes': {'db': 'fixture-hash'}, 'inputs_unchanged': True,
                'results': {
                    'local_qwen': {'config': {'model_id': 'qwen-fixture'}, 'wall_seconds': 1., 'model_calls': 1,
                                   'input_tokens': 10, 'output_tokens': 3, 'result': result},
                    'bedrock': {'config': {'model_id': 'claude-fixture'}, 'wall_seconds': .1, 'model_calls': 0,
                                'input_tokens': 0, 'output_tokens': 0, 'error': 'NoCredentialsError'}}}

    monkeypatch.setattr(module, 'run_comparison', fake_run)
    chat.radio(key='workspace').set_value('So sánh Qwen – Claude').run()
    assert not chat.exception and calls == []
    assert chat.number_input(key='ui_timeout').value == 600
    chat.number_input(key='ui_timeout').set_value(900).run()
    chat.text_area(key='comparison_question').set_value('Same question')
    chat.selectbox(key='comparison_mode').select('B0')
    next(button for button in chat.button if button.label == 'Chạy so sánh Qwen + Claude').click().run()
    assert not chat.exception
    assert calls == [('Same question', 'B0')]
    assert any('NoCredentialsError' in error.value for error in chat.error)
    assert len(chat.dataframe) == 1 and len(chat.code) == 1
    chat.run()
    assert calls == [('Same question', 'B0')]
    assert len(chat.session_state['comparisons']) == 1
    chat.radio(key='workspace').set_value('Hội thoại').run()
    chat.radio(key='workspace').set_value('So sánh Qwen – Claude').run()
    assert not chat.exception and calls == [('Same question', 'B0')]


def test_empty_comparison_does_not_call_models(chat, monkeypatch):
    import aave_analyst.comparison as module
    monkeypatch.setattr(module, 'run_comparison', lambda *args: pytest.fail('Must not call models'))
    chat.radio(key='workspace').set_value('So sánh Qwen – Claude').run()
    next(button for button in chat.button if button.label == 'Chạy so sánh Qwen + Claude').click().run()
    assert not chat.exception
    assert any('Nhập câu hỏi' in warning.value for warning in chat.warning)


def test_chat_model_choice_is_explicit_and_rerun_does_not_call_again(chat, monkeypatch):
    import aave_analyst.cli as cli
    original = cli.analyst_at
    selected = []

    def factory(root, provider=None, deadline=120.):
        assert deadline == 600.
        selected.append(provider)
        return original(root, deadline=deadline)

    monkeypatch.setattr(cli, 'analyst_at', factory)
    chat.selectbox(key='chat_provider').select('local_qwen').run()
    assert selected == []
    chat.chat_input[0].set_value('Question for Qwen').run()
    assert not chat.exception and selected == ['local_qwen']
    assert chat.session_state['messages'][-1]['result']['model_label'] == 'Qwen ViText2SQL 3B · local'
    chat.selectbox(key='chat_provider').select('bedrock').run()
    assert not chat.exception and selected == ['local_qwen']
