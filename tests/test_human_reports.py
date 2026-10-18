import pytest


def test_kappa_reports_undefined_for_constant_labels():
    from aave_analyst.reporting import cohen_kappa
    assert cohen_kappa([1,1],[1,1]) is None
    assert cohen_kappa([0,1,0,1],[0,1,0,1])==1
    assert cohen_kappa([0,1],[1,0])==-1


def test_human_report_requires_two_real_reviewers():
    from aave_analyst.reporting import human_report
    with pytest.raises(ValueError):human_report([{'reviewer_1':{'name':'A'},'reviewer_2':{'name':'A'}}])


def test_manifest_validation_includes_prompt_code(tmp_path):
    from aave_analyst.cli import code_hashes
    hashes=code_hashes()
    assert 'llm.py' in hashes
    assert 'pipeline.py' in hashes


def test_stress_families_do_not_leak_question_templates(tmp_path):
    from aave_analyst.stress import create_stress
    from test_pipeline import fixture_db
    rows=create_stress(fixture_db(tmp_path))
    dev={r['question'].replace('USDC','ASSET').replace('WETH','ASSET') for r in rows if r['split']=='dev'}
    test={r['question'].replace('USDT','ASSET').replace('DAI','ASSET') for r in rows if r['split']=='test'}
    assert not dev.intersection(test)
