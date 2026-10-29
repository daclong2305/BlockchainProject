from aave_analyst.stress import evaluate_stress


def test_stress_plan_timeout_keeps_all_four_outputs_and_usage():
    class LLM:
        calls=[]
        def complete(self,*args,**kwargs):
            assert kwargs['timeout']==120
            self.calls.append({'input_tokens':7,'output_tokens':0})
            raise TimeoutError('model')
    class DB:calls=[]
    class Analyst:
        llm=LLM();db=DB();deadline=120
        def continue_draft(self,*args):raise AssertionError('Do not verify failed draft')
    case={'id':'s','question':'q','error_type':'metric','wrong_sql':'SELECT 2','correct_sql':'SELECT 1','reference_rows':[{'value':1}]}
    persisted=[]
    results=evaluate_stress([case],Analyst(),on_result=persisted.append)
    assert len(results)==4 and persisted==results
    assert all(row['error'] and row['elapsed']>0 for row in results)
    assert all(sum(u['input_tokens'] for u in row['usage'])==7 for row in results)
