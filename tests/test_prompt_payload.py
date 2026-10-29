from copy import deepcopy
from aave_analyst.prompt_payload import local_payload


def test_only_initial_planning_uses_catalog_full_evidence_survives_elsewhere():
    payload={'question':'q','document_evidence':[{'id':'DOC1','title':'Health factor','url':'https://example.org','text':'Full original source'}]}
    original=deepcopy(payload)
    assert 'text' not in local_payload('plan',payload)['document_evidence'][0]
    assert local_payload('plan_review',payload)==original
    assert payload==original


def test_answer_retains_all_source_text_cells_scope_and_existing_claims():
    payload={'documents':[{'id':'DOC1','text':'Full source'}],'sql_result':{'rows':[{'value':100}]},'requirements':{'unit':'USD'},'answer':'','claims':[],'refused':False,'retrieval_runs':[{'tool':'retrieve'}]}
    result=local_payload('answer',payload)
    for key in ('documents','sql_result','requirements'):assert result[key]==payload[key]
    assert 'retrieval_runs' not in result
    assert local_payload('claim_review',payload)==payload
