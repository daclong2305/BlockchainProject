"""Published-rate API estimates, distinct from actual invoices and local costs."""
from decimal import Decimal


SOURCE='https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf'


def usage_cost(calls, config):
    model=config.get('model_id','')
    local=config.get('provider')=='llama.cpp'
    if local:
        input_rate=output_rate=Decimal(0)
    elif model=='us.anthropic.claude-haiku-4-5-20251001-v1:0' and config.get('region')=='us-east-1':
        input_rate,output_rate=Decimal('1.10'),Decimal('5.50')
    else:
        return {'estimated_api_usd':None,'reason':'No verified rate for this model/profile/region'}
    if any(call.get('cache_read_input_tokens',0) or call.get('cache_write_input_tokens',0) for call in calls):
        return {'estimated_api_usd':None,'reason':'Cached tokens require separate rate accounting'}
    inputs=sum(call.get('input_tokens',0) for call in calls)
    outputs=sum(call.get('output_tokens',0) for call in calls)
    unknown=sum(bool(call.get('error')) and not(call.get('input_tokens') or call.get('output_tokens')) for call in calls)
    return {'estimated_api_usd':float((inputs*input_rate+outputs*output_rate)/Decimal(1000000)),
            'input_tokens':inputs,'output_tokens':outputs,'calls':len(calls),'calls_with_unknown_usage':unknown,
            'input_usd_per_million':str(input_rate),'output_usd_per_million':str(output_rate),
            'source':None if local else SOURCE,'source_page':None if local else 6,'verified_on':'2026-10-29',
            'scope':'API fee only; local hardware/electricity excluded. Published standard geo cross-region rate, not account invoice/discount/tax. Missing usage may underestimate API cost.'}


def experiment_costs(results, judge_calls, config):
    physical=[];seen={};consistent=True
    for result in results:
        shared=result.get('shared_draft_id')
        initial=result.get('draft',{}).get('usage',[])
        calls=result.get('usage',[])
        if not shared or calls[:len(initial)]!=initial:
            consistent=False;continue
        if shared not in seen:
            physical.extend(initial);seen[shared]=initial
        elif seen[shared]!=initial:consistent=False
        physical.extend(calls[len(initial):])
    return {'runtime_physical':usage_cost(physical,config['llm']) if consistent else {'estimated_api_usd':None,'reason':'Shared-draft usage binding incomplete'},
            'per_configuration':{mode:usage_cost([call for result in results if result['mode']==mode for call in result.get('usage',[])],config['llm']) for mode in sorted({r['mode'] for r in results})},
            'judge':usage_cost(judge_calls,config.get('judge_config',{})),
            'note':'Per-configuration estimates include the shared draft for standalone comparison; summing them double-counts initial calls. Runtime physical counts the shared draft once.'}
