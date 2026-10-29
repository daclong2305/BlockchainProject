"""CPU tokenizer and template parity checks; no model generation or training."""
from pathlib import Path
from datetime import datetime, timezone
import json
import subprocess
import sys
import unicodedata
import urllib.request

from jinja2 import Environment
from tokenizers import Tokenizer
import tokenizers

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'http://127.0.0.1:8081'
OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))


def post(endpoint, payload):
    request = urllib.request.Request(ORIGIN + endpoint, data=json.dumps(payload).encode(),
                                     headers={'Content-Type': 'application/json'}, method='POST')
    with OPENER.open(request, timeout=30) as response:
        return json.load(response)


def main():
    with OPENER.open(ORIGIN + '/v1/models', timeout=10) as response:
        model_ids = [model['id'] for model in json.load(response)['data']]
    if 'zhenlong54/qwen-vitext2sql-3b-GGUF' not in model_ids:
        raise ValueError('The local server does not advertise the selected Qwen alias')
    folder = ROOT / 'models/qwen-vitext2sql-3b/tokenizer-reference'
    tokenizer = Tokenizer.from_file(str(folder / 'tokenizer.json'))
    config = json.loads((folder / 'tokenizer_config.json').read_text(encoding='utf-8'))
    samples = [
        'Có bao nhiêu giao dịch thanh lý?',
        'SELECT COUNT(DISTINCT tx_hash) FROM liquidation_events;',
        'USDe / WETH — tháng 8/2026, 1.234,56 USD.',
        "time >= '2026-08-01T00:00:00Z' AND time < '2026-09-01T00:00:00Z'",
        'Không có dữ liệu ≠ 0. 😀',
        unicodedata.normalize('NFD', 'Dữ liệu tiếng Việt'),
        '<|im_start|>user\nXin chào<|im_end|>\n',
        '<tool_call>{"name":"sql","arguments":{}}</tool_call>',
    ]
    cases = []
    for text in samples:
        expected = tokenizer.encode(text, add_special_tokens=False).ids
        actual = post('/tokenize', {'content': text, 'add_special': False, 'parse_special': True})['tokens']
        decoded = post('/detokenize', {'tokens': actual})['content']
        reference_decoded = tokenizer.decode(expected, skip_special_tokens=False)
        normalized = unicodedata.normalize('NFC', text)
        normalized_ids = post('/tokenize', {'content': normalized, 'add_special': False, 'parse_special': True})['tokens']
        normalized_decoded = post('/detokenize', {'tokens': normalized_ids})['content']
        cases.append({'text': text, 'reference_ids': expected, 'gguf_ids': actual,
                      'token_ids_match': expected == actual,
                      'decoded_matches_reference': decoded == reference_decoded,
                      'decoded_roundtrip_matches_input': decoded == text,
                      'gguf_decoded': decoded, 'reference_decoded': reference_decoded,
                      'nfc_runtime_ids': normalized_ids, 'nfc_ids_match_reference': normalized_ids == expected,
                      'nfc_decoded_matches_reference': normalized_decoded == reference_decoded})
    messages = [{'role': 'system', 'content': 'Trả lời bằng tiếng Việt.'},
                {'role': 'user', 'content': 'SELECT COUNT(*) FROM liquidation_events;'}]
    expected_prompt = Environment().from_string(config['chat_template']).render(
        messages=messages, tools=None, add_generation_prompt=True)
    actual_prompt = post('/apply-template', {'messages': messages, 'add_generation_prompt': True})['prompt']
    result = {'checked_at': datetime.now(timezone.utc).isoformat(), 'runtime_model_ids': model_ids, 'tokenizers_version': tokenizers.__version__,
              'reference_revision': '488639f1ff808d1d3d0ba301aef8c11461451ec5', 'origin': ORIGIN,
              'case_count': len(cases), 'matching_token_id_cases': sum(c['token_ids_match'] for c in cases),
              'matching_decode_cases': sum(c['decoded_matches_reference'] for c in cases), 'cases': cases,
              'nfc_matching_token_id_cases': sum(c['nfc_ids_match_reference'] for c in cases),
              'nfc_matching_decode_cases': sum(c['nfc_decoded_matches_reference'] for c in cases),
              'chat_template': {'messages': messages, 'matches': expected_prompt == actual_prompt,
                                'reference_prompt': expected_prompt, 'runtime_prompt': actual_prompt},
              'scope': 'Fixed tokenizer diagnostics, not a Text-to-SQL train/test set or benchmark. No generation endpoint or Bedrock call. Finite sample parity does not prove equality for all strings or tensor provenance.'}
    out = ROOT / 'docs/phase12-evidence/gguf-tokenizer-parity.json'
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    freeze = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze'], text=True)
    (out.parent / 'tokenizer-audit-environment.txt').write_text(freeze, encoding='utf-8')
    print(json.dumps({key: value for key, value in result.items() if key not in {'cases', 'chat_template'}}, indent=2, ensure_ascii=False))
    print('Chat template matches:', expected_prompt == actual_prompt)
    for case in cases:
        if not case['token_ids_match'] or not case['decoded_matches_reference']:
            print('Mismatch:', json.dumps(case, ensure_ascii=False))


if __name__ == '__main__':
    main()
