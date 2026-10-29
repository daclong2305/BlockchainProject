"""One live local SQL smoke check; does not create or run a benchmark."""
import json
from pathlib import Path
from aave_analyst.database import Database
from aave_analyst.data import DICTIONARY
from aave_analyst.local_llm import LocalQwenLLM

ROOT = Path(__file__).resolve().parents[1]


if __name__ == '__main__':
    database = Database(ROOT / 'data/processed/aave.duckdb')
    llm = LocalQwenLLM()
    question = 'Trong bộ dữ liệu hiện có, có bao nhiêu giao dịch thanh lý trong tháng 8 năm 2026?'
    payload = {'question': question, 'schema': database.schema(), 'dictionary': DICTIONARY}
    record = {'question': question, 'model': llm.config(), 'matches_reference_values': False,
              'scope': 'Single local inference smoke test; not a benchmark or training example'}
    try:
        generated = llm.complete('sql', payload, timeout=180.)
        record['sql'] = generated['sql']
        result = database.query(generated['sql'])
        reference = database.query("SELECT COUNT(DISTINCT tx_hash) AS transactions FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01 00:00:00+00' AND time < TIMESTAMPTZ '2026-09-01 00:00:00+00'")
        actual = [list(row.values()) for row in result.rows]
        expected = [list(row.values()) for row in reference.rows]
        record.update(rows=result.rows, reference_rows=reference.rows, matches_reference_values=actual == expected)
        if actual != expected:
            raise ValueError('Generated SQL result differs from the independent query')
    except Exception as exc:
        record['error'] = f'{type(exc).__name__}: {exc}'
        raise
    finally:
        record['calls'] = llm.calls
        from datetime import datetime, timezone
        stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
        out = ROOT / f'docs/phase12-evidence/local-qwen-smoke-{stamp}.json'
        out.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(record, ensure_ascii=False, indent=2))
