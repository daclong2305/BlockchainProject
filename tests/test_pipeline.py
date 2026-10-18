from pathlib import Path
import json
import pandas as pd


def fixture_db(tmp_path):
    from aave_analyst.database import Database, build_database
    markets = pd.DataFrame([dict(asset="USDC",hour="2026-08-01T00:00:00Z",supplied_usd=100.,borrowed_usd=40.,source_timestamp="2026-08-01T00:00:00Z",is_carried=False)])
    events = pd.DataFrame([dict(event_id=f"e{i}",tx_hash="0x1",time="2026-08-01T00:00:00Z",amount_usd=10.,market="m",log_index=i) for i in range(2)])
    path=tmp_path/"aave.duckdb"
    build_database(markets,events,path)
    return Database(path)


def test_repair_reexecutes_sql_and_replaces_old_evidence(tmp_path):
    from aave_analyst.pipeline import Analyst
    from aave_analyst.llm import ScriptedLLM
    from aave_analyst.models import Draft, QuerySpec
    from aave_analyst.retrieval import Retriever
    db=fixture_db(tmp_path)
    wrong="SELECT count(*) AS value FROM liquidation_events"
    correct="SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events"
    llm=ScriptedLLM({"sql_review":[{"issues":[]},{"issues":[]}],"claim_review":[{"issues":[]}],"repair":[{"sql":correct}],"answer":[{"answer":"Có 1 giao dịch [SQL1].", "claims":[{"text":"Có 1 giao dịch.","citations":["SQL1"],"numeric":{"value":1,"unit":"count","evidence_id":"SQL1","row":0,"column":"value"}}]}]})
    draft=Draft(question="Có bao nhiêu giao dịch thanh lý?",spec=QuerySpec(kind="data",metric="transactions",aggregation="count_distinct",unit="count"),sql=wrong,query_result=db.query(wrong),answer="Có 2 giao dịch.")
    result=Analyst(db,Retriever([]),llm).continue_draft(draft,"P")
    assert result.draft.sql==correct
    assert result.draft.query_result.rows[0]["value"]==1
    assert "1 giao dịch" in result.draft.answer
    assert result.repairs==1


def test_repair_budget_is_global_and_no_change_stops(tmp_path):
    from aave_analyst.pipeline import Analyst
    from aave_analyst.llm import ScriptedLLM
    from aave_analyst.models import Draft, QuerySpec
    from aave_analyst.retrieval import Retriever
    db=fixture_db(tmp_path)
    sql="SELECT count(*) AS value FROM liquidation_events"
    llm=ScriptedLLM({"sql_review":[{"issues":[]}],"repair":[{"sql":sql}]})
    draft=Draft(question="Số giao dịch?",spec=QuerySpec(kind="data",metric="transactions",aggregation="count_distinct"),sql=sql,query_result=db.query(sql),answer="Hai")
    result=Analyst(db,Retriever([]),llm).continue_draft(draft,"P")
    assert result.repairs<=2
    assert result.status=="unverified"
    assert any("unchanged" in x.get("event","") for x in result.trace)


def test_b0_uses_draft_without_llm_calls(tmp_path):
    from aave_analyst.pipeline import Analyst
    from aave_analyst.llm import ScriptedLLM
    from aave_analyst.models import Draft, QuerySpec
    from aave_analyst.retrieval import Retriever
    llm=ScriptedLLM({})
    draft=Draft(question="q",spec=QuerySpec(kind="docs"),answer="answer")
    result=Analyst(fixture_db(tmp_path),Retriever([]),llm).continue_draft(draft,"B0")
    assert result.draft.answer=="answer"
    assert llm.calls==[]


def test_numeric_claim_mismatch_and_missing_citation_fail(tmp_path):
    from aave_analyst.verification import verify_claims
    from aave_analyst.models import Draft,QuerySpec
    from aave_analyst.llm import ScriptedLLM
    db=fixture_db(tmp_path)
    draft=Draft(question="q",spec=QuerySpec(kind="data"),sql="SELECT 1 AS value",query_result=db.query("SELECT 1 AS value"),answer="Có 2 [SQL1]",claims=[{"text":"Có 2","citations":["SQL1"],"numeric":{"value":2,"evidence_id":"SQL1","row":0,"column":"value","unit":"count"}}])
    issues=verify_claims(draft,ScriptedLLM({"claim_review":[{"issues":[]}]}))
    assert any(i.code=="numeric_mismatch" for i in issues)


def test_benchmark_has_60_records_and_no_family_leakage(tmp_path):
    from aave_analyst.benchmark import create_benchmark,validate_benchmark
    rows=create_benchmark(fixture_db(tmp_path),[])
    assert len(rows)==60
    assert sum(r['split']=='dev' for r in rows)==20
    assert sum(r['split']=='test' for r in rows)==40
    validate_benchmark(rows,final=False)
    assert all(not r['review']['reviewer_1'] for r in rows)


def test_runner_reuses_draft_per_question_repeat(tmp_path):
    from aave_analyst.experiments import run_experiments
    from aave_analyst.models import Draft,QuerySpec,RunResult
    class Fake:
        calls=0
        def make_draft(self,q):
            self.calls+=1
            return Draft(question=q,spec=QuerySpec(kind='docs'),answer=f'draft-{self.calls}',elapsed=1.)
        def continue_draft(self,draft,mode):return RunResult(mode=mode,draft=draft,status='unchecked',elapsed=1.)
    fake=Fake()
    rows=[{'id':'q1','question':'q','split':'dev','family':'a','review':{'reviewer_1':'','reviewer_2':''}}]
    output=run_experiments(fake,rows,tmp_path/'runs',repeats=3,final=False,modes=['B0','P'])
    assert fake.calls==3
    assert len(output)==6
    for repeat in range(3):
        assert len({r['draft']['answer'] for r in output if r['repeat']==repeat})==1
