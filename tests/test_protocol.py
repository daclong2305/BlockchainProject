from aave_analyst.protocol import trace_selection, trace_forms, coverage_report
from aave_analyst.pipeline import MODES


def records():
    return [{'id': f'{category}-{i}', 'category': category, 'split': 'test'}
            for category in ['a', 'b', 'c', 'd', 'e'] for i in range(8)]


def test_trace_selection_is_stratified_stable_and_blank():
    a, b = trace_selection(records()), trace_selection(list(reversed(records())))
    assert a['selected'] == b['selected']
    assert len(a['selected']) == 10
    forms = trace_forms(a)
    assert len(forms) == 60
    assert all(row['traceable'] is None and row['elapsed_seconds'] is None for row in forms)


def test_coverage_counts_failures_and_detects_duplicates_and_missing():
    rows = [dict(question_id=q['id'], repeat=i, mode=m, shared_draft_id=f'{q["id"]}-{i}', error='timeout')
            for q in records() for i in range(3) for m in MODES]
    report = coverage_report(records(), rows)
    assert report['complete'] and report['runtime_errors'] == 720
    rows[-1] = rows[0].copy()
    report = coverage_report(records(), rows)
    assert not report['complete'] and report['duplicates'] and report['missing']


def test_coverage_requires_shared_draft_identity():
    rows = [dict(question_id=q['id'], repeat=i, mode=m, shared_draft_id=f'{q["id"]}-{i}-{m}')
            for q in records() for i in range(3) for m in MODES]
    assert not coverage_report(records(), rows)['complete']


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
