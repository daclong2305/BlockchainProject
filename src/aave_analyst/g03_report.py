"""Blinded review and paired reporting for the G03 final experiment."""

import argparse
from collections import defaultdict
from hashlib import sha256
import json
from pathlib import Path
import random
import unicodedata

from .audit_review import METRICS, audit_cases, export_audit, import_audit
from .benchmark import load_benchmark
from .costs import experiment_costs
from .evaluation import percentile
from .protocol import coverage_report
from .reporting import cohen_kappa

RUBRIC = Path('docs/G03_RUBRIC_VI.md')
CALIBRATION = Path('report/human-review/rubric-calibration.json')
DEV_AUDIT = Path('runs/claude-full-20261110-retry-v1/human_audit.json')
REFUSAL = 'observed_refusal'


def read_json(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def write_new(path, value):
    with path.open('x', encoding='utf-8') as stream:
        json.dump(value, stream, indent=2, ensure_ascii=False)
        stream.write('\n')


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def pack_reviews(source, destination, rubric, *, calibration=False):
    export_audit(source, destination)
    for reviewer in (1, 2):
        form = destination / f'reviewer-{reviewer}.json'
        packet = read_json(form)
        packet['rubric_sha256'] = digest(rubric)
        if calibration:
            packet['rubric_approved'] = None
        else:
            for item in packet['items']:
                item[REFUSAL] = None
        form.write_text(json.dumps(packet, indent=2, ensure_ascii=False), encoding='utf-8')
        booklet = destination / f'reviewer-{reviewer}.md'
        refusal_instruction = ('\nTrong phiếu final, điền `observed_refusal` bằng 1 nếu câu trả lời '
                               'từ chối trả lời nội dung chính, hoặc 0 nếu vẫn trả lời nội dung chính.\n') if not calibration else ''
        booklet.write_text(rubric.read_text(encoding='utf-8') + refusal_instruction + '\n\n' +
                           booklet.read_text(encoding='utf-8'), encoding='utf-8')


def consensus(source, first, second, rubric, adjudication, template, *, final=False):
    paths = (Path(first), Path(second))
    packets = [read_json(path) for path in paths]
    if any(packet.get('original_reviewer_label') for packet in packets):
        raise ValueError('Use independent human submissions from the current review forms')
    if any(packet.get('rubric_sha256') != digest(rubric) for packet in packets):
        raise ValueError('Both review packets must use the frozen rubric')
    rows = import_audit(source, *paths)
    refusal_ratings = [{item['case_id']: item.get(REFUSAL) for item in packet['items']}
                       for packet in packets] if final else []
    metrics = (*METRICS, REFUSAL) if final else METRICS
    disagreements = []
    for row, case in zip(rows, audit_cases(rows)):
        if final:
            for i, index in enumerate(refusal_ratings, start=1):
                rating = index[case['case_id']]
                if type(rating) is not int or rating not in (0, 1):
                    raise ValueError(f"Missing binary {REFUSAL} for {case['case_id']}")
                row[f'reviewer_{i}'][REFUSAL] = rating
        answers = {}
        for metric in metrics:
            a, b = (row[f'reviewer_{i}'][metric] for i in (1, 2))
            if a == b:
                answers[metric] = a
            else:
                answers[metric] = None
        row['human'] = answers
        unresolved = {metric: None for metric in metrics if answers[metric] is None}
        if unresolved:
            disagreements.append(dict(case_id=case['case_id'], **unresolved, notes=''))
    if not disagreements:
        return rows
    binding = {'source_sha256': digest(source), 'review_sha256': [digest(path) for path in paths],
               'rubric_sha256': digest(rubric)}
    if adjudication is None:
        if template.exists() and any(read_json(template).get(key) != value for key, value in binding.items()):
            template = template.with_name(f"{template.stem}-{binding['review_sha256'][0][:8]}-"
                                          f"{binding['review_sha256'][1][:8]}.json")
        if not template.exists():
            write_new(template, dict(binding, items=disagreements))
        raise ValueError(f'Independent ratings disagree. Complete the adjudication file at {template}')
    decisions = read_json(Path(adjudication))
    if any(decisions.get(field) != value for field, value in binding.items()):
        raise ValueError('The adjudication file does not match the two review packets and rubric')
    items = decisions.get('items', [])
    index = {item['case_id']: item for item in items}
    if len(index) != len(items) or set(index) != {item['case_id'] for item in disagreements}:
        raise ValueError('Adjudication must cover exactly the disputed cases')
    for row, case in zip(rows, audit_cases(rows)):
        item = index.get(case['case_id'])
        if item is None:
            continue
        if not str(item.get('notes', '')).strip():
            raise ValueError(f"Adjudication requires reasons for {case['case_id']}")
        for metric, existing in row['human'].items():
            if existing is None:
                decision = item.get(metric)
                if type(decision) is not int or decision not in (0, 1):
                    raise ValueError(f"Missing adjudicated {metric} for {case['case_id']}")
                row['human'][metric] = decision
    return rows


def agreement(rows):
    output = {}
    for metric in METRICS:
        first = [row['reviewer_1'][metric] for row in rows]
        second = [row['reviewer_2'][metric] for row in rows]
        judged = [row for row in rows if (row.get('judge') or {}).get(metric) in (0, 1)]
        output[metric] = {
            'reviewed': len(rows), 'reviewer_agreement': sum(a == b for a, b in zip(first, second)),
            'reviewer_kappa': cohen_kappa(first, second), 'judged': len(judged),
            'judge_matches_human': sum(row['judge'][metric] == row['human'][metric] for row in judged),
        }
    return output


def validate_rubric_calibration(root):
    calibration = read_json(root / CALIBRATION)
    reviewers = calibration.get('reviewers', [])
    names = {unicodedata.normalize('NFC', ' '.join(str(reviewer.get('name', '')).casefold().split()))
             for reviewer in reviewers}
    if (calibration.get('rubric_sha256') != digest(root / RUBRIC) or len(reviewers) != 2
            or len(names) != 2 or '' in names or any(r.get('approved') is not True for r in reviewers)):
        raise ValueError('The current rubric needs calibration and approval by two distinct reviewers')


def calibrate(root, first, second, adjudication=None):
    packets = [read_json(Path(path)) for path in (first, second)]
    if any(packet.get('rubric_approved') is not True for packet in packets):
        raise ValueError('Both reviewers must confirm the rubric after their independent scores')
    rows = consensus(root / DEV_AUDIT, first, second, root / RUBRIC, adjudication,
                     Path(first).parent / 'calibration-adjudication.json')
    result = {'rubric_sha256': digest(root / RUBRIC),
              'reviewers': [{'name': packet['reviewer_name'], 'approved': True} for packet in packets],
              'review_sha256': [digest(Path(path)) for path in (first, second)],
              'dev_audit_sha256': digest(root / DEV_AUDIT), 'agreement': agreement(rows)}
    if adjudication:
        result['adjudication_sha256'] = digest(Path(adjudication))
    write_new(root / CALIBRATION, result)
    return result


def output_key(row):
    return row['question_id'], row['repeat'], row['mode']


def final_context(record, draft):
    return {
        'question': record['question'], 'reference_answer': record['reference_answer'],
        'reference_sources': record['sources'], 'numeric_reference': record.get('expected_numeric', []),
        'scope': record.get('scope', {}), 'expected_refusal': record.get('expected_refusal', False),
        'answer': draft['answer'], 'claims': draft.get('claims', []),
        'sql': draft.get('sql'), 'sql_result': draft.get('query_result'),
        'documents': draft.get('documents', []),
    }


def final_inputs(run):
    config = read_json(run / 'config.json')
    integrity = read_json(run / 'integrity.json')
    protocol = config.get('evaluation_protocol', {})
    if (config.get('final') is not True or protocol.get('modes') != ['B0', 'B1', 'P']
            or protocol.get('repeats') != 3 or protocol.get('test_questions') != 40):
        raise ValueError('Review requires a G03 final run of B0/B1/P on 40 questions, three repeats')
    for name in ('sources', 'code'):
        field = 'source_hashes' if name == 'sources' else 'code_hashes'
        if not integrity.get(f'{name}_unchanged') or integrity.get(f'{field}_after') != config.get(field):
            raise ValueError('Final run failed integrity verification')
    benchmark = load_benchmark(run / 'benchmark_snapshot.jsonl')
    results = load_benchmark(run / 'results.jsonl')
    if not coverage_report(benchmark, results, protocol)['complete']:
        raise ValueError('Final output coverage is incomplete')
    initial = load_benchmark(run / 'initial_drafts.jsonl')
    ids = {(row['question_id'], row['repeat']): row['shared_draft_id'] for row in initial}
    if len(ids) != len(initial) or ids != {output_key(row)[:2]: row['shared_draft_id'] for row in results}:
        raise ValueError('Initial drafts must match all 120 question/repeat pairs')
    return config, {row['id']: row for row in benchmark}, results, initial


def final_cases(records, results):
    groups = {}
    for row in results:
        if row.get('error'):
            continue
        context = final_context(records[row['question_id']], row['draft'])
        fingerprint = json.dumps([row['question_id'], context], sort_keys=True, ensure_ascii=False)
        groups.setdefault(fingerprint, {'review_context': context, 'outputs': []})
        groups[fingerprint]['outputs'].append(output_key(row))
    cases = [groups[key] for key in sorted(groups)]
    random.Random(2026).shuffle(cases)
    return cases


def export_final(run, destination, rubric=RUBRIC):
    _, records, results, _ = final_inputs(run)
    cases = final_cases(records, results)
    source = run / 'final-review-source.json'
    if any((destination / f'reviewer-{i}.{ext}').exists()
           for i in (1, 2) for ext in ('json', 'md')):
        raise FileExistsError('Preserve existing blinded review packets')
    write_new(source, cases)
    if cases:
        pack_reviews(source, destination, rubric)
    return cases


def summarize_pairs(labeled, modes):
    comparisons = {}
    for mode in modes:
        pairs = [(value, labeled[(qid, repeat, 'P')], repeat)
                 for (qid, repeat, m), value in labeled.items() if m == mode]

        def counts(rows):
            return {'pairs': len(rows),
                    'wrong_to_right': sum(not a['correct'] and b['correct'] for a, b, _ in rows),
                    'right_to_wrong': sum(a['correct'] and not b['correct'] for a, b, _ in rows),
                    'right_to_wrong_refusal': sum(a['correct'] and b['wrong_refusal'] for a, b, _ in rows)}

        comparisons[mode] = dict(counts(pairs), by_repeat=[
            dict(counts([row for row in pairs if row[2] == repeat]), repeat=repeat) for repeat in range(3)])
    return comparisons


def import_final(run, first, second, adjudication=None, rubric=RUBRIC):
    config, records, results, initial = final_inputs(run)
    source = run / 'final-review-source.json'
    cases = final_cases(records, results)
    if read_json(source) != json.loads(json.dumps(cases)):
        raise ValueError('Final review cases no longer match the run outputs and references')
    reviewed = consensus(source, first, second, rubric, adjudication,
                         run / 'final-adjudication.json', final=True) if cases else []
    human = {tuple(key): row['human'] for row in reviewed for key in row['outputs']}
    scored = {}
    by_mode = defaultdict(list)
    for row in results:
        key = output_key(row)
        failure = bool(row.get('error'))
        refused = not failure and bool(human[key][REFUSAL])
        expected_refusal = records[key[0]].get('expected_refusal', False)
        wrong_refusal = refused and not expected_refusal
        correct = not failure and all(human[key][metric] for metric in METRICS) and refused == expected_refusal
        score = {'correct': correct, 'wrong_refusal': wrong_refusal, 'runtime_error': failure,
                 'correct_refusal': correct and refused, 'elapsed': row['elapsed'],
                 'criteria': human.get(key, {})}
        scored[key] = score
        by_mode[key[2]].append(score)
    configurations = {}
    for mode, rows in by_mode.items():
        times = [r['elapsed'] for r in rows]
        configurations[mode] = {
            'outputs': len(rows), 'correct': sum(r['correct'] for r in rows),
            'wrong_refusals': sum(r['wrong_refusal'] for r in rows),
            'correct_refusals': sum(r['correct_refusal'] for r in rows),
            'runtime_errors': sum(r['runtime_error'] for r in rows),
            'criterion_passes': {criterion: sum(r['criteria'].get(criterion, 0) for r in rows)
                                 for criterion in METRICS},
            'median_seconds': percentile(times, .5), 'p95_seconds': percentile(times, .95),
            'by_repeat': [{'repeat': r, 'outputs': 40, 'correct': sum(
                score['correct'] for (_, repeat, m), score in scored.items() if repeat == r and m == mode
            )} for r in range(3)],
        }
    judge_path = run / 'scores.jsonl'
    judge_calls_path = run / 'judge_usage.json'
    if judge_path.exists() != judge_calls_path.exists():
        raise ValueError('Judge artifacts are incomplete. Complete scoring before publishing.')
    judge_rows = load_benchmark(judge_path) if judge_path.exists() else []
    judge_calls = read_json(judge_calls_path) if judge_calls_path.exists() else []
    if judge_path.exists() and (len(judge_rows) != len(scored)
                                or {output_key(row) for row in judge_rows} != set(scored)):
        raise ValueError('Judge output keys must cover the same final run')
    judged = {output_key(row): row['judge'] for row in judge_rows if row.get('judge')}
    linked = [dict(row, judge=judged.get(tuple(key))) for row in reviewed for key in row['outputs']]
    summary = {
        'questions': len(records), 'reviewed_unique': len(reviewed), 'configurations': configurations,
        'pairs': summarize_pairs(scored, ('B0', 'B1')), 'judge_agreement': agreement(linked),
        'costs': experiment_costs(results, judge_calls, config),
        'review_source_sha256': digest(source), 'rubric_sha256': digest(rubric),
    }
    if not judge_path.exists():
        summary['costs']['judge'] = {'reason': 'Judge scoring has not been run'}
    initial_by_key = {(row['question_id'], row['repeat']): row['draft'] for row in initial}
    p_results = sorted((row for row in results if row['mode'] == 'P' and not row.get('error')), key=output_key)
    changed = next(((row, mode) for mode in ('B0', 'B1') for row in p_results if
                    scored[output_key(row)]['correct'] != scored[(*output_key(row)[:2], mode)]['correct']), None)
    if p_results:
        chosen, baseline = changed or (p_results[0], 'B0')
        key = output_key(chosen)
        before = initial_by_key[key[:2]] if baseline == 'B0' else next(
            row['draft'] for row in results if output_key(row) == (*key[:2], baseline))
        summary['presentation_case'] = {
            'question_id': key[0], 'repeat': key[1], 'question': records[key[0]]['question'],
            'before': before, 'after': chosen['draft'], 'baseline': baseline,
            'issues': chosen.get('issues', []), 'trace': chosen.get('trace', []),
            'human': human[key], 'baseline_correct': scored[(*key[:2], baseline)]['correct'],
            'P_correct': scored[key]['correct'],
        }
    output = run / 'final-human-summary.json'
    report = run / 'final-human-report.md'
    if output.exists() or report.exists():
        raise FileExistsError('Preserve existing human results')
    write_new(output, summary)
    with report.open('x', encoding='utf-8') as stream:
        stream.write(report_markdown(summary))
    return summary


def report_markdown(summary):
    lines = ['# Kết quả test G03', '',
             'Hai người chấm độc lập theo rubric. Bảng tính trên 40 câu và 3 lượt mỗi cấu hình.', '',
             '| Cấu hình | Đúng/tổng | Dẫn chứng đạt | Từ chối đúng | Từ chối nhầm | Lỗi runtime | Trung vị (s) | p95 (s) |',
             '|---|---:|---:|---:|---:|---:|---:|---:|']
    for mode, row in summary['configurations'].items():
        lines.append(f"| {mode} | {row['correct']}/{row['outputs']} | "
                     f"{row['criterion_passes']['citation_quality']} | {row['correct_refusals']} | {row['wrong_refusals']} | "
                     f"{row['runtime_errors']} | {row['median_seconds']:.2f} | {row['p95_seconds']:.2f} |")
    lines += ['', '| Cấu hình | Đúng lượt 1 / 40 | Đúng lượt 2 / 40 | Đúng lượt 3 / 40 |',
              '|---|---:|---:|---:|']
    for mode, row in summary['configurations'].items():
        lines.append('| ' + ' | '.join([mode, *(str(r['correct']) for r in row['by_repeat'])]) + ' |')
    lines += ['', '| So sánh | Lượt | Số cặp | Sai → đúng | Đúng → sai | Trong đó từ chối nhầm |',
              '|---|---|---:|---:|---:|---:|']
    for baseline, pair in summary['pairs'].items():
        for row in [pair, *pair['by_repeat']]:
            repeat = row['repeat'] + 1 if 'repeat' in row else 'Tất cả'
            lines.append(f"| {baseline} → P | {repeat} | {row['pairs']} | {row['wrong_to_right']} | "
                         f"{row['right_to_wrong']} | {row['right_to_wrong_refusal']} |")
    lines += ['', '## Chi phí ước tính', '', '| Phạm vi | Token vào | Token ra | Lượt thiếu usage | USD |',
              '|---|---:|---:|---:|---:|']
    costs = summary['costs']
    for name, row in {'Toàn bộ runtime': costs['runtime_physical'], **costs['per_configuration'],
                      'Judge': costs['judge']}.items():
        values = [row.get(key) for key in ('input_tokens', 'output_tokens', 'calls_with_unknown_usage',
                                          'estimated_api_usd')]
        lines.append('| ' + ' | '.join([name, *(str(value) if value is not None else 'chưa có' for value in values)]) + ' |')
    lines += ['', 'Tổng chi phí runtime tính mỗi bản nháp dùng chung một lần. '
              'Chi phí từng cấu hình gồm phần tạo bản nháp khi triển khai riêng.', '',
              '## Judge so với nhãn đã phân xử', '',
              '| Tiêu chí | Khớp / có điểm judge |', '|---|---:|']
    for name, row in summary['judge_agreement'].items():
        lines.append(f"| {name} | {row['judge_matches_human']}/{row['judged']} |")
    case = summary.get('presentation_case')
    if case:
        lines.extend(presentation_markdown(case))
    return '\n'.join(lines) + '\n'


def presentation_markdown(case):
    before, after = case['before'], case['after']
    lines = ['', '## Case test cho slide', '',
             f"**{case['question_id']} · Lượt {case['repeat'] + 1}**", '', case['question'], '',
             f"**{case['baseline']}**", '', before['answer'], '',
             '**P**', '', after['answer'], '']
    for title, draft in ((case['baseline'], before), ('P', after)):
        if draft.get('sql'):
            lines += [f'**SQL · {title}**', '', '```sql', draft['sql'], '```', '']
            result = draft.get('query_result')
            if result:
                lines += ['```json', json.dumps(result['rows'][:3], ensure_ascii=False), '```', '']
        cited = {citation for claim in draft.get('claims', []) for citation in claim.get('citations', [])}
        documents = [doc for doc in draft.get('documents', []) if doc['id'] in cited]
        for doc in documents:
            lines += [f"**Đoạn nguồn · {title} · {doc['id']}**", '', doc.get('text', ''), '']
    lines += ['**Cảnh báo checker**', '']
    issues = [issue for step in case['trace'] if step['event'] == 'verification'
              for issue in step['issues']] or case['issues']
    lines.extend(f"- {message}" for message in dict.fromkeys(issue['message'] for issue in issues))
    if not issues:
        lines.append('Checker không ghi cảnh báo.')
    opinion = {True: 'đạt', False: 'không đạt'}
    lines += ['', f"**Kết quả sau phân xử** · {case['baseline']} {opinion[case['baseline_correct']]} · "
              f"P {opinion[case['P_correct']]}.", '']
    return lines


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path.cwd())
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('calibration-export').add_argument('destination', type=Path)
    calibration = sub.add_parser('calibrate')
    export = sub.add_parser('final-export')
    export.add_argument('run', type=Path)
    export.add_argument('destination', type=Path)
    ingest = sub.add_parser('final-import')
    ingest.add_argument('run', type=Path)
    for command in (calibration, ingest):
        command.add_argument('first', type=Path)
        command.add_argument('second', type=Path)
        command.add_argument('--adjudication', type=Path)
    args = parser.parse_args()
    rubric = args.root / RUBRIC
    if args.command == 'calibration-export':
        pack_reviews(args.root / DEV_AUDIT, args.destination, rubric, calibration=True)
    elif args.command == 'calibrate':
        calibrate(args.root, args.first, args.second, args.adjudication)
    else:
        from .cli import verify_final_run

        verify_final_run(args.root, args.run)
        if args.command == 'final-export':
            print(f'{len(export_final(args.run, args.destination, rubric))} distinct blinded review cases')
        else:
            import_final(args.run, args.first, args.second, args.adjudication, rubric)


if __name__ == '__main__':
    main()
