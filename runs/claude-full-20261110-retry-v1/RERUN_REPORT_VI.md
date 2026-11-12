# Kết quả chạy lại dev

Nhãn máy tạm thời; chưa được người xác minh. Đây là kết quả dev, không phải test độc lập.

API pace 6.0 giây; cooldown 0.0 giây ngoài deadline; xoay thứ tự: True. Deadline 120 giây gồm pacing trong câu.

| Mode | Đúng/tổng | Hoàn thành runtime | Đúng/hoàn thành | Lỗi runtime | Judge lỗi | Median s | p95 s |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 | 19/20 | 20 | 19/20 | 0 | 0 | 16.32 | 28.40 |
| B1 | 18/20 | 20 | 18/20 | 0 | 0 | 28.90 | 77.24 |
| P | 17/20 | 20 | 17/20 | 0 | 0 | 36.27 | 78.53 |
| P-Evidence | 19/20 | 20 | 19/20 | 0 | 0 | 32.78 | 75.67 |
| P-Repair | 16/20 | 20 | 16/20 | 0 | 0 | 31.72 | 40.66 |
| P-SQL | 14/20 | 20 | 14/20 | 0 | 0 | 33.07 | 64.34 |

Điểm trên đầu ra hoàn thành là chỉ số có điều kiện, không thay điểm toàn bộ lượt chạy.

## P so với baseline

{
  "B0": {
    "wrong_to_right": 0,
    "right_to_wrong": 2,
    "paired_scored": 20
  },
  "B1": {
    "wrong_to_right": 1,
    "right_to_wrong": 2,
    "paired_scored": 20
  },
  "P-SQL": {
    "wrong_to_right": 3,
    "right_to_wrong": 0,
    "paired_scored": 20
  },
  "P-Evidence": {
    "wrong_to_right": 0,
    "right_to_wrong": 2,
    "paired_scored": 20
  },
  "P-Repair": {
    "wrong_to_right": 2,
    "right_to_wrong": 1,
    "paired_scored": 20
  }
}

## Chi phí

{
  "known_usage_estimate_usd": 4.4708829,
  "unknown_usage_calls": 28,
  "calls": 874,
  "note": "Token estimate, not invoice; excludes connection doctor."
}

## Hiệu quả phát hiện

Nhãn tạm thời. Precision/recall trên verdict có kết luận phải đọc cùng coverage và insufficient.

### natural

| Verifier | TP | FP | FN | TN | Recall toàn bộ lỗi | Insufficient | Timeout | Lỗi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rules | 0 | 7 | 1 | 12 | 0.0 | 0 | 0 | 0 |
| generic | 1 | 2 | 0 | 10 | 1.0 | 7 | 0 | 0 |
| full | 1 | 6 | 0 | 4 | 1.0 | 9 | 0 | 0 |
| no_sql | 1 | 7 | 0 | 4 | 1.0 | 8 | 0 | 0 |
| no_evidence | 1 | 10 | 0 | 8 | 1.0 | 1 | 0 | 0 |

### sql_stress

| Verifier | TP | FP | FN | TN | Recall toàn bộ lỗi | Insufficient | Timeout | Lỗi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rules | 6 | 0 | 4 | 10 | 0.6 | 0 | 0 | 0 |
| generic | 10 | 0 | 0 | 1 | 1.0 | 9 | 0 | 0 |
| full | 7 | 1 | 0 | 4 | 0.7 | 8 | 0 | 0 |
| no_sql | 7 | 1 | 0 | 4 | 0.7 | 8 | 0 | 0 |
| no_evidence | 10 | 1 | 0 | 8 | 1.0 | 1 | 0 | 0 |

### evidence_stress

| Verifier | TP | FP | FN | TN | Recall toàn bộ lỗi | Insufficient | Timeout | Lỗi |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| rules | 2 | 0 | 8 | 10 | 0.2 | 0 | 0 | 0 |
| generic | 7 | 5 | 0 | 0 | 0.7 | 8 | 0 | 0 |
| full | 6 | 10 | 0 | 0 | 0.6 | 4 | 0 | 0 |
| no_sql | 6 | 10 | 0 | 0 | 0.6 | 4 | 0 | 0 |
| no_evidence | 0 | 0 | 10 | 10 | 0.0 | 0 | 0 | 0 |

## Sửa lỗi có kiểm soát

| Ca | Mode | Số vòng sửa | Đúng cuối tạm thời | Runtime lỗi |
|---|---|---:|---|---|
| S001-wrong | B1 | 1 | True | False |
| S001-wrong | P | 1 | True | False |
| S001-correct | B1 | 0 | True | False |
| S001-correct | P | 0 | True | False |
| S002-wrong | B1 | 2 | True | False |
| S002-wrong | P | 2 | True | False |
| S002-correct | B1 | 0 | True | False |
| S002-correct | P | 0 | True | False |
