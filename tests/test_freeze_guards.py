import pytest
from aave_analyst.benchmark import validate_benchmark,freeze_benchmark


@pytest.mark.parametrize('review',[
    {'reviewer_1':'Person A','reviewer_2':' person  a ','approved':True},
    {'reviewer_1':'A','reviewer_2':'B','approved':'true'},
    {'reviewer_1':'A','reviewer_2':'B','approved':1},
])
def test_final_gate_requires_distinct_names_and_actual_boolean(review):
    with pytest.raises(ValueError,match='review'):
        validate_benchmark([{'id':'q','family':'f','split':'test','review':review}],final=True)


def test_freeze_never_replaces_existing_lock(tmp_path):
    source=tmp_path/'questions.jsonl';lock=source.with_suffix('.lock.json')
    lock.write_text('original immutable lock')
    with pytest.raises(FileExistsError):freeze_benchmark(source)
    assert lock.read_text()=='original immutable lock'
