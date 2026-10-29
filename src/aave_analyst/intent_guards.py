"""Conservative literal anchors from the original question, independent of model plans."""
import re
import unicodedata


def question_anchors(question):
    text=unicodedata.normalize('NFC',question or '').casefold()
    result={}
    if not re.search(r'không (?:hỏi|cần|phải)|not asking',text):
        metrics=[]
        if re.search(r'dư\s+nợ|\bborrowed_usd\b|\boutstanding debt\b',text):metrics.append('borrowed_usd')
        if re.search(r'tài\s+sản\s+cung\s+cấp|giá\s+trị\s+cung\s+cấp|\bsupplied_usd\b',text):metrics.append('supplied_usd')
        if len(metrics)==1:result['metric']=metrics[0]
    months=[]
    for match in re.finditer(r'tháng\s+(?:(\d{4})-(\d{1,2})|(\d{1,2})(?:/|\s+năm\s+)(\d{4}))\b',text):
        year,month=(int(match[1]),int(match[2])) if match[1] else (int(match[4]),int(match[3]))
        if 1<=month<=12 and 1<=year<9999:months.append((year,month))
    if len(months)==1 and len(re.findall(r'\btháng\b',text))==1 and not re.search(r'\d{4}-\d{2}-\d{2}|\btrừ\b|\bđến\b|\btới\b|so sánh|chênh lệch|thay đổi',text):
        year,month=months[0]
        result.update(start=f'{year:04d}-{month:02d}-01',end=f'{year+1 if month==12 else year:04d}-{1 if month==12 else month+1:02d}-01')
    return result
