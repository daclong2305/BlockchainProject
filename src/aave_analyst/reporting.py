from collections import Counter


def cohen_kappa(a,b):
    if len(a)!=len(b) or not a:return None
    n=len(a);agreement=sum(x==y for x,y in zip(a,b))/n
    ca,cb=Counter(a),Counter(b)
    expected=sum(ca[k]*cb[k] for k in set(ca)|set(cb))/(n*n)
    return (agreement-expected)/(1-expected) if expected!=1 else None


def human_report(rows):
    result={}
    for row in rows:
        a,b=row.get('reviewer_1',{}),row.get('reviewer_2',{})
        if not a.get('name') or not b.get('name') or a['name']==b['name']:raise ValueError('Two distinct human reviewers required')
        for key in ['answer_correctness','faithfulness','citation_quality']:
            if a.get(key) not in (0,1) or b.get(key) not in (0,1):raise ValueError(f'Missing binary human score: {key}')
    for key in ['answer_correctness','faithfulness','citation_quality']:
        a=[r['reviewer_1'][key] for r in rows];b=[r['reviewer_2'][key] for r in rows]
        judge=[r['judge'][key] for r in rows]
        consensus=[i for i,(x,y) in enumerate(zip(a,b)) if x==y]
        result[key]={'n':len(a),'human_agreement':sum(x==y for x,y in zip(a,b))/len(a) if a else None,'human_kappa':cohen_kappa(a,b),'judge_vs_reviewer1_kappa':cohen_kappa(a,judge),'judge_vs_reviewer2_kappa':cohen_kappa(b,judge),'judge_agreement_on_human_consensus':sum(judge[i]==a[i] for i in consensus)/len(consensus) if consensus else None,'consensus_cases':len(consensus)}
    return result
