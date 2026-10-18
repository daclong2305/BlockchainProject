from pathlib import Path
from datetime import date, datetime
from decimal import Decimal
import threading
import time
import duckdb
import sqlglot
from sqlglot import exp
from .models import QueryResult

TABLES = {"market_hourly", "liquidation_events", "coverage"}


def validate_sql(sql: str):
    trees = sqlglot.parse(sql, read="duckdb")
    if len(trees)!=1 or not isinstance(trees[0], exp.Query):
        raise ValueError("Only one SELECT/CTE query is allowed")
    tree=trees[0]
    ctes={c.alias_or_name.lower() for c in tree.find_all(exp.CTE)}
    for table in tree.find_all(exp.Table):
        if not isinstance(table.this, exp.Identifier) or table.name.lower() not in TABLES|ctes or table.db or table.catalog:
            raise ValueError("Query refers to a table/function outside the allowlist")
    # Table-valued functions and file/system functions are not research tools.
    for f in tree.find_all(exp.Func):
        name=f.name.lower() if isinstance(f,exp.Anonymous) else f.sql_name().lower()
        if any(s in name for s in ("read_","scan","http","query","pragma","getenv","write","system","setting")):
            raise ValueError("External and system functions are forbidden")
    if tree.find(exp.Into):
        raise ValueError("SELECT INTO is forbidden")
    return tree


def build_database(markets, events, path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with duckdb.connect(str(path)) as con:
        con.execute("SET TimeZone='UTC'")
        con.register("markets_df",markets);con.register("events_df",events)
        con.execute("CREATE OR REPLACE TABLE market_hourly AS SELECT * REPLACE (CAST(hour AS TIMESTAMPTZ) AS hour, CAST(source_timestamp AS TIMESTAMPTZ) AS source_timestamp) FROM markets_df")
        con.execute("CREATE OR REPLACE TABLE liquidation_events AS SELECT * REPLACE (CAST(time AS TIMESTAMPTZ) AS time) FROM events_df")
        con.execute("CREATE OR REPLACE TABLE coverage AS SELECT asset, min(hour) AS start_utc, max(hour) AS end_utc, count(*) AS rows, count(DISTINCT hour) AS observed_hours FROM market_hourly GROUP BY asset")


def _json_value(x):
    if isinstance(x,(datetime,date)):return x.isoformat()
    if isinstance(x,Decimal):return str(x)
    return x


class Database:
    def __init__(self,path):self.path=Path(path);self.calls=[]

    def query(self,sql,timeout=15.,max_rows=200):
        start=time.perf_counter();record={'tool':'sql','sql':sql,'started':start}
        try:
            result=self._query(sql,timeout,max_rows)
            record.update(returned_rows=len(result.rows),truncated=result.truncated)
            return result
        except Exception as exc:
            record['error']=type(exc).__name__;raise
        finally:
            record['elapsed']=time.perf_counter()-start;self.calls.append(record)

    def _query(self,sql,timeout=15.,max_rows=200):
        validate_sql(sql)
        if not self.path.exists():raise FileNotFoundError(f"Build database first: {self.path}")
        con=duckdb.connect(str(self.path),read_only=True)
        timer=None
        try:
            con.execute("SET TimeZone='UTC'")
            con.execute("SET enable_external_access=false")
            timer=threading.Timer(max(.01,timeout),con.interrupt);timer.daemon=True;timer.start()
            cur=con.execute(sql)
            names=[c[0] for c in cur.description]
            # LIMIT is not injected into SQL, so aggregates are never altered.
            values=cur.fetchmany(max_rows+1)
            return QueryResult(names,[dict(zip(names,map(_json_value,row))) for row in values[:max_rows]],len(values)>max_rows,len(values))
        finally:
            if timer:timer.cancel();timer.join()
            con.close()

    def schema(self):
        with duckdb.connect(str(self.path),read_only=True) as con:
            return {name:con.execute(f'DESCRIBE {name}').fetchall() for name in sorted(TABLES)}
