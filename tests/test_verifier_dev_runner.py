from dataclasses import asdict
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from aave_analyst.models import Draft, QuerySpec, RunResult


def load_runner():
    path = Path(__file__).resolve().parents[1] / 'scripts/run_verifier_dev.py'
    spec = importlib.util.spec_from_file_location('verifier_dev_runner', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_external_candidates_are_saved_and_resume_reuses_generated_drafts(tmp_path, monkeypatch):
    runner = load_runner()
    monkeypatch.setattr(runner, '__file__', str(tmp_path / 'scripts/run_verifier_dev.py'))
    for name in ('data/benchmark/questions.jsonl', 'data/processed/aave.duckdb',
                 'data/documents/chunks.json'):
        path = tmp_path / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text('fixture', encoding='utf-8')
    records = [dict(id=qid, question=qid, split='dev', category='lookup') for qid in ('Q1', 'Q2')]
    draft = Draft(question='Q1', spec=QuerySpec(), answer='saved answer')
    source = tmp_path / 'source.jsonl'
    source.write_text(json.dumps(dict(question_id='Q1', draft=asdict(draft))) + '\n', encoding='utf-8')
    generated, continued = [], []

    def make_draft(question):
        generated.append(question)
        return Draft(question=question, spec=QuerySpec(), answer='generated answer')

    def continue_draft(candidate, mode):
        continued.append(candidate.question)
        return RunResult(mode, candidate, 'unchecked')

    analyst = SimpleNamespace(llm=SimpleNamespace(config=lambda: {}),
                              make_draft=make_draft, continue_draft=continue_draft)
    monkeypatch.setattr(runner, 'analyst_at', lambda *args, **kwargs: analyst)
    monkeypatch.setattr(runner, 'load_benchmark', lambda path: records)
    monkeypatch.setattr(runner, 'code_hashes', lambda: {})
    monkeypatch.setattr(runner.time, 'sleep', lambda seconds: None)
    monkeypatch.setattr('aave_analyst.research_runtime.MeteredLLM', lambda inner, *args, **kwargs: inner)
    out = tmp_path / 'run'
    monkeypatch.setattr(runner.sys, 'argv', ['runner', '--out', str(out), '--candidates', str(source), '--modes', 'B0'])
    runner.main()
    runner.main()
    saved = runner.load_candidates(out / 'candidates.jsonl')
    assert set(saved) == {'Q1', 'Q2'}
    assert saved['Q1']['draft'] == asdict(draft)
    assert generated == ['Q2']
    assert continued == ['Q1', 'Q2']
    assert len((out / 'candidates.jsonl').read_text(encoding='utf-8').splitlines()) == 2


def test_conflicting_candidates_are_rejected(tmp_path):
    runner = load_runner()
    saved, source = tmp_path / 'saved.jsonl', tmp_path / 'source.jsonl'
    for path, answer in ((saved, 'old'), (source, 'changed')):
        path.write_text(json.dumps(dict(question_id='Q1', draft={'answer': answer})) + '\n', encoding='utf-8')
    with pytest.raises(ValueError, match='Candidate changed'):
        runner.candidate_sources(saved, source)
