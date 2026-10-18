import json
from dataclasses import asdict
import pytest


def test_factual_score_does_not_require_same_sql_alias():
    from aave_analyst.evaluation import factual_score
    gold={"expected_numeric":[{"column":"value","row":0,"unit":"USD","value":100.}]}
    result={"draft":{"claims":[{"text":"100 USD","numeric":{"column":"debt","row":0,"unit":"USD","value":100.}}]}}
    assert factual_score(gold,result) is True


def test_single_snapshot_outside_coverage_is_detected(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.verification import coverage_rules
    from aave_analyst.models import QuerySpec
    spec=QuerySpec(kind="data",assets=["USDC"],start="2027-01-01",end="2027-02-01")
    assert any(i.action=="stop" for i in coverage_rules(fixture_db(tmp_path),spec))


def test_hard_deadline_returns_error_without_calling_model(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.pipeline import Analyst
    from aave_analyst.llm import ScriptedLLM
    from aave_analyst.retrieval import Retriever
    from aave_analyst.models import Draft,QuerySpec
    llm=ScriptedLLM({})
    result=Analyst(fixture_db(tmp_path),Retriever([]),llm,deadline=1).continue_draft(Draft(question="q",spec=QuerySpec(),elapsed=2),"P")
    assert result.status=="error"
    assert "TimeoutError" in result.error
    assert not llm.calls


def test_cli_help_and_doctor_do_not_call_inference(capsys):
    from aave_analyst.cli import main
    main(["doctor"])
    output=capsys.readouterr().out
    assert "model_id" in output
    assert "credentials_available" in output


def test_stress_dataset_is_separate_and_has_five_error_types(tmp_path):
    from test_pipeline import fixture_db
    from aave_analyst.stress import create_stress
    rows=create_stress(fixture_db(tmp_path))
    assert len(rows)==20
    assert len({r['error_type'] for r in rows})==5
    assert sum(r['split']=='test' for r in rows)==10
    assert all(r['review']['approved'] is False for r in rows)
