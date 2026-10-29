from pathlib import Path
import hashlib, json, platform, subprocess
from datetime import datetime, timezone
import duckdb

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/phase12-evidence'

def digest(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

if __name__ == '__main__':
    con = duckdb.connect(str(ROOT / 'data/processed/aave.duckdb'), read_only=True)
    con.execute("SET TimeZone='UTC'")
    def rows(sql):
        cursor = con.execute(sql)
        return [dict(zip([c[0] for c in cursor.description], row)) for row in cursor.fetchall()]
    report = {'collected_at': datetime.now(timezone.utc).isoformat(), 'python': platform.python_version(), 'platform': platform.platform(), 'timezone': rows("SELECT current_setting('TimeZone') AS timezone"), 'schema': rows('DESCRIBE market_hourly') + rows('DESCRIBE liquidation_events')}
    report['market'] = rows('''SELECT asset, count(*) AS rows, min(hour) AS start_utc, max(hour) AS end_utc,
      count(*)-count(DISTINCT hour) AS duplicate_hours,
      date_diff('hour',min(hour),max(hour))+1-count(DISTINCT hour) AS internal_missing_hours,
      count(*) FILTER (WHERE hour != date_trunc('hour',hour)) AS unaligned_hours,
      count(*) FILTER (WHERE supplied_usd IS NULL) AS null_supplied,
      count(*) FILTER (WHERE borrowed_usd IS NULL) AS null_borrowed,
      count(*) FILTER (WHERE source_timestamp IS NULL) AS null_source_time,
      count(*) FILTER (WHERE is_carried) AS carried_hours,
      count(DISTINCT source_timestamp) AS distinct_observations,
      min(source_age_hours) AS min_age_hours, max(source_age_hours) AS max_age_hours,
      count(*) FILTER (WHERE source_age_hours<0) AS future_observations
      FROM market_hourly GROUP BY asset ORDER BY asset''')
    report['events'] = rows('''SELECT count(*) AS events, count(DISTINCT tx_hash) AS transactions,
      count(*)-count(DISTINCT event_id) AS duplicate_event_ids,
      count(*)-count(DISTINCT (tx_hash,log_index)) AS duplicate_tx_log,
      min(time) AS start_utc,max(time) AS end_utc,
      count(*) FILTER (WHERE time IS NULL) AS null_time,
      count(*) FILTER (WHERE amount_usd IS NULL) AS null_amount,
      count(*) FILTER (WHERE tx_hash IS NULL OR tx_hash IN ('nan','None','')) AS invalid_tx,
      count(*) FILTER (WHERE event_id IS NULL OR event_id IN ('nan','None','')) AS invalid_id,
      count(*) FILTER (WHERE log_index IS NULL) AS null_log_index
      FROM liquidation_events''')
    report['carried_flag_mismatches'] = rows('''SELECT count(*) AS mismatches FROM (
      SELECT *, row_number() OVER (PARTITION BY asset,source_timestamp ORDER BY hour)>1 AS expected_carried
      FROM market_hourly) WHERE is_carried != expected_carried''')
    report['benchmark_market'] = rows("SELECT asset,count(*) AS rows FROM market_hourly WHERE hour>='2025-01-01T00:00:00Z' AND hour<'2026-09-01T00:00:00Z' GROUP BY asset ORDER BY asset")
    report['benchmark_events'] = rows("SELECT count(*) AS events,count(DISTINCT tx_hash) AS transactions FROM liquidation_events WHERE time>='2025-01-01T00:00:00Z' AND time<'2026-09-01T00:00:00Z'")
    con.close()
    release = json.loads(json.loads((OUT/'github_release.json').read_text(encoding='utf-8'))['body'])
    expected = next(a['digest'].split(':')[1] for a in release['assets'] if a['name']=='aave_data.zip')
    actual = digest(ROOT/'data/raw/aave_data.zip')
    report['archive_digest'] = {'expected': expected, 'actual': actual, 'match': expected == actual}
    assert expected == actual, 'Release archive digest mismatch'
    assert all(r['duplicate_hours']==r['future_observations']==r['unaligned_hours']==r['internal_missing_hours']==0 for r in report['market'])
    assert report['events'][0]['duplicate_event_ids']==report['events'][0]['duplicate_tx_log']==0
    assert report['carried_flag_mismatches'][0]['mismatches']==0
    assert all(r['null_supplied']==r['null_borrowed']==r['null_source_time']==0 for r in report['market'])
    assert all(report['events'][0][k]==0 for k in ['null_time','null_amount','invalid_tx','invalid_id','null_log_index'])
    (OUT/'local_audit.json').write_text(json.dumps(report,indent=2,ensure_ascii=False,default=str),encoding='utf-8')
    files = sorted(p for base in ['data/raw','data/processed','data/documents'] for p in (ROOT/base).rglob('*') if p.is_file())
    manifest = [{'path':p.relative_to(ROOT).as_posix(),'bytes':p.stat().st_size,'sha256':digest(p)} for p in files]
    (OUT/'hash_manifest.json').write_text(json.dumps({'collected_at':report['collected_at'],'files':manifest},indent=2),encoding='utf-8')
    (OUT/'environment-freeze.txt').write_text(subprocess.check_output([__import__('sys').executable,'-m','pip','freeze'],text=True),encoding='utf-8')
    print(json.dumps(report,indent=2,default=str))
