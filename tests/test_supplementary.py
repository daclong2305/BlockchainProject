import pytest
from aave_analyst.protocol import trace_selection,trace_forms
from aave_analyst.supplementary import trace_report,stress_report


def registration():
    return trace_selection([{'id':f'{cat}-{i}','category':cat,'split':'test'} for cat in 'abcde' for i in range(2)])


def test_blank_trace_is_pending_not_zero_seconds_success():
    selected=registration()
    result=trace_report(trace_forms(selected),selected)
    assert not result['complete'] and result['pending']==60
    assert result['per_mode']['P']['median_seconds'] is None


def test_trace_keeps_failed_cases_and_requires_real_source_for_success():
    selected=registration();forms=trace_forms(selected)
    for row in forms:row.update(reviewer_name='Fixture human',traceable=False,elapsed_seconds=12,notes='Could not locate source')
    result=trace_report(forms,selected)
    assert result['complete'] and result['per_mode']['P']['traceable']==0
    assert result['per_mode']['P']['median_seconds']==12
    forms[0]['traceable']=True
    with pytest.raises(ValueError,match='source'):trace_report(forms,selected)


def test_trace_rejects_replacement_or_duplicate_case():
    selected=registration();forms=trace_forms(selected)
    forms[-1]=forms[0]
    with pytest.raises(ValueError,match='registered'):trace_report(forms,selected)


def test_stress_flags_do_not_become_correctness_without_humans():
    row={'stress_id':'s','mode':'P','injected':'wrong','elapsed':2,'trace':[{'event':'verification','repair':0,'issues':[{'code':'unit'}]}]}
    report=stress_report([row])
    counts=report['per_mode']['P']['counts']
    assert counts['wrong_initial_flagged']==1
    assert counts.get('human_confirmed_wrong_to_right',0)==0
    assert not report['per_mode']['P']['coverage_complete']


def test_stress_reports_human_disagreements_and_correct_case_damage():
    rows=[{'stress_id':'s','mode':'P','injected':label,'elapsed':2,'trace':[],
           'reviewer_1':{'name':'Fixture A','final_correct':False},
           'reviewer_2':{'name':'Fixture B','final_correct':False if label=='correct' else True}}
          for label in ('wrong','correct')]
    counts=stress_report(rows)['per_mode']['P']['counts']
    assert counts['human_disagreements']==1
    assert counts['human_confirmed_right_to_wrong']==1
