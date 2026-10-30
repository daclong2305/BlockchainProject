### 5.4 Pilot so sánh baseline và phương pháp đề xuất

Nhóm chạy 20 câu dev, một lần lặp cho B0, B1 và P, tạo 60 đầu ra với Qwen ViText2SQL 3B Q4_K_M local. Mỗi câu dùng chung bản nháp ban đầu cho ba cấu hình; ngân sách 120 giây bao gồm cả sinh bản nháp, kiểm chứng và sửa. Không thay cấu hình giữa lượt; hash mã và dữ liệu đầu/cuối khớp. Thứ tự B0, B1, P cố định và cache server không được reset giữa các bước, nên chưa tách ảnh hưởng cache khỏi độ trễ. Judge là Claude Haiku 4.5 qua Bedrock, chạy tách khỏi verifier Qwen. Đáp án tham chiếu vẫn chưa được hai người duyệt; mọi điểm dưới đây là kết quả pilot theo tham chiếu tạm thời, không phải kết quả test cuối.

| Chỉ số trên 20 câu mỗi cấu hình | B0 | B1 | P |
|---|---:|---:|---:|
| Đầu ra lưu được | 20 | 20 | 20 |
| Có nhãn judge hợp lệ | 15/20 (75,0%) | 13/20 (65,0%) | 1/20 (5,0%) |
| Answer correctness bằng 1 | 13/20 (65,0%) | 11/20 (55,0%) | 0/20 (0,0%) |
| Faithfulness bằng 1 | 13/20 (65,0%) | 11/20 (55,0%) | 0/20 (0,0%) |
| Citation quality bằng 1 | 13/20 (65,0%) | 11/20 (55,0%) | 0/20 (0,0%) |
| Đạt toàn bộ tiêu chí và số liệu | 1/20 (5,0%) | 1/20 (5,0%) | 0/20 (0,0%) |
| Chưa xác định đúng toàn bộ | 1 | 0 | 0 |
| Số liệu đạt theo judge độc lập | 12/14 (85,7%) | 10/14 (71,4%) | 0/14 (0,0%) |
| Khai báo số và phạm vi đạt theo scorer | 0/14 (0,0%) | 0/14 (0,0%) | 0/14 (0,0%) |
| Số liệu còn thiếu phán quyết phạm vi | 0 | 0 | 0 |
| Câu định lượng chưa có nhãn judge | 0 | 3 | 14 |
| Lỗi runtime kể cả timeout | 4 | 4 | 19 |
| Timeout | 3 | 3 | 18 |
| Lỗi judge | 1 | 3 | 0 |
| Từ chối đúng được judge xác nhận | 0/2 (0,0%) | 0/2 (0,0%) | 0/2 (0,0%) |
| Từ chối sai trên câu có thể trả lời | 1 | 1 | 2 |
| Median giây | 40,02 | 56,49 | 120,01 |
| p95 giây | 120,01 | 120,01 | 120,03 |
| Token vào / ra đã ghi | 84273 / 4759 | 111148 / 4871 | 171147 / 7046 |

Đạt toàn bộ yêu cầu đồng thời answer_correctness, faithfulness và citation_quality bằng 1, không sai kiểm tra số liệu/phạm vi. Tỷ lệ đạt luôn dùng mẫu số 20, gồm lỗi runtime. Nếu có câu chưa chấm được, đây là tỷ lệ đạt đã xác nhận, không tự quy toàn bộ câu chưa biết thành sai hoặc công bố điểm hoàn chỉnh. Số liệu dùng mẫu số là số câu có đáp án định lượng, không chỉ phần model trả lời thành công. Scorer theo mã yêu cầu numeric claim có cấu trúc; thiếu khai báo này bị đánh không đạt dù văn bản có thể chứa số đúng. Vì vậy báo riêng phán quyết số liệu của judge để không đánh đồng thiếu cấu trúc bằng chứng với sai giá trị. Timeout được xác định từ lỗi đã ghi; token chưa trả về khi timeout có thể làm thiếu thống kê usage.

| Chỉ số dẫn chứng trên đầu ra có judge | B0 | B1 | P |
|---|---:|---:|---:|
| Citation precision trung bình | 0,87 (n=15) | 0,85 (n=13) | 0,00 (n=1) |
| Citation completeness trung bình | 0,87 (n=15) | 0,85 (n=13) | 0,00 (n=1) |
| Judge ghi nhận câu thiếu căn cứ | 2 | 2 | 1 |

Precision/completeness là trung bình theo đầu ra được chấm và có mẫu số phù hợp; không bao gồm câu runtime lỗi, judge lỗi hoặc không có phát biểu cần dẫn. Vì thế không được diễn giải điểm dẫn chứng cao của vài câu thành chất lượng toàn bộ bộ câu hỏi.

| Chuyển trạng thái khi dùng P | Sai thành đúng | Đúng thành sai | Cặp xác định |
|---|---:|---:|---:|
| P so với B0 | 0 | 1 | 19/20 |
| P so với B1 | 0 | 1 | 20/20 |

Các cặp chỉ gồm câu có trạng thái đúng/sai xác định ở cả hai cấu hình. Một lần chạy trên 20 câu dev không đủ để khẳng định ý nghĩa thống kê hoặc tính tổng quát. Không điều chỉnh tham số dựa vào test từ bảng này.

Pilot chưa hỗ trợ kết luận P tốt hơn B0/B1 trên cấu hình hiện tại. P có 18/20 timeout, median 120,01 giây, trong khi B0 và B1 có median 40,02 và 56,49 giây. Chênh lệch phản ánh ngân sách kiểm chứng trên máy local, không chứng minh kiểm chứng có cấu trúc vô ích khi thay phần cứng hoặc ngân sách. B0 có một câu chưa xác định nên tỷ lệ đạt toàn bộ đã xác nhận là 5%, khoảng khả dĩ 5–10%; B1 đạt 5% và P đạt 0% theo scorer hiện hành. Điểm toàn bộ thấp còn do scorer yêu cầu numeric claim có cấu trúc, trong khi judge vẫn đánh giá đúng số và phạm vi ở 12/14 câu B0 và 10/14 câu B1. Cần cải thiện hợp đồng đầu ra và kiểm tra độ tin cậy judge, không sửa cách chấm sau khi xem test để tạo kết quả thuận lợi.

Bốn lỗi judge đều là ThrottlingException của Bedrock: Q048/B1, Q049/B1, Q050/B1 và Q056/B0. Các lỗi được giữ trong journal, chưa gọi lại để thay nhãn. Trong đó một câu B0 còn chưa xác định toàn bộ, còn các câu B1 đã không đạt yêu cầu cấu trúc số liệu theo mã nhưng thiếu phán quyết judge cho các tiêu chí độc lập. Không coi ba lỗi judge B1 là ba lần chấm hợp lệ.

| Nhóm câu hỏi và số câu | B0 đạt | B1 đạt | P đạt |
|---|---:|---:|---:|
| Cơ chế (n=4) | 1/4 | 1/4 | 0/4 |
| Tra cứu (n=4) | 0/4 | 0/4 | 0/4 |
| Phân tích (n=6) | 0/6 | 0/6 | 0/6 |
| Hỗn hợp (n=4) | 0/4 | 0/4 | 0/4 |
| Không trả lời được (n=2) | 0/2 | 0/2 | 0/2 |

Phí API suy luận Qwen local là 0 USD; chưa đo điện và khấu hao phần cứng. Phí judge ước tính từ các token đã ghi của pilot là 0,119793 USD theo đơn giá trong costs.json, không phải hóa đơn tài khoản. Bốn lượt throttling không có thống kê usage; chưa đối chiếu chi phí đầy đủ với hóa đơn. Token bản nháp được tính vào từng cấu hình để mô phỏng triển khai riêng; không cộng ba tổng này thành chi phí vật lý vì bản nháp thực tế dùng chung.

Kết quả này bổ sung số đo giữa kỳ cho E1. Không dùng pilot ba cấu hình để tuyên bố đã kiểm định H1–H3: các đối chiếu P-SQL, P-Evidence và P-Repair vẫn cần thí nghiệm chính. Audit người và Cohen kappa chưa có nhãn, không được suy ra từ điểm judge.

Minh chứng pilot: runs/midterm-dev20-qwen-v1/; gồm config.json, benchmark_snapshot.jsonl, results.jsonl, integrity.json, scoring_journal.jsonl, scores.jsonl, summary.json, audit_sampling.json và costs.json.

