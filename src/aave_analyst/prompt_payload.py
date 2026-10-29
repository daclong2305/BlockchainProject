"""Stage-specific transport payloads; full evidence remains in the runtime trace."""
from copy import deepcopy


def local_payload(role,payload):
    value=deepcopy(payload)
    if role=='plan' and 'document_evidence' in value:
        # Intent routing needs the source catalog; answering/review still see full text.
        value['document_evidence']=[{key:doc[key] for key in ('id','title','url') if key in doc}
                                    for doc in value['document_evidence']]
        value['document_stage']='Catalog only for intent routing. Full retrieved text is available to the answer and evidence-review stages. Absence of text here is not absent evidence. Do not answer or infer document details from titles.'
    if role=='answer':
        # These fields repeat prior model output or lookup telemetry, not evidence.
        value.pop('retrieval_runs',None)
        if not value.get('answer') and not value.get('claims'):
            for key in ('answer','claims','refused'):value.pop(key,None)
    return value
