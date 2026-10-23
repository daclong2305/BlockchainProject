import json

import boto3
from botocore.stub import ANY, Stubber
import pytest

from aave_analyst.llm import BedrockLLM, parse_json


def response(text):
    return {
        'output': {'message': {'role': 'assistant', 'content': [{'text': text}]}},
        'stopReason': 'end_turn',
        'usage': {'inputTokens': 10, 'outputTokens': 5, 'totalTokens': 15},
        'metrics': {'latencyMs': 1},
    }


@pytest.fixture
def bedrock(monkeypatch):
    session = boto3.Session(aws_access_key_id='test', aws_secret_access_key='test', region_name='us-east-1')
    client = session.client('bedrock-runtime')
    monkeypatch.setattr(session, 'client', lambda *args, **kwargs: client)
    llm = BedrockLLM()
    monkeypatch.setattr(llm, 'session', lambda: session)
    with Stubber(client) as stubber:
        yield llm, stubber
        stubber.assert_no_pending_responses()


def test_extra_data_is_retried_with_original_context_and_usage_recorded(bedrock):
    llm, stubber = bedrock
    malformed = json.dumps({'issues': []}, indent=2) + '\nNo issues found.'
    with pytest.raises(json.JSONDecodeError, match='line 4 column 1'):
        parse_json(malformed)
    stubber.add_response('converse', response(malformed))
    payload = {'question': 'Check the answer', 'answer': 'Candidate answer'}
    stubber.add_response('converse', response('{"issues": []}'), {
        'modelId': llm.model_id, 'system': ANY, 'inferenceConfig': ANY,
        'messages': [
            {'role': 'user', 'content': [{'text': json.dumps(payload, ensure_ascii=False, default=str)}]},
            {'role': 'assistant', 'content': [{'text': malformed}]},
            {'role': 'user', 'content': ANY},
        ],
    })
    assert llm.complete('claim_review', payload) == {'issues': []}
    assert len(llm.calls) == 2
    assert llm.calls[0]['error'] == 'JSONDecodeError'
    assert 'error' not in llm.calls[1]
    assert sum(call['input_tokens'] for call in llm.calls) == 20
    assert sum(call['output_tokens'] for call in llm.calls) == 10


def test_multiple_objects_are_not_silently_accepted_and_retry_is_bounded(bedrock):
    llm, stubber = bedrock
    malformed = '{"issues": []}\n{"issues": [{"code": "wrong_sql"}]}'
    for _ in range(2):
        stubber.add_response('converse', response(malformed))
    with pytest.raises(ValueError, match='claim_review'):
        llm.complete('claim_review', {})
    assert len(llm.calls) == 2
    assert all(call['error'] == 'JSONDecodeError' for call in llm.calls)


def test_non_object_json_gets_one_format_retry(bedrock):
    llm, stubber = bedrock
    stubber.add_response('converse', response('[]'))
    stubber.add_response('converse', response('{"issues": []}'))
    assert llm.complete('sql_review', {}) == {'issues': []}
    assert len(llm.calls) == 2


def test_valid_fenced_json_needs_only_one_call(bedrock):
    llm, stubber = bedrock
    stubber.add_response('converse', response('```json\n{"issues": []}\n```'))
    assert llm.complete('claim_review', {}) == {'issues': []}
    assert len(llm.calls) == 1


def test_api_error_is_not_retried_as_a_format_error(bedrock):
    from botocore.exceptions import ClientError
    llm, stubber = bedrock
    stubber.add_client_error('converse', service_error_code='AccessDeniedException')
    with pytest.raises(ClientError):
        llm.complete('plan', {})
    assert len(llm.calls) == 1


def test_format_retry_respects_original_deadline(bedrock, monkeypatch):
    import aave_analyst.llm as module
    llm, stubber = bedrock
    stubber.add_response('converse', response('{} trailing text'))
    # One unit of time per clock read exhausts this call's budget after response 1.
    from itertools import count
    monkeypatch.setattr(module.time, 'perf_counter', lambda counter=count(): next(counter))
    with pytest.raises(TimeoutError):
        llm.complete('plan', {}, timeout=2)
    assert len(llm.calls) == 1
