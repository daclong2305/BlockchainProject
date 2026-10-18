def test_numeric_matching_is_rounding_not_half_percent():
    from aave_analyst.evaluation import numeric_equal
    assert numeric_equal(100.004,100,"USD")
    assert not numeric_equal(100.40,100,"USD")
    assert not numeric_equal(101,100,"count")
    assert numeric_equal(0,0,"USD")
    assert not numeric_equal(None,0,"USD")


def test_family_leakage_and_unapproved_gold_block_final_run():
    import pytest
    from aave_analyst.benchmark import validate_benchmark
    with pytest.raises(ValueError, match="family"):
        validate_benchmark([{"id":"1","family":"a","split":"dev"},{"id":"2","family":"a","split":"test"}], final=False)
    with pytest.raises(ValueError, match="review"):
        validate_benchmark([{"id":"1","family":"a","split":"test","review":{"reviewer_1":"","reviewer_2":""}}], final=True)


def test_citation_metrics_empty_is_not_perfect():
    from aave_analyst.evaluation import citation_metrics
    scores = citation_metrics([])
    assert scores["precision"] is None
    assert scores["completeness"] is None
    scores = citation_metrics([{"needs_evidence":True,"citations":[{"supported":True},{"supported":False}]}, {"needs_evidence":True,"citations":[]}])
    assert scores == {"precision":.5,"completeness":.5}


def test_ablation_flags_are_distinct():
    from aave_analyst.pipeline import MODES
    assert not MODES["B0"].repair
    assert MODES["B1"].generic_review
    assert MODES["P"].sql_check and MODES["P"].evidence_check
    assert not MODES["P-SQL"].sql_check
    assert not MODES["P-Evidence"].evidence_check
    assert not MODES["P-Repair"].repair
