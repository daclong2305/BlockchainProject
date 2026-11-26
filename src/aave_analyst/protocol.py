"""Pre-register traceability IDs and audit final-run coverage without inference."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import random

from .pipeline import MODES

FINAL_MODES = ('B0', 'B1', 'P')


def evaluation_protocol():
    return {'version':2,'deadline_seconds':120,'repeats':3,'modes':list(FINAL_MODES),
            'test_questions':40,'outputs':360,'repair_limit':2,'retrieval_top_k':5,
            'chunk_words':400,'chunk_overlap':60,'USD_relative_tolerance':'0.005',
            'count_rule':'exact','audit_fraction':1.0,'audit_seed':2026,
            'audit_rule':'Independent human grading of every final output; runtime failures retained; automatic scores are supplementary.',
            'trace_questions':10,'trace_repeat':0,
            'analysis_unit':'question','judge_numeric_scope_required':True}


def trace_selection(records, seed=2026):
    groups = defaultdict(list)
    for row in records:
        if row['split'] == 'test':
            groups[row['category']].append(row['id'])
    if len(groups) != 5 or any(len(ids) < 2 for ids in groups.values()):
        raise ValueError('Trace protocol requires five categories with at least two test questions each')
    rng = random.Random(seed)
    selected = []
    for category, ids in sorted(groups.items()):
        selected.extend({'question_id': qid, 'category': category} for qid in sorted(rng.sample(sorted(ids), 2)))
    return {'schema_version': 2, 'modes': list(FINAL_MODES), 'created_at': datetime.now(timezone.utc).isoformat(),
            'selection_rule': 'two IDs per category; sorted IDs; seeded random; no model outputs inspected',
            'seed': seed, 'selected': selected,
            'measurement_rule': 'For repeat 0 in each registered mode, start timing when opening the answer; stop after finding and checking the cited source/SQL result or recording failure. Record actual seconds and notes. Do not replace failed cases.'}


def trace_forms(selection):
    return [dict(item, mode=mode, repeat=0, reviewer_name='', traceable=None,
                 elapsed_seconds=None, source_checked='', notes='')
            for item in selection['selected'] for mode in selection.get('modes', MODES)]


def coverage_report(records, results, protocol=None):
    protocol = evaluation_protocol() if protocol is None else protocol
    ids = {row['id'] for row in records if row['split'] == 'test'}
    expected = {(qid, repeat, mode) for qid in ids for repeat in range(protocol['repeats']) for mode in protocol['modes']}
    counts = Counter((row.get('question_id'), row.get('repeat'), row.get('mode')) for row in results)
    actual = set(counts)
    missing, unexpected = expected - actual, actual - expected
    duplicates = [(key, count) for key, count in counts.items() if count > 1]
    shared = defaultdict(set)
    owners = defaultdict(set)
    missing_shared = 0
    for row in results:
        draft_id = row.get('shared_draft_id')
        if not draft_id:
            missing_shared += 1
        pair=(row.get('question_id'), row.get('repeat'))
        shared[pair].add(draft_id)
        owners[draft_id].add(pair)
    inconsistent = [key for key, values in shared.items() if len(values) != 1]
    reused = [key for key, values in owners.items() if len(values)>1]
    return {'complete': len(ids) == protocol['test_questions'] and not (missing or unexpected or duplicates or inconsistent or missing_shared or reused),
            'test_questions': len(ids), 'expected_outputs': len(expected), 'actual_outputs': len(results),
            'missing': sorted(missing), 'unexpected': sorted(unexpected, key=str),
            'duplicates': sorted(duplicates, key=str), 'inconsistent_shared_draft': sorted(inconsistent, key=str),
            'missing_shared_draft_id': missing_shared, 'reused_shared_draft_id': sorted(reused,key=str),
            'runtime_errors': sum(bool(row.get('error')) for row in results),
            'note': 'Coverage includes errors and timeouts; it does not certify answer quality or human review.'}
