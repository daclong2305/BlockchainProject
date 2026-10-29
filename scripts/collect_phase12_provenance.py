import json, struct, urllib.request, urllib.error
from pathlib import Path
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parents[1] / 'docs/phase12-evidence'
OUT.mkdir(parents=True, exist_ok=True)

def fetch(name, url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers={'User-Agent': 'AaveResearchAudit/0.1'}), timeout=60) as response:
            status, body = response.status, response.read().decode()
    except urllib.error.HTTPError as exc:
        status, body = exc.code, exc.read().decode()
    (OUT / (name + '.json')).write_text(json.dumps({'url': url, 'collected_at': datetime.now(timezone.utc).isoformat(), 'status': status, 'body': body}, ensure_ascii=False, indent=2), encoding='utf-8')
    print(name, status)
    return json.loads(body) if status == 200 and body.startswith(('{', '[')) else body

if __name__ == '__main__':
    model = fetch('hf_model', 'https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF')
    rev = model['sha']
    fetch('hf_tree', f'https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF/tree/{rev}?recursive=true')
    fetch('hf_readme', f'https://huggingface.co/zhenlong54/qwen-vitext2sql-3b-GGUF/raw/{rev}/README.md')
    fetch('hf_search', 'https://huggingface.co/api/models?author=zhenlong54&search=qwen&limit=100')
    commits = fetch('hf_commits', 'https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF/commits/main')
    if isinstance(commits, list) and commits:
        fetch('hf_initial_tree', f"https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF/tree/{commits[-1]['id']}?recursive=true")
    for key, url in {
        'hf_discussions': 'https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF/discussions',
        'hf_global_search': 'https://huggingface.co/api/models?search=vitext2sql&limit=100',
        'hf_author_models': 'https://huggingface.co/api/models?author=zhenlong54&limit=100',
        'hf_author_spaces': 'https://huggingface.co/api/spaces?author=zhenlong54&limit=100',
        'hf_author_datasets': 'https://huggingface.co/api/datasets?author=zhenlong54&limit=100',
    }.items():
        fetch(key, url)
    candidate = fetch('hf_source_candidate', 'https://huggingface.co/api/models/Qwen/Qwen2.5-Coder-3B-Instruct')
    for filename, key in [('README.md', 'card'), ('LICENSE', 'license'), ('config.json', 'config'), ('tokenizer_config.json', 'tokenizer_config')]:
        fetch('hf_candidate_' + key, f"https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct/raw/{candidate['sha']}/{filename}")
    fetch('github_repo', 'https://api.github.com/repos/MSCA-DN-Digital-Finance/stablecoin-onchain-data')
    fetch('github_release', 'https://api.github.com/repos/MSCA-DN-Digital-Finance/stablecoin-onchain-data/releases/tags/data-2026-09-15')
    fetch('github_tree', 'https://api.github.com/repos/MSCA-DN-Digital-Finance/stablecoin-onchain-data/git/trees/main?recursive=1')
    fetch('github_readme', 'https://raw.githubusercontent.com/MSCA-DN-Digital-Finance/stablecoin-onchain-data/main/README.md')
    url = f'https://huggingface.co/zhenlong54/qwen-vitext2sql-3b-GGUF/resolve/{rev}/model-q4_k_m.gguf'
    limit = 8 * 1024 * 1024
    with urllib.request.urlopen(urllib.request.Request(url, headers={'Range': f'bytes=0-{limit-1}'}), timeout=60) as response:
        data = response.read(limit)
        status, content_range = response.status, response.headers.get('Content-Range')
    offset = 0
    def unpack(fmt):
        global offset
        size = struct.calcsize(fmt)
        result = struct.unpack_from(fmt, data, offset)[0]
        offset += size
        return result
    def string():
        global offset
        length = unpack('<Q')
        result = data[offset:offset+length].decode()
        offset += length
        return result
    def value(kind):
        if kind == 8:
            return string()
        if kind == 9:
            item_kind, length = unpack('<I'), unpack('<Q')
            for _ in range(length):
                value(item_kind)
            return {'length': length, 'item_type': item_kind}
        return unpack({0:'<B',1:'<b',2:'<H',3:'<h',4:'<I',5:'<i',6:'<f',7:'<?',10:'<Q',11:'<q',12:'<d'}[kind])
    assert unpack('<I') == 0x46554747
    version, tensors, count = unpack('<I'), unpack('<Q'), unpack('<Q')
    metadata = {}
    for _ in range(count):
        key = string()
        metadata[key] = value(unpack('<I'))
    result = {'url': url, 'collected_at': datetime.now(timezone.utc).isoformat(), 'http_status': status, 'content_range': content_range, 'bytes_fetched': len(data), 'metadata_bytes': offset, 'version': version, 'tensor_count': tensors, 'metadata_count': count, 'complete': True, 'metadata': metadata}
    (OUT / 'hf_gguf_header.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print('GGUF metadata', offset, 'bytes; no tensor weights saved')
