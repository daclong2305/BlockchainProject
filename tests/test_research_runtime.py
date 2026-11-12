import json

import pytest
from botocore.exceptions import ClientError, EndpointConnectionError, SSLError

from aave_analyst.research_runtime import MeteredLLM


class Adapter:
    def __init__(self, outcomes):
        self.outcomes = iter(outcomes)
        self.calls = []

    def config(self):
        return {'provider': 'bedrock'}

    def complete(self, role, payload, timeout):
        result = next(self.outcomes)
        record = {'role': role, 'input_tokens': 0, 'output_tokens': 0}
        self.calls.append(record)
        if isinstance(result, Exception):
            record['error'] = type(result).__name__
            raise result
        record.update(input_tokens=10, output_tokens=2)
        return result


def throttle():
    return ClientError({'Error': {'Code': 'ThrottlingException', 'Message': 'Slow down'}}, 'Converse')


def test_throttling_is_retried_and_each_attempt_is_logged(tmp_path, monkeypatch):
    monkeypatch.setattr('aave_analyst.research_runtime.time.sleep', lambda _: None)
    adapter = Adapter([throttle(), {'issues': []}])
    path = tmp_path / 'calls.jsonl'
    llm = MeteredLLM(adapter, path, pace=0)
    assert llm.complete('review', {}, timeout=120) == {'issues': []}
    rows = [json.loads(line) for line in path.read_text().splitlines()]
    assert len(rows) == 2
    assert rows[0]['transport_attempt'] == 1
    assert rows[1]['transport_attempt'] == 2
    assert rows[0]['usage_unknown']


@pytest.mark.parametrize('error', [EndpointConnectionError(endpoint_url='https://example.invalid'),
                                 SSLError(endpoint_url='https://example.invalid', error='certificate')])
def test_persistent_transport_failure_stops_run_instead_of_poisoning_next_cases(tmp_path, monkeypatch, error):
    monkeypatch.setattr('aave_analyst.research_runtime.time.sleep', lambda _: None)
    llm = MeteredLLM(Adapter([error] * 4), tmp_path / 'calls.jsonl', pace=0)
    with pytest.raises(BaseException) as caught:
        llm.complete('review', {}, timeout=120)
    assert type(caught.value).__name__ == 'ResearchRunBlocked'
    assert not isinstance(caught.value, Exception)


def test_does_not_retry_json_errors(tmp_path):
    llm = MeteredLLM(Adapter([ValueError('bad JSON')]), tmp_path / 'calls.jsonl', pace=0)
    with pytest.raises(ValueError):
        llm.complete('review', {})
