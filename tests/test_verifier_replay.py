from copy import deepcopy
from aave_analyst.models import Draft, QuerySpec
from aave_analyst.llm import ScriptedLLM
from aave_analyst.retrieval import Retriever
from aave_analyst.pipeline import Analyst
from aave_analyst.verifier_replay import verify_candidate, detection_metrics

def test_replay_is_read_only_and_does_not_need_reference():
    llm=ScriptedLLM({'claim_review':[{'issues':[]}]})
    d=Draft(question='Khái niệm?',spec=QuerySpec(kind='docs'),answer='Nguồn [D1]',claims=[{'text':'Nguồn','citations':['D1']}],documents=[{'id':'D1','text':'Nguồn'}],elapsed=999)
    before=deepcopy(d)
    r=verify_candidate(d,Analyst(None,Retriever([]),llm), 'full')
    assert r['verdict']=='pass' and r['execution_status']=='completed'
    assert d==before
    assert all('reference_answer' not in str(x) for x in r.get('payload_keys',[]))

def test_unrelated_flag_is_not_target_detection_and_timeouts_remain_in_denominator():
    rows=[{'has_error':True,'target_error':'metric','execution_status':'completed','verdict':'fail','issues':[{'code':'time_filter'}]},
          {'has_error':False,'execution_status':'completed','verdict':'fail','issues':[{'code':'metric'}]},
          {'has_error':True,'target_error':'metric','execution_status':'timeout','verdict':None,'issues':[]}]
    m=detection_metrics(rows)
    assert m['tp']==1 and m['fp']==1
    assert m['target_hits']==0
    assert m['recall_all_scheduled_errors']==.5
    assert m['completion_rate']==2/3
    assert m['timeouts']==1

def test_answer_repair_receives_feedback_and_versions(tmp_path):
    from test_pipeline import fixture_db
    llm=ScriptedLLM({'generic_review':[{'issues':[{'code':'unsupported','message':'Remove guarantee','action':'answer'}]},{'issues':[]}], 'repair':[{}], 'answer':[{'answer':'Supported [D1]','claims':[{'text':'Supported','citations':['D1']}]}]})
    seen=[];original=llm.complete
    def capture(role,payload,timeout=60):
        seen.append((role,deepcopy(payload)));return original(role,payload,timeout)
    llm.complete=capture
    d=Draft(question='q',spec=QuerySpec(kind='docs'),answer='Guaranteed',documents=[{'id':'D1','text':'Supported'}])
    r=Analyst(fixture_db(tmp_path),Retriever([]),llm).continue_draft(d,'B1')
    answer=next(p for role,p in seen if role=='answer')
    assert answer['repair_feedback'][0]['code']=='unsupported'
    repair=next(t for t in r.trace if t['event']=='repair')
    assert repair['before']['answer']=='Guaranteed'
    assert repair['after']['answer']=='Supported [D1]'

def test_bedrock_read_timeout_is_reported_as_timeout():
    from botocore.exceptions import ReadTimeoutError
    class TimedOut:
        calls=[]
        def complete(self,*args,**kwargs):raise ReadTimeoutError(endpoint_url='https://example.invalid')
    d=Draft(question='q',spec=QuerySpec(kind='docs'),answer='answer')
    r=verify_candidate(d,Analyst(None,Retriever([]),TimedOut()),'generic')
    assert r['execution_status']=='timeout'
