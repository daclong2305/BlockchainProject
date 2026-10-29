import json
import pytest
from aave_analyst.audit_review import export_audit,import_audit
from aave_analyst.experiments import human_audit_sample


def sample(tmp_path):
    source=tmp_path/'audit.json'
    rows=[{'question_id':'q','mode':'P','repeat':0,'judge':{'answer_correctness':1},'correct':True,
           'review_context':{'question':'Question?', 'reference_answer':'Reference','system_answer':'Candidate','sources':[]}}]
    source.write_text(json.dumps(rows),encoding='utf-8')
    destination=tmp_path/'packets';export_audit(source,destination)
    return source,destination


def test_blinded_packets_hide_machine_labels_and_peer_decisions(tmp_path):
    source,directory=sample(tmp_path)
    packet=json.loads((directory/'reviewer-1.json').read_text())
    assert packet['reviewer_name']=='' and packet['items'][0]['answer_correctness'] is None
    text=(directory/'reviewer-1.md').read_text()
    assert 'Candidate' in text and 'Reference' in text
    assert '"judge"' not in text and '"mode"' not in text and '"correct"' not in text
    with pytest.raises(FileExistsError):export_audit(source,directory)


def test_import_requires_two_explicit_human_labels_and_preserves_machine_scores(tmp_path):
    source,directory=sample(tmp_path);paths=[directory/f'reviewer-{i}.json' for i in (1,2)]
    for i,path in enumerate(paths):
        packet=json.loads(path.read_text());packet['reviewer_name']=f'Fixture human {i}'
        packet['items'][0].update(answer_correctness=0,faithfulness=1,citation_quality=0)
        path.write_text(json.dumps(packet))
    rows=import_audit(source,*paths)
    assert rows[0]['reviewer_1']['answer_correctness']==0
    assert rows[0]['judge']['answer_correctness']==1
    source.write_text(source.read_text()+' ')
    with pytest.raises(ValueError,match='changed'):import_audit(source,*paths)


def test_stratified_sample_is_exact_twenty_percent_and_order_stable():
    rows=[{'question_id':f'q{i:02}','mode':mode,'category':cat,'repeat':rep,'judge':{'answer_correctness':1}}
          for mode in ('B0','B1','P','P-SQL','P-Evidence','P-Repair')
          for cat,size in [('mechanism',8),('lookup',8),('analysis',12),('mixed',8),('unanswerable',4)]
          for i in range(size) for rep in range(3)]
    a=human_audit_sample(rows);b=human_audit_sample(list(reversed(rows)))
    assert len(rows)==720 and len(a)==144
    assert a==b
    assert all(row['reviewer_1']['answer_correctness'] is None for row in a)
