import json

import pytest

from aave_analyst.audit_review import audit_cases
from aave_analyst.g03_report import export_final, import_final
from aave_analyst.protocol import evaluation_protocol


def test_blind_reporting_covers_final_run_and_requires_adjudication(tmp_path):
    protocol = evaluation_protocol()
    rows = [{'id': f'Q{i:02}', 'question': f'Question {i}', 'split': 'test',
             'reference_answer': {'required_points': ['answer']}, 'sources': [],
             'expected_refusal': False}
            for i in range(40)]
    results = []
    initial = []
    for row in rows:
        for repeat in range(3):
            qid = row['id']
            draft_id = f'{qid}-R{repeat}'
            key = dict(question_id=qid, repeat=repeat, shared_draft_id=draft_id)
            base = dict(answer='answer', documents=[], claims=[], refused=False)
            initial.append(dict(key, draft=base))
            for mode in ('B0', 'B1', 'P'):
                refusal = qid == 'Q00' and repeat == 0 and mode == 'P'
                failed = qid == 'Q01' and repeat == 0 and mode == 'B1'
                draft = dict(base, answer='I cannot answer' if refusal else 'answer',
                             refused=False)
                results.append(dict(key, mode=mode, draft=draft, elapsed=2, usage=[],
                                    issues=[], error='TimeoutError: deadline' if failed else ''))

    def put(name, value):
        tmp_path.joinpath(name).write_text(json.dumps(value), encoding='utf-8')

    def put_lines(name, values):
        tmp_path.joinpath(name).write_text('\n'.join(map(json.dumps, values)), encoding='utf-8')

    put('config.json', dict(final=True, evaluation_protocol=protocol,
                           llm={'provider': 'llama.cpp'}, source_hashes={}, code_hashes={}))
    put('integrity.json', dict(sources_unchanged=True, code_unchanged=True,
                              source_hashes_after={}, code_hashes_after={}))
    put_lines('benchmark_snapshot.jsonl', rows)
    put_lines('results.jsonl', results)
    put_lines('initial_drafts.jsonl', initial)
    packets = tmp_path / 'review'
    cases = export_final(tmp_path, packets)
    booklet = (packets / 'reviewer-1.md').read_text(encoding='utf-8')
    assert len(cases) == 41
    assert all(marker not in booklet for marker in ('B0', 'B1', 'checks_passed', 'shared_draft_id'))
    paths = [packets / f'reviewer-{i}.json' for i in (1, 2)]
    refusal_case = next(case['case_id'] for case in audit_cases(cases)
                        if case['context']['answer'] == 'I cannot answer')
    for i, path in enumerate(paths):
        data = json.loads(path.read_text(encoding='utf-8'))
        data['reviewer_name'] = f'Reviewer {i}'
        for item in data['items']:
            item.update(answer_correctness=1, faithfulness=1, citation_quality=1,
                        observed_refusal=int(item['case_id'] == refusal_case), notes='Checked source')
        if i == 1:
            data['items'][0]['citation_quality'] = 0
        path.write_text(json.dumps(data), encoding='utf-8')
    with pytest.raises(ValueError, match='adjudication'):
        import_final(tmp_path, *paths)
    conflicts = tmp_path / 'final-adjudication.json'
    decision = json.loads(conflicts.read_text(encoding='utf-8'))
    decision['items'][0].update(citation_quality=1, notes='Both reviewers checked the source')
    conflicts.write_text(json.dumps(decision), encoding='utf-8')
    summary = import_final(tmp_path, *paths, adjudication=conflicts)
    assert summary['configurations']['P']['wrong_refusals'] == 1
    assert summary['pairs']['B0']['right_to_wrong'] == 1
    assert summary['pairs']['B0']['right_to_wrong_refusal'] == 1
    assert summary['pairs']['B1']['wrong_to_right'] == 1
    assert summary['pairs']['B1']['pairs'] == 120
    assert summary['configurations']['B1']['runtime_errors'] == 1
    assert [x['pairs'] for x in summary['pairs']['B0']['by_repeat']] == [40, 40, 40]
