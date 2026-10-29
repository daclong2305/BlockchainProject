from collections import Counter
import unicodedata


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
        names=[unicodedata.normalize('NFC',' '.join(str(r.get('name','')).casefold().split())) for r in (a,b)]
        if not all(names) or names[0]==names[1]:raise ValueError('Two distinct human reviewers required')
        for key in ['answer_correctness','faithfulness','citation_quality']:
            if a.get(key) not in (0,1) or b.get(key) not in (0,1):raise ValueError(f'Missing binary human score: {key}')
    for key in ['answer_correctness','faithfulness','citation_quality']:
        a=[r['reviewer_1'][key] for r in rows];b=[r['reviewer_2'][key] for r in rows]
        judge=[r['judge'][key] for r in rows]
        consensus=[i for i,(x,y) in enumerate(zip(a,b)) if x==y]
        result[key]={'n':len(a),'human_agreement':sum(x==y for x,y in zip(a,b))/len(a) if a else None,'human_kappa':cohen_kappa(a,b),'judge_vs_reviewer1_kappa':cohen_kappa(a,judge),'judge_vs_reviewer2_kappa':cohen_kappa(b,judge),'judge_agreement_on_human_consensus':sum(judge[i]==a[i] for i in consensus)/len(consensus) if consensus else None,'consensus_cases':len(consensus)}
    return result


def experiment_markdown(summary, coverage, config):
    """Describe measured outputs without inventing missing evaluation or costs."""
    def display(value):
        if value is None:return 'chưa có'
        if isinstance(value,float):return f'{value:.4f}'
        return str(value)
    lines=['# Báo cáo E1–E4', '',
           f"Final được khai báo: {config.get('final',False)}. Độ phủ final đạt: {coverage['complete']}.",
           f"Đầu ra: {coverage['actual_outputs']}/{coverage['expected_outputs']} theo protocol final. Lỗi runtime: {coverage['runtime_errors']}.",
           'Độ phủ không chứng minh chất lượng hoặc phê duyệt của người. Báo cáo thiếu judge không được dùng kết luận hiệu quả.', '',
           '| Cấu hình | Đầu ra | Đã chấm | Đúng toàn bộ | Độ đúng | Số liệu đúng/đã chấm | Median giây | p95 giây | Lỗi runtime |',
           '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for mode, row in sorted(summary['configurations'].items()):
        lines.append('| '+' | '.join(display(x) for x in [mode,row['outputs'],row['scored_outputs'],row['correct'],row['correct_rate'],f"{row['numeric_correct']}/{row['numeric_total']}",row['median_seconds'],row['p95_seconds'],row['runtime_errors']])+' |')
    lines += ['', '## E1 — Hiệu quả tổng thể', '',
              'So sánh B0, B1, P bằng độ đúng toàn bộ, dẫn chứng và từ chối. Điểm chưa chấm là chưa biết; timeout/lỗi là sai, không loại khỏi mẫu số.', '',
              '## E2 — Ý nghĩa SQL', '',
              'So sánh P với P-SQL. numeric_value_correct kiểm tra giá trị/đơn vị; numeric_correct còn yêu cầu judge kiểm tra đại lượng, tổng hợp, tài sản và thời gian. Stress SQL được báo cáo riêng.', '',
              '## E3 — Dẫn chứng', '',
              '| Cấu hình | Citation precision | Citation completeness | Phát biểu thiếu căn cứ | Từ chối sai |',
              '|---|---:|---:|---:|---:|']
    for mode in ['P','P-Evidence']:
        if mode in summary['configurations']:
            row=summary['configurations'][mode]
            lines.append('| '+' | '.join(display(x) for x in [mode,row['citation_precision'],row['citation_completeness'],row['unsupported_answers'],row['wrong_refusals']])+' |')
    lines += ['', '## E4 — Vòng sửa', '', '| P so với | Sai → đúng | Đúng → sai | Cặp đã chấm |', '|---|---:|---:|---:|']
    for mode,row in summary['paired_P_vs'].items():
        lines.append(f"| {mode} | {row['wrong_to_right']} | {row['right_to_wrong']} | {row['paired_scored']} |")
    lines += ['', '## Chi phí và giới hạn', '',
              'Token và độ trễ thực có trong summary.json; token judge trong judge_usage.json. costs.json lưu ước tính phí API theo đơn giá đã kiểm tra cho đúng model/profile/region; cấu hình chưa có đơn giá giữ null. Chi phí điện/phần cứng chưa xác minh; phí API local bằng 0 không đồng nghĩa tổng chi phí bằng 0.',
              'Bản nháp dùng chung được tính vào token mỗi cấu hình để so sánh khi triển khai riêng; không cộng sáu cấu hình để suy ra hóa đơn thực vì sẽ đếm trùng bản nháp.',
              'Chưa kết luận H1–H3 nếu thiếu chấm độc lập, audit người 20%, Cohen kappa, stress SQL hoặc đo truy vết. Benchmark nhỏ và ba lần lặp không phải ba câu hỏi độc lập.', '']
    return '\n'.join(lines)
