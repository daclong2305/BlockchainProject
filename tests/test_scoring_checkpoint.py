import json
import pytest
from aave_analyst.scoring import checkpointed_scores


def inputs():
    records=[{'id':'q','category':'mechanism','question':'Question?','sources':[],'reference_answer':'Answer'}]
    results=[{'question_id':'q','repeat':0,'mode':mode,'elapsed':1,'draft':{'answer':'Answer','claims':[]}} for mode in ('B0','P')]
    return records,results


class Judge:
    def __init__(self, interrupt=False):self.calls=[];self.interrupt=interrupt
    def complete(self,*args,**kwargs):
        if self.interrupt and len(self.calls)==1:raise KeyboardInterrupt()
        self.calls.append({'input_tokens':10,'output_tokens':2})
        return {'answer_correctness':1,'faithfulness':1,'citation_quality':1,'claim_checks':[]}


def test_resume_skips_durable_scores_and_preserves_usage(tmp_path):
    records,results=inputs();journal=tmp_path/'journal.jsonl'
    with pytest.raises(KeyboardInterrupt):
        checkpointed_scores(records,results,Judge(True),journal,{'code':'v1'})
    assert len(journal.read_text().splitlines())==2
    judge=Judge()
    scores,usage=checkpointed_scores(records,results,judge,journal,{'code':'v1'},resume=True)
    assert len(scores)==2 and len(usage)==2 and len(judge.calls)==1
    assert [row['mode'] for row in scores]==['B0','P']
    with pytest.raises(FileExistsError):
        checkpointed_scores(records,results,Judge(),journal,{'code':'v1'})


def test_resume_rejects_changed_judge_inputs_or_code_before_call(tmp_path):
    records,results=inputs();journal=tmp_path/'journal.jsonl'
    checkpointed_scores(records,results,Judge(),journal,{'code':'v1'})
    judge=Judge()
    with pytest.raises(ValueError,match='changed'):
        checkpointed_scores(records,results,judge,journal,{'code':'v2'},resume=True)
    assert not judge.calls


def test_malformed_tail_is_preserved_not_silently_removed(tmp_path):
    records,results=inputs();journal=tmp_path/'journal.jsonl'
    checkpointed_scores(records,results,None,journal,{})
    with journal.open('a') as stream:stream.write('{partial')
    before=journal.read_bytes()
    with pytest.raises(ValueError,match='Malformed'):
        checkpointed_scores(records,results,None,journal,{},resume=True)
    assert journal.read_bytes()==before
