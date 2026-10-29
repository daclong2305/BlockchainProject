"""Blinded independent human audit packets; judge labels stay outside the packets."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unicodedata

METRICS=('answer_correctness','faithfulness','citation_quality')


def audit_cases(rows):
    cases=[]
    for index,row in enumerate(rows):
        context=row.get('review_context')
        if not context:raise ValueError('Audit requires source/question/candidate context')
        cases.append({'case_id':f'A{index+1:04d}','context':context})
    return cases


def export_audit(source,destination):
    source,destination=Path(source),Path(destination)
    rows=json.loads(source.read_text(encoding='utf-8'))
    if not rows:raise ValueError('No judge-auditable cases in this sample')
    cases=audit_cases(rows)
    outputs=[destination/f'reviewer-{i}.{suffix}' for i in (1,2) for suffix in ('json','md')]
    if any(path.exists() for path in outputs):raise FileExistsError('Preserve existing audit packets')
    destination.mkdir(parents=True,exist_ok=True)
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    booklet=['# Independent audit', '',
             'Assess each answer against the supplied reference and sources. Do not inspect machine labels or the other reviewer’s decisions.',
             'Record 0 or 1 for correctness, faithfulness and citation quality; give reasons. Do not infer correctness from a runtime passed status. Gold must already have independent review for a final experiment.', '']
    for case in cases:
        booklet += [f"## {case['case_id']}",'','```json',json.dumps(case['context'],ensure_ascii=False,indent=2),'```','']
    for i in (1,2):
        packet={'schema_version':1,'source_sha256':sha,'reviewer_name':'',
                'items':[{'case_id':case['case_id'],**{metric:None for metric in METRICS},'notes':''} for case in cases]}
        (destination/f'reviewer-{i}.json').write_text(json.dumps(packet,ensure_ascii=False,indent=2),encoding='utf-8')
        (destination/f'reviewer-{i}.md').write_text('\n'.join(booklet),encoding='utf-8')
    return {'cases':len(cases),'source_sha256':sha,'outputs':[str(path) for path in outputs]}


def import_audit(source,first,second):
    source=Path(source)
    rows=json.loads(source.read_text(encoding='utf-8'))
    if not rows:raise ValueError('No audit sample')
    sha=hashlib.sha256(source.read_bytes()).hexdigest()
    packets=[json.loads(Path(path).read_text(encoding='utf-8-sig')) for path in (first,second)]
    names=[str(packet.get('reviewer_name','')).strip() for packet in packets]
    normalized=[unicodedata.normalize('NFC',' '.join(name.casefold().split())) for name in names]
    if not all(normalized) or normalized[0]==normalized[1]:raise ValueError('Two distinct named humans required')
    cases=audit_cases(rows);expected={case['case_id'] for case in cases};indexes=[]
    for packet in packets:
        if packet.get('source_sha256')!=sha:raise ValueError('Audit source changed since export')
        items=packet.get('items',[]);index={item['case_id']:item for item in items}
        if len(index)!=len(items) or set(index)!=expected:raise ValueError('Audit IDs must match sample exactly')
        for item in items:
            if any(type(item.get(metric)) is not int or item[metric] not in (0,1) for metric in METRICS):
                raise ValueError('Every audit criterion needs an explicit binary human score')
        indexes.append(index)
    completed=deepcopy(rows)
    for row,case in zip(completed,cases):
        for i in (0,1):
            item=indexes[i][case['case_id']]
            row[f'reviewer_{i+1}']={'name':names[i],**{metric:item[metric] for metric in METRICS},'notes':item.get('notes','')}
    return completed
