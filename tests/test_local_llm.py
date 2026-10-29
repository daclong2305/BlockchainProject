import json
import pytest
import requests
from aave_analyst.local_llm import LocalQwenLLM, configured_llm


@pytest.fixture
def local_server(monkeypatch):
    replies, sent = [], []

    class Session:
        def __enter__(self):
            return self

        def __exit__(self, *args):
            pass

        def post(self, url, **kwargs):
            assert self.trust_env is False
            sent.append((url, json.loads(json.dumps(kwargs))))
            item = replies.pop(0)
            if isinstance(item, Exception):
                raise item

            class Response:
                def raise_for_status(self):
                    pass

                def json(self):
                    return {'choices': [{'message': {'content': item}, 'finish_reason': 'stop'}],
                            'usage': {'prompt_tokens': 10, 'completion_tokens': 5}}
            return Response()

    monkeypatch.setattr('aave_analyst.local_llm.requests.Session', Session)
    return replies, sent


def test_local_json_retry_preserves_evidence_and_usage(local_server):
    replies, sent = local_server
    replies.extend(['{"sql":"SELECT 1"} extra text', '{"sql":"SELECT 1"}'])
    llm = LocalQwenLLM()
    payload = {'question': 'Đếm giao dịch', 'dictionary': {'grain': 'event'}}
    assert llm.complete('sql', payload) == {'sql': 'SELECT 1'}
    assert len(sent) == 2
    assert json.loads(sent[1][1]['json']['messages'][1]['content']) == payload
    assert sent[1][1]['json']['response_format']['schema']['required'] == ['sql']
    assert sum(c['input_tokens'] for c in llm.calls) == 20
    assert llm.calls[0]['error'] == 'JSONDecodeError'
    assert llm.calls[0]['timeout_seconds'] > 0
    assert llm.calls[0]['prompt_characters'] > 0
    assert sent[1][1]['timeout'][1] <= sent[0][1]['timeout'][1]


def test_local_input_is_nfc_but_original_payload_is_preserved(local_server):
    import unicodedata
    replies, sent = local_server
    replies.append('{"sql":"SELECT 1"}')
    original = unicodedata.normalize('NFD', 'Dữ liệu tiếng Việt')
    payload = {'question': original}
    llm = LocalQwenLLM()
    llm.complete('sql', payload)
    transmitted = json.loads(sent[0][1]['json']['messages'][1]['content'])
    assert transmitted['question'] == unicodedata.normalize('NFC', original)
    assert payload['question'] == original
    assert llm.config()['input_normalization'] == 'NFC'


def test_local_invalid_json_stops_after_two_attempts(local_server):
    replies, sent = local_server
    replies.extend(['[]', '[]'])
    llm = LocalQwenLLM()
    with pytest.raises(ValueError, match='after 2 attempts'):
        llm.complete('sql', {})
    assert len(sent) == len(llm.calls) == 2


def test_role_schema_rejects_wrong_answer_type_even_when_json_is_valid(local_server):
    replies, sent = local_server
    replies.extend(['{"answer":0,"refused":false,"claims":[]}',
                    '{"answer":"Không có kết quả SQL để kết luận.","refused":true,"claims":[]}'])
    result = LocalQwenLLM().complete('answer', {'question': 'q'})
    assert result['refused'] is True
    assert len(sent) == 2
    assert sent[0][1]['json']['response_format']['schema']['properties']['answer']['type'] == 'string'


def test_planning_schema_blocks_database_metric_with_docs_routing(local_server):
    replies, sent = local_server
    plan = {'metric': 'transactions', 'kind': 'docs', 'assets': [], 'start': None, 'end': None,
            'unit': 'count', 'aggregation': 'count_distinct', 'grain': 'none',
            'retrieval_query': '', 'clarification': ''}
    replies.extend([json.dumps(plan), json.dumps(dict(plan, kind='data'))])
    llm = LocalQwenLLM()
    result = llm.complete('plan', {'question': 'Đếm giao dịch thanh lý'})
    assert result['kind'] == 'data'
    assert len(sent) == 2
    assert 'anyOf' in sent[0][1]['json']['response_format']['schema']


def test_local_timeout_records_failure_without_retry(local_server):
    replies, sent = local_server
    replies.append(requests.ReadTimeout())
    llm = LocalQwenLLM()
    with pytest.raises(TimeoutError):
        llm.complete('sql', {})
    assert len(sent) == 1
    assert llm.calls[0]['error'] == 'TimeoutError'
    assert llm.calls[0]['timeout_seconds'] > 0


@pytest.mark.parametrize('url', ['https://example.com', 'http://192.168.1.1:8081', 'http://user:pass@localhost:8081', 'http://localhost:8081/path'])
def test_local_endpoint_keeps_data_on_loopback(url):
    with pytest.raises(ValueError, match='local HTTP'):
        LocalQwenLLM(url)


def test_provider_selection_and_expired_deadline(monkeypatch, local_server):
    monkeypatch.setenv('AAVE_LLM_PROVIDER', 'local_qwen')
    llm = configured_llm()
    assert isinstance(llm, LocalQwenLLM)
    with pytest.raises(TimeoutError):
        llm.complete('sql', {}, timeout=0)
    assert local_server[1] == []
    monkeypatch.setenv('AAVE_LLM_PROVIDER', 'unknown')
    with pytest.raises(ValueError, match='AAVE_LLM_PROVIDER'):
        configured_llm()
