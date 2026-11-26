from dataclasses import asdict
from copy import deepcopy
import json
from types import SimpleNamespace

import pytest

from aave_analyst.checker_evaluation import review_labels, summarize_replay, draft_hash
from aave_analyst import checker_evaluation as evaluation, cli
from aave_analyst.models import Draft, QuerySpec
from aave_analyst.review import content_hash


def cases():
    return [
        {'id': str(i), 'root_id': str(i // 2), 'group': 'sql' if i < 4 else 'evidence',
         'draft': asdict(Draft(question=str(i // 2), spec=QuerySpec(), answer=str(i)))}
        for i in range(6)
    ]


def packets(rows):
    items = [
        {'id': row['id'], 'content_sha256': content_hash(row), 'has_error': i % 2 == 1,
         'target_error': 'metric' if i < 4 else 'missing_citation', 'notes': 'SQL and sources checked'}
        for i, row in enumerate(rows)
    ]
    for item in items:
        if not item['has_error']:
            item['target_error'] = None
    return [{'reviewer_name': name, 'independent_confirmation': True,
             'items': deepcopy(items)} for name in ('Người một', 'Người hai')]


def test_two_reviewers_must_agree_on_exact_cases():
    rows = cases()
    first, second = packets(rows)
    labels = review_labels(rows, first, second, require_pairs=True)
    assert len(labels) == 6
    assert labels['5'] == {'has_error': True, 'target_error': 'missing_citation'}
    second['items'][1]['target_error'] = 'join'
    with pytest.raises(ValueError, match='disagree'):
        review_labels(rows, first, second, require_pairs=True)
    second['items'][1] = first['items'][1]
    rows[0]['draft']['answer'] = 'edited'
    with pytest.raises(ValueError, match='changed'):
        review_labels(rows, first, second, require_pairs=True)


def test_blank_and_simulated_reviews_are_rejected():
    rows = cases()
    first, second = packets(rows)
    second['independent_confirmation'] = False
    with pytest.raises(ValueError, match='independent'):
        review_labels(rows, first, second)
    second['independent_confirmation'] = True
    second['original_reviewer_label'] = 'AI mô phỏng'
    with pytest.raises(ValueError, match='independent'):
        review_labels(rows, first, second)


def test_replay_denominators_include_insufficient_and_runtime_failure():
    rows = cases()
    labels = review_labels(rows, *packets(rows))
    states = [('completed', 'pass'), ('completed', 'fail'), ('completed', 'insufficient'),
              ('timeout', None), ('error', None), ('completed', 'pass')]
    replay = [
        {'case_id': case['id'], 'execution_status': state, 'verdict': verdict,
         'candidate_sha256': draft_hash(case['draft']), 'issues': [{'code': 'question_metric'}]}
        for case, (state, verdict) in zip(rows, states)
    ]
    result = summarize_replay(rows, labels, replay)
    assert result['sql']['incorrect'] == {
        'total': 2, 'fail': 1, 'pass': 0, 'insufficient': 0, 'timeout': 1, 'error': 0,
    }
    assert result['sql']['correct']['insufficient'] == 1
    assert result['sql']['question_roots'] == 2
    assert result['sql']['target_code_hits'] == 1
    assert result['evidence']['incorrect']['pass'] == 1
    assert result['evidence']['correct']['error'] == 1
    with pytest.raises(ValueError, match='coverage'):
        summarize_replay(rows, labels, replay[:-1] + replay[:1])


def test_local_review_artifacts_pin_both_decisions(tmp_path, monkeypatch):
    rows = cases()
    directory = tmp_path / evaluation.FINAL_DIR
    directory.mkdir(parents=True)
    for name in ('cases.jsonl', 'preparation.json'):
        (directory / name).write_text(name, encoding='utf-8')
    prepared = {'cases_sha256': 'test-digest', 'source_hashes': {'database': 'db-digest'}}
    monkeypatch.setattr(evaluation, '_checked_cases', lambda root: (rows, prepared))
    files = []
    for i, packet in enumerate(packets(rows), 1):
        path = tmp_path / f'reviewer-{i}.json'
        path.write_text(json.dumps(packet), encoding='utf-8')
        files.append(path)
    assert evaluation.approve_cases(tmp_path, *files) == 6
    hashes = evaluation.checker_lock_inputs(tmp_path)
    approval_path = directory / 'approved.json'
    assert (evaluation.FINAL_DIR / 'approved.json').as_posix() in hashes
    approval = json.loads(approval_path.read_text(encoding='utf-8'))
    approval['labels']['1'] = {'has_error': False, 'target_error': None}
    approval_path.write_text(json.dumps(approval), encoding='utf-8')
    with pytest.raises(ValueError, match='approvals'):
        evaluation.checker_lock_inputs(tmp_path)


def test_holdout_requires_six_evidence_roots_with_two_drafts_each(tmp_path, monkeypatch):
    directory = tmp_path / evaluation.FINAL_DIR
    directory.mkdir(parents=True)
    source = directory / 'cases.jsonl'
    rows = [
        {'id': f'{group}-{index}-{side}', 'root_id': f'{group}-{index}',
         'group': group, 'split': 'test'}
        for group, roots in (('sql', 10), ('evidence', 6))
        for index in range(roots) for side in ('A', 'B')
    ]
    monkeypatch.setattr(evaluation, '_source_hashes', lambda root: {})

    def save(rows):
        evaluation.save_benchmark(rows, source)
        (directory / 'preparation.json').write_text(json.dumps({
            'source_hashes': {}, 'cases_sha256': evaluation._file_hash(source),
        }), encoding='utf-8')

    save(rows)
    assert len(evaluation._checked_cases(tmp_path)[0]) == 32
    save(rows[:-4])
    with pytest.raises(ValueError, match='6 evidence pairs'):
        evaluation._checked_cases(tmp_path)
    rows[-1]['root_id'] = rows[-3]['root_id']
    save(rows)
    with pytest.raises(ValueError, match='two drafts each'):
        evaluation._checked_cases(tmp_path)


def test_replay_checks_freeze_and_only_sends_draft_to_checker(tmp_path, monkeypatch):
    rows = cases()
    directory = tmp_path / evaluation.FINAL_DIR
    directory.mkdir(parents=True)
    labels = review_labels(rows, *packets(rows))
    (directory / 'approved.json').write_text(json.dumps({'labels': labels}), encoding='utf-8')
    hashes = {'cases.jsonl': 'held-out-draft-digest'}
    lock = {'checker_inputs': {}, 'llm_config': {'id': 'fake'}}
    monkeypatch.setattr(evaluation, '_checked_cases', lambda root: (rows, {}))
    monkeypatch.setattr(evaluation, 'checker_lock_inputs', lambda root: hashes)
    monkeypatch.setattr(cli, 'verify_final_lock', lambda root: lock.copy())
    seen = []

    def fake_checker(draft, analyst, variant, deadline):
        assert isinstance(draft, Draft)
        assert variant == 'full'
        assert deadline == 120.
        seen.append(draft.answer)
        return {'execution_status': 'completed', 'verdict': 'pass', 'issues': [],
                'candidate_sha256': draft_hash(asdict(draft))}

    monkeypatch.setattr(evaluation, 'verify_candidate', fake_checker)
    monkeypatch.setattr(cli, 'analyst_at', lambda *args, **kwargs:
                        SimpleNamespace(llm=SimpleNamespace(config=lambda: {'id': 'fake'})))
    out = tmp_path / 'replay'
    with pytest.raises(ValueError, match='freeze'):
        evaluation.run_replay(tmp_path, out)
    assert not out.exists()
    assert seen == []
    lock['checker_inputs'] = hashes
    summary = evaluation.run_replay(tmp_path, out)
    assert seen == [row['draft']['answer'] for row in rows]
    assert summary['sql']['incorrect']['pass'] == 2
    output = [json.loads(line) for line in (out / 'replay.jsonl').read_text(encoding='utf-8').splitlines()]
    assert all('has_error' not in row for row in output)
    with pytest.raises(FileExistsError):
        evaluation.run_replay(tmp_path, out, resume=True)
