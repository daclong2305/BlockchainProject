"""Small, separately reported repair experiment on DEV-only controlled errors."""
import argparse,sys,json
from pathlib import Path
from dataclasses import asdict
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from aave_analyst.cli import analyst_at,write_json,code_hashes
from aave_analyst.research_runtime import MeteredLLM
from aave_analyst.experiments import score_results
from run_verifier_dev import restore
root=Path(__file__).resolve().parents[1]
def read(p):return [json.loads(s) for s in p.read_text(encoding='utf-8').splitlines()]
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--out',type=Path,required=True,help='Completed dev replay directory')
    folder=parser.parse_args().out
    if not (folder/'completed.json').exists():
        parser.error('Finish dev scoring and replay before controlled repairs')
    inputs={r['id']:r for r in read(folder/'replay_candidates.jsonl')}
    chosen=['S001-wrong','S001-correct','S002-wrong','S002-correct']
    out=folder/'controlled_repairs';out.mkdir(exist_ok=True)
    config={'case_ids':chosen,'modes':['B1','P'],'pace':12,'deadline':120,'code_hashes':code_hashes(),'label_status':'provisional DEV controlled experiment'}
    path=out/'config.json'
    if path.exists() and json.loads(path.read_text())!=config:raise ValueError('Controlled protocol changed')
    if not path.exists():write_json(path,config)
    a=analyst_at(root,provider='bedrock');a.llm=MeteredLLM(a.llm,out/'api_calls.jsonl',pace=12.,cap=1.)
    target=out/'results.jsonl';previous=read(target) if target.exists() else [];done={(r['case_id'],r['mode']) for r in previous}
    for cid in chosen:
        for mode in ['B1','P']:
            if (cid,mode) in done:continue
            d=restore(inputs[cid]['draft']);d.elapsed=0
            result=dict(asdict(a.continue_draft(d,mode)),case_id=cid,question_id=cid,repeat=0)
            # Evaluation receives gold only after the runtime result has been finalized.
            good=inputs[cid.replace('-wrong','-correct')]['draft'];value=good['query_result']['rows'][0]['value']
            record={'id':cid,'category':'analysis','question':good['question'],'reference_answer':{'sql_result':good['query_result']['rows']},
                    'sources':[{'id':'SQL1','sql':good['sql'],'rows':good['query_result']['rows']}],
                    'expected_numeric':[{'value':value,'unit':'USD'}],'numeric_relative_tolerance':'0.005','scope':{}}
            score=score_results([record],[result],a.llm)[0]
            row=dict(result,score=score)
            with target.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False,default=str)+'\n')
            print(cid,mode,result['status'],'correct',score['correct'],flush=True)
    write_json(out/'completed.json',{'outputs':len(read(target)),'note':'Separate from 120 natural dev outputs; controlled labels need human validation.'})
if __name__=='__main__':main()
