from aave_analyst.protocol import trace_selection, trace_forms, coverage_report
from aave_analyst.protocol import FINAL_MODES, evaluation_protocol
import json
import pytest


def records():
    return [{'id': f'{category}-{i}', 'category': category, 'split': 'test'}
            for category in ['a', 'b', 'c', 'd', 'e'] for i in range(8)]


def test_trace_selection_is_stratified_stable_and_blank():
    a, b = trace_selection(records()), trace_selection(list(reversed(records())))
    assert a['selected'] == b['selected']
    assert len(a['selected']) == 10
    forms = trace_forms(a)
    assert len(forms) == 30
    assert all(row['traceable'] is None and row['elapsed_seconds'] is None for row in forms)


def test_coverage_counts_failures_and_detects_duplicates_and_missing():
    rows = [dict(question_id=q['id'], repeat=i, mode=m, shared_draft_id=f'{q["id"]}-{i}', error='timeout')
            for q in records() for i in range(3) for m in FINAL_MODES]
    report = coverage_report(records(), rows)
    assert report['complete'] and report['runtime_errors'] == 360
    rows[-1] = rows[0].copy()
    report = coverage_report(records(), rows)
    assert not report['complete'] and report['duplicates'] and report['missing']


def test_coverage_requires_shared_draft_identity():
    rows = [dict(question_id=q['id'], repeat=i, mode=m, shared_draft_id=f'{q["id"]}-{i}-{m}')
            for q in records() for i in range(3) for m in FINAL_MODES]
    assert not coverage_report(records(), rows)['complete']
    for row in rows:row['shared_draft_id']='same-for-every-question'
    assert coverage_report(records(), rows)['reused_shared_draft_id']==['same-for-every-question']


def test_failed_shared_draft_records_real_latency(tmp_path, monkeypatch):
    from aave_analyst.experiments import run_experiments
    times = iter([10.0, 130.0])
    monkeypatch.setattr('aave_analyst.experiments.time.monotonic', lambda: next(times))
    class FailedAnalyst:
        def make_draft(self, question):
            raise TimeoutError('deadline')
    output = run_experiments(FailedAnalyst(), [{'id':'q', 'family':'f', 'split':'dev', 'question':'q'}],
                             tmp_path / 'run', repeats=1, final=False, modes=['B0', 'P'])
    assert len(output) == 2
    assert all(row['elapsed'] == 120 and row['error'] for row in output)
    assert len({row['shared_draft_id'] for row in output}) == 1


def test_three_mode_final_writes_120_shared_drafts_and_360_outputs(tmp_path):
    from copy import deepcopy
    from aave_analyst.benchmark import load_benchmark
    from aave_analyst.experiments import run_experiments
    from aave_analyst.models import Draft, QuerySpec, RunResult
    class FixtureAnalyst:
        def make_draft(self, question):
            return Draft(question, QuerySpec(), answer='before', usage=[{'input_tokens':1,'output_tokens':1}])
        def continue_draft(self, shared, mode):
            draft = deepcopy(shared)
            draft.answer = 'after' if mode != 'B0' else shared.answer
            return RunResult(mode, draft, 'fixture', usage=shared.usage.copy())
    questions = [dict(q, family=q['id'], question=q['id'], sources=['fixture'], reference_answer='fixture',
                      review={'reviewer_1':'Synthetic one','reviewer_2':'Synthetic two','approved':True})
                 for q in records()]
    result = run_experiments(FixtureAnalyst(), questions, tmp_path)
    assert evaluation_protocol()['outputs'] == len(result) == 360
    initial = load_benchmark(tmp_path / 'initial_drafts.jsonl')
    assert len(initial) == 120 and all(r['draft']['answer'] == 'before' for r in initial)
    assert {r['shared_draft_id'] for r in result} == {r['shared_draft_id'] for r in initial}
    assert coverage_report(questions, result)['complete']
    assert not coverage_report(questions, result[:-1])['complete']
    assert not coverage_report(questions, result + result[-1:])['complete']


def test_final_cli_freeze_run_and_score_with_offline_synthetic_data(tmp_path, monkeypatch):
    from aave_analyst import cli
    from aave_analyst.benchmark import CATEGORIES, save_benchmark
    from aave_analyst.models import Draft, QuerySpec, RunResult

    class OfflineModel:
        def __init__(self):
            self.calls = []
        def config(self):
            return {'provider':'synthetic'}
        def complete(self, role, payload, timeout):
            assert role == 'judge'
            return {'answer_correctness':1, 'faithfulness':1, 'citation_quality':1}

    class OfflineAnalyst:
        llm = OfflineModel()
        def make_draft(self, question):
            return Draft(question, QuerySpec(kind='docs'), answer='synthetic', elapsed=.1)
        def continue_draft(self, shared, mode):
            return RunResult(mode, shared, 'synthetic', elapsed=.1)

    monkeypatch.setattr(cli, 'configured_llm', OfflineModel)
    monkeypatch.setattr(cli, 'BedrockLLM', OfflineModel)
    monkeypatch.setattr(cli, 'analyst_at', lambda root: OfflineAnalyst())
    gates = {'checker_inputs':{'fixture':'held-out'}, 'rubric_inputs':{'fixture':'rubric'}}
    monkeypatch.setattr(cli, 'review_inputs', lambda root: gates)
    for source in ('data/processed/aave.duckdb','data/processed/dictionary.json','data/documents/chunks.json','data/benchmark/stress.jsonl'):
        path=tmp_path/source
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text('synthetic',encoding='utf-8')
    records=[]
    for category,counts in CATEGORIES.items():
        for split,n in zip(('dev','test'),counts):
            for i in range(n):
                name=f'{category}-{split}-{i}'
                records.append(dict(id=name,question=name,family=name,category=category,split=split,
                                    reference_answer='fixture',sources=['fixture'],
                                    review={'reviewer_1':'fixture A','reviewer_2':'fixture B','approved':True}))
    save_benchmark(records,tmp_path/'data/benchmark/questions.jsonl')
    base=['--root',str(tmp_path)]
    cli.main(base+['trace-register'])
    cli.main(base+['freeze'])
    out=tmp_path/'run'
    results=cli.main(base+['run','--split','test','--final','--out',str(out)])
    assert len(results)==360
    assert cli.verify_final_run(tmp_path,out)['modes']==['B0','B1','P']
    scores=cli.main(base+['score',str(out),'--judge'])
    assert len(scores)==360
    assert set(json.loads((out/'summary.json').read_text())['paired_P_vs'])=={'B0','B1'}
    gates['checker_inputs']['fixture']='changed'
    with pytest.raises(ValueError,match='checker_inputs'):
        cli.verify_final_run(tmp_path,out)
    gates['checker_inputs']['fixture']='held-out'
    with (out/'results.jsonl').open('a',encoding='utf-8') as stream:
        stream.write(json.dumps(results[0])+'\n')
    with pytest.raises(ValueError,match='artifacts'):
        cli.verify_final_run(tmp_path,out)
