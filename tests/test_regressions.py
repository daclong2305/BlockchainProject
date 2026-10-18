from dataclasses import asdict
import pytest


def test_failed_shared_draft_preserves_elapsed_and_usage(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.pipeline import Analyst
    from aave_analyst.retrieval import Retriever
    from aave_analyst.experiments import run_experiments
    class Failure:
        calls=[]
        def complete(self,role,payload,timeout=60):
            self.calls.append({'role':role,'input_tokens':123,'output_tokens':0,'elapsed':.01})
            raise TimeoutError('network timeout')
    analyst=Analyst(fixture_db(tmp_path),Retriever([]),Failure())
    rows=[{'id':'1','family':'a','split':'dev','question':'q'}]
    results=run_experiments(analyst,rows,tmp_path/'r',1,False,['B0','P'])
    assert all(r['error'] for r in results)
    assert all(sum(u['input_tokens'] for u in r['usage'])==123 for r in results)
    assert all(r['elapsed']>0 for r in results)


def test_benchmark_questions_are_unique_and_no_exact_cross_split_leakage(tmp_path):
    from aave_analyst.benchmark import create_benchmark,validate_benchmark
    from test_pipeline import fixture_db
    rows=create_benchmark(fixture_db(tmp_path),[])
    assert len({r['question'] for r in rows})==60
    dev={r['question'] for r in rows if r['split']=='dev'}
    test={r['question'] for r in rows if r['split']=='test'}
    assert not dev.intersection(test)
    with pytest.raises(ValueError,match='question'):
        validate_benchmark([{'id':'a','family':'a','split':'dev','question':'same'},{'id':'b','family':'b','split':'test','question':'same'}])


def test_deadline_is_checked_even_for_b0(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.pipeline import Analyst
    from aave_analyst.models import Draft,QuerySpec
    from aave_analyst.llm import ScriptedLLM
    from aave_analyst.retrieval import Retriever
    result=Analyst(fixture_db(tmp_path),Retriever([]),ScriptedLLM({}),deadline=1).continue_draft(Draft(question='q',spec=QuerySpec(),elapsed=2), 'B0')
    assert result.error


def test_numeric_wrong_unit_does_not_pass_code_verification():
    from aave_analyst.verification import verify_claims
    from aave_analyst.models import Draft,QuerySpec,QueryResult
    from aave_analyst.llm import ScriptedLLM
    draft=Draft(question='q',spec=QuerySpec(unit='USD'),answer='100 tokens [SQL1]',query_result=QueryResult(['value'],[{'value':100.}]),claims=[{'text':'100 tokens','citations':['SQL1'],'numeric':{'value':100,'unit':'count','evidence_id':'SQL1','row':0,'column':'value'}}])
    issues=verify_claims(draft,ScriptedLLM({'claim_review':[{'issues':[]}]}))
    assert any(i.code=='numeric_unit' for i in issues)


def test_expected_refusal_is_not_automatically_correct():
    from aave_analyst.experiments import summarize
    score={'question_id':'q','category':'unanswerable','mode':'P','repeat':0,'numeric_correct':None,'correct':False,'judge':{'answer_correctness':0,'faithfulness':0,'citation_quality':0,'refusal_correct':False},'judge_error':'','citation':{'precision':None,'completeness':None},'refused':True,'expected_refusal':True,'elapsed':1.,'input_tokens':0,'output_tokens':0,'runtime_error':False}
    assert summarize([score])['configurations']['P']['correct_refusals']==0


def test_actual_sql_and_retrieval_calls_are_logged(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.retrieval import Retriever
    db=fixture_db(tmp_path)
    db.query('SELECT count(*) FROM liquidation_events')
    assert db.calls[-1]['tool']=='sql'
    assert db.calls[-1]['elapsed']>=0
    retriever=Retriever([]);retriever.search('health factor')
    assert retriever.calls[-1]['tool']=='retrieve'


def test_stress_evaluation_starts_with_complete_shared_answer(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.stress import evaluate_stress
    from aave_analyst.models import RunResult
    class Stub:
        calls=[]
        def complete(self,*args,**kwargs):return {'kind':'data'}
    class Fake:
        llm=Stub()
        db=fixture_db(tmp_path)
        deadline=120.
        def _answer(self,draft,end):draft.answer='Candidate answer'
        def continue_draft(self,draft,mode):
            assert draft.answer=='Candidate answer'
            return RunResult(mode,draft,'unchecked')
    rows=[{'id':'s','question':'q','error_type':'metric','correct_sql':'SELECT 1 AS value','wrong_sql':'SELECT 2 AS value','reference_rows':[{'value':1}]}]
    assert len(evaluate_stress(rows,Fake()))==4
