import json
import pytest
from aave_analyst.benchmark import save_benchmark
from aave_analyst.review import export_reviews, import_reviews


def packets(tmp_path):
    source = tmp_path / 'questions.jsonl'
    save_benchmark([{'id': 'q1', 'split': 'dev', 'family': 'f1', 'question': 'Question?', 'reference_answer': 'Draft'}], source)
    directory = tmp_path / 'reviews'
    export_reviews(source, directory)
    paths = [directory / f'reviewer-{i}.json' for i in (1, 2)]
    for i, path in enumerate(paths):
        packet = json.loads(path.read_text(encoding='utf-8'))
        packet['reviewer_name'] = f'Test fixture reviewer {i}'
        for item in packet['items']:
            item.update(verdict='approved', verified_answer=True, verified_sources=True, verified_scope=True)
        path.write_text(json.dumps(packet), encoding='utf-8')
    return source, paths


def test_explicit_two_reviewers_required(tmp_path):
    source, paths = packets(tmp_path)
    packet = json.loads(paths[1].read_text())
    packet['reviewer_name'] = '  TEST fixture reviewer 0 '
    paths[1].write_text(json.dumps(packet))
    with pytest.raises(ValueError, match='distinct'):
        import_reviews(source, *paths)


def test_review_content_cannot_change(tmp_path):
    source, paths = packets(tmp_path)
    source.write_text(source.read_text().replace('Draft', 'Changed'))
    with pytest.raises(ValueError, match='changed'):
        import_reviews(source, *paths)


def test_blank_scope_is_not_approval(tmp_path):
    source, paths = packets(tmp_path)
    packet = json.loads(paths[1].read_text())
    packet['items'][0]['verified_scope'] = None
    paths[1].write_text(json.dumps(packet))
    assert import_reviews(source, *paths)['approved'] == 0


def test_complete_fixture_review_and_frozen_guard(tmp_path):
    source, paths = packets(tmp_path)
    assert import_reviews(source, *paths)['approved'] == 1
    source.with_suffix('.lock.json').write_text('{}')
    with pytest.raises(ValueError, match='Frozen'):
        import_reviews(source, *paths)
