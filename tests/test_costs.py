from aave_analyst.costs import usage_cost,experiment_costs


def test_geo_price_not_global_and_unknown_model_not_guessed():
    config={'model_id':'us.anthropic.claude-haiku-4-5-20251001-v1:0','region':'us-east-1','provider':'bedrock'}
    assert usage_cost([{'input_tokens':1000000,'output_tokens':1000000}],config)['estimated_api_usd']==6.6
    assert usage_cost([],dict(config,model_id='other'))['estimated_api_usd'] is None


def test_shared_draft_is_charged_once_physically():
    config={'llm':{'provider':'bedrock','model_id':'us.anthropic.claude-haiku-4-5-20251001-v1:0','region':'us-east-1'}}
    initial=[{'input_tokens':100,'output_tokens':10}]
    results=[{'mode':mode,'shared_draft_id':'q-R0','draft':{'usage':initial},'usage':initial+[{'input_tokens':20,'output_tokens':2}]} for mode in ('B0','P')]
    report=experiment_costs(results,[],config)
    assert report['runtime_physical']['input_tokens']==140
    assert sum(row['input_tokens'] for row in report['per_configuration'].values())==240


def test_local_api_zero_does_not_claim_free_hardware():
    cost=usage_cost([{'error':'TimeoutError'}],{'provider':'llama.cpp'})
    assert cost['estimated_api_usd']==0 and cost['calls_with_unknown_usage']==1
    assert 'hardware/electricity excluded' in cost['scope']
