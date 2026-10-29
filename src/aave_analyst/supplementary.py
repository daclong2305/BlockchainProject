"""Report supplementary measurements; never invent human labels or timing."""
from collections import Counter
import math
import statistics
import unicodedata
from .evaluation import percentile
from .pipeline import MODES


def trace_report(rows, registration):
    if len(registration['selected'])!=10 or len({item['question_id'] for item in registration['selected']})!=10:
        raise ValueError('Ten unique registered question IDs required')
    expected={(item['question_id'],mode,0) for item in registration['selected'] for mode in MODES}
    keys=[(row.get('question_id'),row.get('mode'),row.get('repeat')) for row in rows]
    if len(keys)!=len(set(keys)) or set(keys)!=expected:
        raise ValueError('Trace measurements must match all 60 registered question/mode/repeat combinations')
    complete=[];pending=[]
    for row in rows:
        seconds=row.get('elapsed_seconds')
        if row.get('traceable') is None or seconds is None or not row.get('reviewer_name','').strip():
            pending.append(row);continue
        if type(row['traceable']) is not bool or type(seconds) not in (int,float) or not math.isfinite(seconds) or seconds<0:
            raise ValueError('Trace decision must be boolean and duration finite nonnegative seconds')
        if row['traceable'] and not row.get('source_checked','').strip():
            raise ValueError('Trace success requires the source actually checked')
        if not row['traceable'] and not row.get('notes','').strip():
            raise ValueError('Trace failure requires an explanation; keep failed cases')
        complete.append(row)
    modes={}
    for mode in MODES:
        measured=[row for row in complete if row['mode']==mode]
        times=[row['elapsed_seconds'] for row in measured]
        modes[mode]={'expected':10,'measured':len(measured),'traceable':sum(row['traceable'] for row in measured),
                     'median_seconds':statistics.median(times) if times else None,'p95_seconds':percentile(times,.95)}
    return {'complete':not pending,'registered_questions':len(registration['selected']),
            'measured':len(complete),'pending':len(pending),'per_mode':modes,
            'note':'Human-recorded elapsed time; failures remain in measurements. No timing is inferred from model latency.'}


def stress_report(results):
    keys=[(row['stress_id'],row['injected'],row['mode']) for row in results]
    if len(keys)!=len(set(keys)):raise ValueError('Duplicate stress output')
    summary={}
    for mode in sorted({row['mode'] for row in results}):
        subset=[row for row in results if row['mode']==mode]
        counts=Counter()
        for row in subset:
            label=row['injected']
            if label not in {'wrong','correct'}:raise ValueError('Unknown injection label')
            counts[label+'_total']+=1
            if row.get('error'):counts['runtime_errors']+=1
            initial=next((event for event in row.get('trace',[]) if event.get('event')=='verification' and event.get('repair')==0),None)
            if initial is not None:
                counts[label+'_initial_checks_completed']+=1
                counts[label+'_initial_flagged']+=bool(initial.get('issues'))
            a,b=row.get('reviewer_1',{}),row.get('reviewer_2',{})
            if a.get('final_correct') is not None or b.get('final_correct') is not None:
                names=[unicodedata.normalize('NFC',' '.join(str(x.get('name','')).casefold().split())) for x in (a,b)]
                if not all(names) or names[0]==names[1] or any(type(x.get('final_correct')) is not bool for x in (a,b)):
                    raise ValueError('Two distinct human reviewers must supply boolean final correctness')
                counts['human_reviewed']+=1
                if a['final_correct']!=b['final_correct']:counts['human_disagreements']+=1
                else:
                    counts['human_agreed']+=1
                    if label=='wrong' and a['final_correct']:counts['human_confirmed_wrong_to_right']+=1
                    if label=='correct' and not a['final_correct']:counts['human_confirmed_right_to_wrong']+=1
        times=[row['elapsed'] for row in subset]
        expected={(sid,label) for sid in {r['stress_id'] for r in results} for label in ('wrong','correct')}
        actual={(row['stress_id'],row['injected']) for row in subset}
        summary[mode]={'outputs':len(subset),'coverage_complete':actual==expected,
                       'counts':dict(counts),'median_seconds':statistics.median(times) if times else None,
                       'p95_seconds':percentile(times,.95)}
    return {'per_mode':summary,'observed_cases':len({row['stress_id'] for row in results}),
            'both_modes_present':set(summary)=={'B1','P'},
            'note':'Coverage is only within observed case IDs; compare with the frozen stress manifest for full coverage. Initial flags are checker behavior, not ground-truth detection accuracy. Repair/breakage counts require two human decisions; missing review is not success. Stress results are separate from the 60-question benchmark.'}
