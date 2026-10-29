"""Durable, input-bound checkpoints for long independent evaluation runs."""
import hashlib
import json
import os
from pathlib import Path

from .experiments import score_results


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def checkpointed_scores(records, results, llm, journal, provenance, resume=False):
    journal=Path(journal)
    header={'type':'manifest','schema_version':1,
            'fingerprint':digest({'records':records,'results':results,'provenance':provenance})}
    previous=[]
    if resume:
        if not journal.exists():raise ValueError('No scoring journal to resume')
        try:
            entries=[json.loads(line) for line in journal.read_text(encoding='utf-8').splitlines()]
        except (ValueError,UnicodeError) as exc:
            raise ValueError('Malformed journal; preserve original before manual recovery') from exc
        if not entries or entries[0]!=header:raise ValueError('Scoring inputs/judge/code changed; cannot resume')
        previous=entries[1:]
        if len(previous)>len(results):raise ValueError('Journal has extra scores')
        for index,event in enumerate(previous):
            key=lambda row:(row.get('question_id'),row.get('repeat'),row.get('mode'))
            if event.get('type')!='score' or event.get('index')!=index or event.get('result_sha256')!=digest(results[index]) or key(event.get('score',{}))!=key(results[index]):
                raise ValueError('Journal ordering or result binding invalid')
    elif journal.exists():
        raise FileExistsError('Scoring journal exists; explicitly resume with the same inputs')
    scores=[event['score'] for event in previous]
    usage=[call for event in previous for call in event['judge_usage']]
    journal.parent.mkdir(parents=True,exist_ok=True)
    with journal.open('a' if resume else 'x',encoding='utf-8') as stream:
        def append(event):
            stream.write(json.dumps(event,ensure_ascii=False)+'\n')
            stream.flush()
            os.fsync(stream.fileno())
        if not resume:append(header)
        for index in range(len(previous),len(results)):
            start=len(llm.calls) if llm else 0
            score=score_results(records,[results[index]],llm)[0]
            calls=llm.calls[start:] if llm else []
            append({'type':'score','index':index,'result_sha256':digest(results[index]),'score':score,'judge_usage':calls})
            scores.append(score);usage.extend(calls)
    return scores,usage
