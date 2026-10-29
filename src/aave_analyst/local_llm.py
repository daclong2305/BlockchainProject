"""Local llama.cpp chat adapter for the selected Qwen GGUF."""
import json
import time
from urllib.parse import urlsplit

import requests

from .config import read_settings, normalize_model_text
from .llm import BASE, PROMPTS, BedrockLLM, parse_json
from .response_schemas import SCHEMAS
from .prompt_payload import local_payload

MODEL_ID = 'zhenlong54/qwen-vitext2sql-3b-GGUF'
REVISION = '579ae3d2f0db23dd25fd83076a57dbab79f68dd9'
MODEL_SHA256 = 'b34a028bc6c18d738b57552423bb75ca555d823c19722c4261acc792547a4cd2'


class LocalQwenLLM:
    def __init__(self, base_url=None):
        self.base_url = (base_url or read_settings().get('QWEN_BASE_URL') or 'http://127.0.0.1:8081').rstrip('/')
        url = urlsplit(self.base_url)
        if url.scheme != 'http' or url.hostname not in {'localhost', '127.0.0.1', '::1'} or url.username or url.password or url.query or url.fragment or url.path:
            raise ValueError('QWEN_BASE_URL must be a local HTTP server origin')
        self.model_id = MODEL_ID
        self.calls = []

    def complete(self, role, payload, timeout=60.):
        if timeout <= 0:
            raise TimeoutError('Question deadline exceeded')
        deadline = time.perf_counter() + timeout
        transport_payload=local_payload(role,payload)
        messages = [{'role': 'system', 'content': BASE + PROMPTS[role]},
                    {'role': 'user', 'content': json.dumps(transport_payload, ensure_ascii=False, default=str, separators=(',', ':'))}]
        for attempt in range(2):
            messages = [dict(message, content=normalize_model_text(message['content'])) for message in messages]
            started = time.perf_counter()
            remaining = deadline - started
            if remaining <= 0:
                raise TimeoutError('Question deadline exceeded')
            record = {'role': role, 'model_id': self.model_id, 'format_attempt': attempt + 1,
                      'input_tokens': 0, 'output_tokens': 0, 'timeout_seconds': remaining,
                      'prompt_characters': sum(len(message['content']) for message in messages)}
            try:
                # Disable proxy inheritance: evidence stays on the loopback endpoint.
                with requests.Session() as session:
                    session.trust_env = False
                    response = session.post(self.base_url + '/v1/chat/completions', json={
                        'model': self.model_id, 'messages': messages, 'max_tokens': 4096,
                        'temperature': .2 if role in {'plan', 'sql', 'answer', 'repair'} else 0.,
                        'response_format': {'type': 'json_object', 'schema': SCHEMAS[role]} if role in SCHEMAS else {'type': 'json_object'}, 'stream': False,
                    }, timeout=(min(5., remaining), remaining))
                    response.raise_for_status()
                    result = response.json()
                usage = result.get('usage', {})
                record.update(input_tokens=usage.get('prompt_tokens', 0), output_tokens=usage.get('completion_tokens', 0))
                if isinstance(result.get('timings'), dict):
                    record['server_timings'] = {key: result['timings'][key] for key in
                                               ('prompt_ms', 'prompt_n', 'predicted_ms', 'predicted_n')
                                               if key in result['timings']}
                choice = result['choices'][0]
                if choice.get('finish_reason') == 'length':
                    raise ValueError('Model output truncated: max_tokens')
                content = choice['message']['content']
                try:
                    parsed = parse_json(content)
                    if role in SCHEMAS:
                        from jsonschema import validate
                        from jsonschema.exceptions import ValidationError
                        try:
                            validate(parsed, SCHEMAS[role])
                        except ValidationError as exc:
                            raise ValueError('Model output does not match the role schema') from exc
                    return parsed
                except ValueError as exc:
                    record['error'] = type(exc).__name__
                    if attempt:
                        raise ValueError(f'Model returned invalid JSON for {role} after 2 attempts') from exc
                    if content.strip():
                        messages.append({'role': 'assistant', 'content': content})
                    messages.append({'role': 'user', 'content': 'Return exactly one complete valid JSON object for the original task, preserving all findings. No text outside JSON.'})
            except requests.Timeout as exc:
                record['error'] = 'TimeoutError'
                raise TimeoutError('Local model request timed out') from exc
            except Exception as exc:
                record.setdefault('error', type(exc).__name__)
                raise
            finally:
                record['elapsed'] = time.perf_counter() - started
                self.calls.append(record)

    def config(self):
        return {'provider': 'llama.cpp', 'model_id': self.model_id, 'revision': REVISION,
                'artifact_sha256': MODEL_SHA256,
                'base_url': self.base_url, 'quantization': 'Q4_K_M',
                'generation_temperature': .2, 'review_temperature': 0.,
                'max_tokens': 4096, 'json_format_retries': 1, 'role_schema_version': 2, 'input_normalization': 'NFC', 'payload_serialization':'stage_payload_v2'}


def configured_llm(provider=None):
    provider = (provider or read_settings().get('AAVE_LLM_PROVIDER', 'bedrock')).lower()
    if provider == 'local_qwen':
        return LocalQwenLLM()
    if provider == 'bedrock':
        return BedrockLLM()
    raise ValueError('AAVE_LLM_PROVIDER must be bedrock or local_qwen')
