"""Replay three known dev regression pairs against an explicit verifier."""
import argparse
import hashlib
import json
import subprocess
import sys
from copy import deepcopy
from importlib.resources import files
from pathlib import Path
from tempfile import TemporaryDirectory

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'runs/claude-full-20261110-retry-v1/replay_candidates.jsonl'
BASELINE = '00c04088f9886718c4ae179a457db362ee88c9eb'


def regression_cases(db):
    from run_verifier_dev import restore
    wanted = {'Q030', 'E-missing_citation-0-correct', 'E-missing_citation-0-wrong'}
    originals = {}
    for line in SOURCE.read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        if row['id'] in wanted:
            originals[row['id']] = restore(row['draft'])
    yield 'health-factor', originals['E-missing_citation-0-correct']
    yield 'health-factor-no-citation', originals['E-missing_citation-0-wrong']
    august = originals['Q030']
    yield 'observed-interval', august
    future = deepcopy(august)
    future.question = future.question.replace('2026-08', '2026-10')
    future.spec.start, future.spec.end = '2026-10-01T00:00:00Z', '2026-11-01T00:00:00Z'
    future.spec.retrieval_query = future.spec.retrieval_query.replace('August', 'October')
    future.sql = future.sql.replace('2026-08-01', '2026-10-01').replace('2026-09-01', '2026-11-01')
    future.query_result = db.query(future.sql)
    future.answer = 'Không có giá trị trong kết quả truy vấn cho khoảng đã hỏi [SQL1].'
    future.claims = [{'text': future.answer, 'citations': ['SQL1']}]
    yield 'beyond-observations', future
    yield 'source-sql', august
    other_asset = deepcopy(august)
    other_asset.sql = august.sql.replace("'USDe'", "'WETH'")
    other_asset.query_result = db.query(other_asset.sql)
    claim = other_asset.claims[0]
    numeric = claim['numeric']
    old = f"{numeric['value']:,.2f}"
    numeric['value'] = round(other_asset.query_result.rows[0][numeric['column']], 2)
    new = f"{numeric['value']:,.2f}"
    other_asset.answer = other_asset.answer.replace(old, new)
    claim['text'] = claim['text'].replace(old, new)
    yield 'source-other-asset', other_asset


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out', required=True, type=Path)
    parser.add_argument('--verifier', choices=['full', 'rules'], default='full')
    parser.add_argument('--provider', choices=['local_qwen', 'bedrock'], default='local_qwen')
    parser.add_argument('--baseline', action='store_true', help='Load pre-fix checker from the recorded Git revision')
    args = parser.parse_args()
    with TemporaryDirectory() as tmp:
        if args.baseline:
            archive = Path(tmp) / 'baseline.zip'
            subprocess.run(['git', 'archive', '--format=zip', '-o', str(archive), BASELINE,
                            'src/aave_analyst'], cwd=ROOT, check=True)
            sys.path.insert(0, str(archive / 'src'))
        else:
            sys.path.insert(0, str(ROOT / 'src'))
        replay(args)


def replay(args):
    from aave_analyst.cli import analyst_at
    from aave_analyst.verifier_replay import verify_candidate
    from aave_analyst.research_runtime import MeteredLLM

    analyst = analyst_at(ROOT, provider=args.provider)
    if args.provider == 'bedrock' and args.verifier != 'rules':
        if analyst.llm.region != 'us-east-1':
            raise ValueError('These six dev cases are scoped to the us-east-1 endpoint')
        if args.out.exists():
            raise FileExistsError(args.out)
        analyst.llm = MeteredLLM(analyst.llm, args.out.with_suffix('.calls.jsonl'), pace=6., cap=1.25)
    package = files('aave_analyst')
    checker_hashes = {name: hashlib.sha256(package.joinpath(name).read_bytes()).hexdigest()
                      for name in ['verification.py', 'verifier_replay.py', 'llm.py', 'response_schemas.py']}
    args.out.parent.mkdir(exist_ok=True, parents=True)
    with args.out.open('x', encoding='utf-8') as stream:
        for case, draft in regression_cases(analyst.db):
            result = verify_candidate(draft, analyst, args.verifier, deadline=120)
            row = dict(result, case=case, model=analyst.llm.config(), checker_hashes=checker_hashes,
                       fixture_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest())
            stream.write(json.dumps(row, ensure_ascii=False, default=str) + '\n')
            stream.flush()
            print(case, result['execution_status'], result['verdict'], flush=True)
            if result['execution_status'] != 'completed':
                raise SystemExit(result['error'])


if __name__ == '__main__':
    main()
