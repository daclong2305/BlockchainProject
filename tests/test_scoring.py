from aave_analyst.experiments import score_results, summarize, human_audit_sample


def numeric_case():
    gold = {'id':'q','category':'lookup','question':'USDC in August?', 'sources':[],
            'reference_answer':'100 USD', 'expected_numeric':[{'value':100,'unit':'USD'}]}
    result = {'question_id':'q','mode':'P','repeat':0,'elapsed':1,'usage':[],
              'draft':{'answer':'100 USD for DAI','claims':[{'numeric':{'value':100,'unit':'USD'}}]}}
    return gold, result


class Judge:
    def __init__(self, scope):self.scope=scope
    def complete(self, role, payload, timeout):
        assert payload['numeric_reference']
        return {'answer_correctness':1,'faithfulness':1,'citation_quality':1,
                'numeric_scope_correct':self.scope,'numeric_error_types':['asset'] if self.scope == 0 else [],'claim_checks':[]}


def test_equal_value_wrong_asset_fails_numeric_and_overall():
    gold, result = numeric_case()
    score = score_results([gold],[result],Judge(0))[0]
    assert score['numeric_value_correct'] is True
    assert score['numeric_correct'] is False and score['correct'] is False
    assert score['review_context']['system_answer'] == result['draft']['answer']


def test_missing_judge_scope_stays_unscored_not_success():
    gold, result = numeric_case()
    score = score_results([gold],[result],Judge(None))[0]
    assert score['numeric_correct'] is None and score['judge_error']
    summary = summarize([score])['configurations']['P']
    assert summary['correct_rate'] is None
    assert summary['correct_rate_bounds'] == [0,1]


def test_runtime_error_is_kept_as_failure_in_denominator():
    gold, result = numeric_case()
    result['error'] = 'TimeoutError'
    score = score_results([gold],[result],Judge(1))[0]
    summary = summarize([score])['configurations']['P']
    assert summary['outputs'] == 1 and summary['correct_rate'] == 0
    assert score['numeric_correct'] is False


def test_report_does_not_invent_complete_evaluation():
    from aave_analyst.protocol import coverage_report
    from aave_analyst.reporting import experiment_markdown
    gold,result=numeric_case()
    score=score_results([gold],[result])[0]
    report=experiment_markdown(summarize([score]),coverage_report([], [result]),{'final':False})
    assert 'E1' in report and 'E2' in report and 'E3' in report and 'E4' in report
    assert 'Độ phủ final đạt: False' in report
    assert 'chưa có' in report
    assert 'chưa xác minh' in report
