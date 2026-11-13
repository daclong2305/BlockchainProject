"""Summarize a completed rerun without invoking models or changing raw logs."""
import argparse,csv,json
from pathlib import Path

def main():
    p=argparse.ArgumentParser();p.add_argument('run',type=Path);args=p.parse_args();out=args.run
    scores=json.loads((out/'scores.json').read_text(encoding='utf-8'))
    summary=json.loads((out/'summary.json').read_text(encoding='utf-8'))
    config=json.loads((out/'config.json').read_text(encoding='utf-8'))
    calls=[]
    for name in ('api_calls.jsonl','evaluation_api_calls.jsonl','controlled_repairs/api_calls.jsonl'):
        path=out/name
        if path.exists():calls.extend(json.loads(s) for s in path.read_text(encoding='utf-8').splitlines() if s.strip())
    cost={'known_usage_estimate_usd':sum((c.get('input_tokens',0)*1.1+c.get('output_tokens',0)*5.5)/1e6 for c in calls),'unknown_usage_calls':sum(bool(c.get('usage_unknown')) for c in calls),'calls':len(calls),'note':'Token estimate, not invoice; excludes connection doctor.'}
    (out/'cost_summary.json').write_text(json.dumps(cost,indent=2),encoding='utf-8')
    lines=['# Kết quả chạy lại dev','', 'Nhãn máy tạm thời; chưa được người xác minh. Đây là kết quả dev, không phải test độc lập.','',
           f"API pace {config['pace_seconds']} giây; cooldown {config.get('cooldown_seconds',0)} giây ngoài deadline; xoay thứ tự: {config.get('rotate_modes',False)}. Deadline {config['deadline_seconds']} giây gồm pacing trong câu.",'',
           '| Mode | Đúng/tổng | Hoàn thành runtime | Đúng/hoàn thành | Lỗi runtime | Judge lỗi | Median s | p95 s |','|---|---:|---:|---:|---:|---:|---:|---:|']
    for mode,v in summary['configurations'].items():
        complete=[s for s in scores if s['mode']==mode and not s['runtime_error']]
        correct=sum(s['correct'] is True for s in complete)
        lines.append(f"| {mode} | {v['correct']}/{v['outputs']} | {len(complete)} | {correct}/{len(complete)} | {v['runtime_errors']} | {v['judge_errors']} | {v['median_seconds']:.2f} | {v['p95_seconds']:.2f} |")
    lines+=['','Điểm trên đầu ra hoàn thành là chỉ số có điều kiện, không thay điểm toàn bộ lượt chạy.','','## P so với baseline','',json.dumps(summary['paired_P_vs'],ensure_ascii=False,indent=2),'','## Chi phí','',json.dumps(cost,ensure_ascii=False,indent=2)]
    detection=out/'detection_summary.json'
    if detection.exists():
        lines+=['','## Hiệu quả phát hiện','', 'Nhãn tạm thời. Precision/recall trên verdict có kết luận phải đọc cùng coverage và insufficient.']
        for group,variants in json.loads(detection.read_text(encoding='utf-8')).items():
            lines+=['',f'### {group}','','| Verifier | TP | FP | FN | TN | Recall toàn bộ lỗi | Insufficient | Timeout | Lỗi |','|---|---:|---:|---:|---:|---:|---:|---:|---:|']
            for variant,m in variants.items():
                lines.append(f"| {variant} | {m['tp']} | {m['fp']} | {m['fn']} | {m['tn']} | {m.get('recall_all_scheduled_errors')} | {m['insufficient']} | {m['timeouts']} | {m['errors']} |")
    controlled=out/'controlled_repairs/results.jsonl'
    if controlled.exists():
        lines+=['','## Sửa lỗi có kiểm soát','','| Ca | Mode | Số vòng sửa | Đúng cuối tạm thời | Runtime lỗi |','|---|---|---:|---|---|']
        for line in controlled.read_text(encoding='utf-8').splitlines():
            row=json.loads(line)
            lines.append(f"| {row['case_id']} | {row['mode']} | {row['repairs']} | {row['score']['correct']} | {bool(row.get('error'))} |")
    (out/'RERUN_REPORT_VI.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
    fields=['question_id','mode','correct','runtime_error','judge_error','elapsed']
    with (out/'per_question.csv').open('w',encoding='utf-8-sig',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(scores)
    print('\n'.join(lines))

if __name__=='__main__':main()
