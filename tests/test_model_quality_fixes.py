from aave_analyst.sql_normalization import normalize_datetime_quotes
from aave_analyst.pipeline import Analyst
from aave_analyst.models import Draft,QuerySpec


def test_asset_identifier_mistake_is_repaired_only_in_asset_equality():
    sql,changes=normalize_datetime_quotes('SELECT AVG("borrowed_usd") FROM market_hourly WHERE "asset" = "usdc"')
    assert "'USDC'" in sql and changes
    original='SELECT "usdc" FROM market_hourly'
    assert normalize_datetime_quotes(original)==(original,[])


def test_query_failure_cannot_generate_unbacked_number():
    class NoModel:
        def complete(self,*args,**kwargs):raise AssertionError('No numeric generation without query result')
    analyst=Analyst(None,None,NoModel())
    draft=Draft(question='Average?',spec=QuerySpec(kind='data'),sql='SELECT bad')
    analyst._answer(draft,0)
    assert draft.refused and not draft.claims


def test_final_sql_review_prompt_retains_average_policy():
    from aave_analyst.llm import PROMPTS
    assert 'Stock semantics prohibit SUM across time, not AVG' in PROMPTS['sql_review']
    assert 'question_anchors' in PROMPTS['sql_review']
