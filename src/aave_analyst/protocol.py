"""Pre-register traceability IDs and audit final-run coverage without inference."""
from collections import Counter, defaultdict
from datetime import datetime, timezone
import random

from .pipeline import MODES


def evaluation_protocol():
    return {'version':1,'deadline_seconds':120,'repeats':3,'modes':list(MODES),
            'test_questions':40,'outputs':720,'repair_limit':2,'retrieval_top_k':5,
            'chunk_words':400,'chunk_overlap':60,'USD_relative_tolerance':'0.005',
            'count_rule':'exact','audit_fraction':0.2,'audit_seed':2026,
            'audit_rule':'ceil(20% of successful judge outputs); proportional strata mode/category with largest remainder; report eligible and total populations separately',
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
    return {'schema_version': 1, 'created_at': datetime.now(timezone.utc).isoformat(),
            'selection_rule': 'two IDs per category; sorted IDs; seeded random; no model outputs inspected',
            'seed': seed, 'selected': selected,
            'measurement_rule': 'For repeat 0 in each of six modes, start timing when opening the answer; stop after finding and checking the cited source/SQL result or recording failure. Record actual seconds and notes. Do not replace failed cases.'}


def trace_forms(selection):
    return [dict(item, mode=mode, repeat=0, reviewer_name='', traceable=None,
                 elapsed_seconds=None, source_checked='', notes='')
            for item in selection['selected'] for mode in MODES]


def coverage_report(records, results):
    ids = {row['id'] for row in records if row['split'] == 'test'}
    expected = {(qid, repeat, mode) for qid in ids for repeat in range(3) for mode in MODES}
    counts = Counter((row.get('question_id'), row.get('repeat'), row.get('mode')) for row in results)
    actual = set(counts)
    missing, unexpected = expected - actual, actual - expected
    duplicates = [(key, count) for key, count in counts.items() if count > 1]
    shared = defaultdict(set)
    missing_shared = 0
    for row in results:
        draft_id = row.get('shared_draft_id')
        if not draft_id:
            missing_shared += 1
        shared[(row.get('question_id'), row.get('repeat'))].add(draft_id)
    inconsistent = [key for key, values in shared.items() if len(values) != 1]
    return {'complete': len(ids) == 40 and not (missing or unexpected or duplicates or inconsistent or missing_shared),
            'test_questions': len(ids), 'expected_outputs': len(expected), 'actual_outputs': len(results),
            'missing': sorted(missing), 'unexpected': sorted(unexpected, key=str),
            'duplicates': sorted(duplicates, key=str), 'inconsistent_shared_draft': sorted(inconsistent, key=str),
            'missing_shared_draft_id': missing_shared,
            'runtime_errors': sum(bool(row.get('error')) for row in results),
            'note': 'Coverage includes errors and timeouts; it does not certify answer quality or human review.'}
