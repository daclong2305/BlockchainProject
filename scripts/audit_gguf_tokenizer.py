"""Compare the selected GGUF's embedded tokenizer with a pinned public candidate.

This checks tokenizer metadata, not equality or provenance of tensor weights.
"""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import struct
import requests

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = 'Qwen/Qwen2.5-Coder-3B-Instruct'
REVISION = '488639f1ff808d1d3d0ba301aef8c11461451ec5'


def fingerprint(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, separators=(',', ':')).encode()).hexdigest()


def read_metadata(path):
    with path.open('rb') as stream:
        def unpack(fmt):
            return struct.unpack(fmt, stream.read(struct.calcsize(fmt)))[0]

        def string():
            return stream.read(unpack('<Q')).decode('utf-8')

        def value(kind):
            if kind == 8:
                return string()
            if kind == 9:
                item_kind, count = unpack('<I'), unpack('<Q')
                return [value(item_kind) for _ in range(count)]
            return unpack({0:'<B',1:'<b',2:'<H',3:'<h',4:'<I',5:'<i',6:'<f',7:'<?',10:'<Q',11:'<q',12:'<d'}[kind])

        assert unpack('<I') == 0x46554747
        version, tensors, count = unpack('<I'), unpack('<Q'), unpack('<Q')
        metadata = {}
        for _ in range(count):
            name = string()
            metadata[name] = value(unpack('<I'))
        return metadata, {'version': version, 'tensors': tensors, 'metadata_bytes': stream.tell()}


def main():
    model = ROOT / 'models/qwen-vitext2sql-3b/model-q4_k_m.gguf'
    model_hash = hashlib.sha256()
    with model.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            model_hash.update(block)
    actual_model_hash = model_hash.hexdigest()
    if actual_model_hash != 'b34a028bc6c18d738b57552423bb75ca555d823c19722c4261acc792547a4cd2':
        raise ValueError('Selected GGUF whole-file SHA-256 mismatch')
    folder = ROOT / 'models/qwen-vitext2sql-3b/tokenizer-reference'
    folder.mkdir(parents=True, exist_ok=True)
    reference_files = {}
    for filename in ('tokenizer.json', 'tokenizer_config.json'):
        path = folder / filename
        url = f'https://huggingface.co/{CANDIDATE}/resolve/{REVISION}/{filename}'
        if not path.exists():
            response = requests.get(url, timeout=(15, 90))
            response.raise_for_status()
            # Parse before saving; do not mistake an HTML error page for tokenizer JSON.
            response.json()
            path.write_bytes(response.content)
        reference_files[filename] = {'url': url, 'bytes': path.stat().st_size,
                                    'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}
    tokenizer = json.loads((folder / 'tokenizer.json').read_text(encoding='utf-8'))
    config = json.loads((folder / 'tokenizer_config.json').read_text(encoding='utf-8'))
    metadata, header = read_metadata(model)
    tokens = metadata['tokenizer.ggml.tokens']
    by_id = {i: token for token, i in tokenizer['model']['vocab'].items()}
    for item in tokenizer.get('added_tokens', []):
        if item['id'] in by_id and by_id[item['id']] != item['content']:
            raise ValueError('Conflicting vocabulary IDs in reference tokenizer')
        by_id[item['id']] = item['content']
    mismatches = [{'id': i, 'reference': token, 'gguf': tokens[i] if i < len(tokens) else None}
                  for i, token in by_id.items() if i >= len(tokens) or tokens[i] != token]
    merges = [' '.join(pair) if isinstance(pair, list) else pair for pair in tokenizer['model']['merges']]
    actual_merges = metadata['tokenizer.ggml.merges']
    unassigned_ids = [i for i in range(len(tokens)) if i not in by_id]
    types = metadata['tokenizer.ggml.token_type']
    specials = {str(i): {'reference': item['content'], 'reference_special': item.get('special'),
                        'gguf_type': types[i], 'content_matches': tokens[i] == item['content']}
                for i, item in ((item['id'], item) for item in tokenizer.get('added_tokens', [])) if i < len(tokens)}
    result = {'collected_at': datetime.now(timezone.utc).isoformat(), 'gguf_sha256': actual_model_hash, 'reference_candidate': CANDIDATE,
              'reference_revision': REVISION, 'reference_files': reference_files, 'gguf_header': header,
              'gguf_token_count': len(tokens), 'reference_assigned_ids': len(by_id),
              'mismatched_assigned_ids': len(mismatches), 'mismatch_examples': mismatches[:10],
              'gguf_unassigned_reference_ids': len(unassigned_ids),
              'unassigned_tokens_all_named_padding': all(tokens[i] == f'[PAD{i}]' for i in unassigned_ids),
              'extra_token_examples': [{'id': i, 'token': tokens[i]} for i in unassigned_ids[:10]],
              'merges_match_exactly': merges == actual_merges,
              'reference_merge_count': len(merges), 'gguf_merge_count': len(actual_merges),
              'reference_merges_sha256': fingerprint(merges), 'gguf_merges_sha256': fingerprint(actual_merges),
              'chat_template_matches_exactly': config.get('chat_template') == metadata.get('tokenizer.chat_template'),
              'reference_chat_template_sha256': fingerprint(config.get('chat_template')),
              'gguf_chat_template_sha256': fingerprint(metadata.get('tokenizer.chat_template')),
              'gguf_tokens_sha256': fingerprint(tokens), 'added_token_comparison': specials,
              'gguf_special_ids': {k: v for k, v in metadata.items() if k.startswith('tokenizer.ggml.') and k.endswith('_token_id')},
              'limitation': 'Matching tokenizer metadata does not prove weights, fine-tune dataset or exact Transformers checkpoint provenance. Token IDs unassigned in reference are reported without assuming equivalence.'}
    output = ROOT / 'docs/phase12-evidence/gguf-tokenizer-audit.json'
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k not in {'added_token_comparison', 'reference_files'}}, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
