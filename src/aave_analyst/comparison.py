"""Explicit, on-demand model comparisons; never selects a winner automatically."""
from copy import deepcopy
from dataclasses import asdict
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from queue import Queue, Empty

from .database import Database
from .llm import BedrockLLM
from .local_llm import LocalQwenLLM
from .pipeline import Analyst, MODES
from .retrieval import Retriever

PROVIDERS = {'local_qwen': 'Qwen ViText2SQL 3B · local', 'bedrock': 'Claude Haiku 4.5 · Bedrock'}


def input_hashes(root):
    result = {}
    for name in ('data/processed/aave.duckdb', 'data/processed/dictionary.json', 'data/documents/chunks.json'):
        h = hashlib.sha256()
        with (Path(root) / name).open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                h.update(block)
        result[name] = h.hexdigest()
    return result


def run_comparison(root, question, mode, deadline=600.,progress=None):
    root = Path(root)
    if not question.strip() or mode not in MODES:
        raise ValueError('Question and a valid analysis mode are required')
    if not isinstance(deadline, (int, float)) or not math.isfinite(deadline) or deadline <= 0:
        raise ValueError('Deadline must be a finite positive number of seconds')
    before = input_hashes(root)
    chunks = json.loads((root / 'data/documents/chunks.json').read_text(encoding='utf-8'))
    record = {'id': uuid.uuid4().hex, 'created_at': datetime.now(timezone.utc).isoformat(),
              'question': question.strip(), 'mode': mode, 'deadline_seconds_per_model': float(deadline),
              'execution': 'parallel', 'input_hashes': before,
              'code_hashes': {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(Path(__file__).parent.glob('*.py'))},
              'results': {}}
    events=Queue()
    def run_provider(provider):
        started = time.perf_counter()
        def emit(event):
            events.put(dict(event,provider=provider,elapsed_seconds=time.perf_counter()-started))
        emit({'event':'model_started'})
        llm = None
        item = {'provider': provider}
        try:
            llm = LocalQwenLLM() if provider == 'local_qwen' else BedrockLLM()
            item['config'] = llm.config()
            analyst = Analyst(Database(root / 'data/processed/aave.duckdb'), Retriever(deepcopy(chunks)), llm, deadline=deadline)
            analyst.progress=emit
            item['result'] = asdict(analyst.answer(record['question'], mode))
        except Exception as exc:
            # Keep a failed side visible while still attempting the other model.
            # Exceptions may contain service detail: only the type is displayed.
            item['error'] = type(exc).__name__
        finally:
            usage = llm.calls if llm is not None else []
            item['calls'] = deepcopy(usage)
            item.update(wall_seconds=time.perf_counter() - started,
                        input_tokens=sum(c.get('input_tokens', 0) for c in usage),
                        output_tokens=sum(c.get('output_tokens', 0) for c in usage),
                        model_calls=len(usage))
        emit({'event':'model_finished','status':item.get('result',{}).get('status','error')})
        return item
    comparison_started=time.perf_counter()
    # Worker threads never touch Streamlit. Deliver progress on the caller thread.
    with ThreadPoolExecutor(max_workers=2,thread_name_prefix='model-comparison') as pool:
        futures={provider:pool.submit(run_provider,provider) for provider in PROVIDERS}
        while not all(future.done() for future in futures.values()) or not events.empty():
            try:event=events.get(timeout=.1)
            except Empty:continue
            if progress:progress(event)
        record['results']={provider:future.result() for provider,future in futures.items()}
    record['wall_seconds']=time.perf_counter()-comparison_started
    try:
        after = input_hashes(root)
        record['inputs_unchanged'] = before == after
        record['input_hashes_after'] = after
    except OSError as exc:
        record['inputs_unchanged'] = False
        record['snapshot_error'] = type(exc).__name__
    try:
        folder = root / 'runs/comparisons'
        folder.mkdir(parents=True, exist_ok=True)
        (folder / (record['id'] + '.json')).write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
    except OSError as exc:
        record['log_error'] = type(exc).__name__
    return record
