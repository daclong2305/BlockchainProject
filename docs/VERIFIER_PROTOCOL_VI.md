# Protocol kiểm chứng dev phiên bản 2

## Vai trò
Generator tạo Draft chứa câu hỏi, kế hoạch, câu trả lời, claims, SQL, kết quả và nguồn. Candidate được lưu bất biến; verifier nhận bản sao. Evaluator có tham chiếu riêng, không truyền nhãn chuẩn vào sửa.

## Thí nghiệm
Một lần trên 20 câu dev, sáu cấu hình B0/B1/P/P-SQL/P-Evidence/P-Repair. Chung bản nháp theo câu. Deadline đầu cuối 120 giây, bao gồm pacing trong câu và bước sinh ban đầu. Tối đa hai vòng sửa. Giữ mọi timeout/API error. Đây không phải test cuối.
Replay riêng: tối đa 120 giây/candidate/verifier, không sửa. Rules, generic, full, no_sql, no_evidence; cùng nguồn/candidate. Không gộp độ trễ replay với độ trễ chatbot.
Stress SQL dùng 10 ca dev đúng/sai. Các yêu cầu được chỉ định theo câu hỏi, thay vì lấy kế hoạch LLM làm chuẩn. Stress dẫn chứng có 10 cặp đúng/sai ở năm loại; nhãn thiết kế vẫn chờ người xác minh.

## Đánh giá
Các thước đo phát hiện dùng nhãn evaluator tạm thời, không dùng checker pass. Báo TP/FP/FN/TN trên verdict pass/fail hoàn tất, precision/recall/F1, FPR, coverage, insufficient/timeout/error. Báo thêm recall trên toàn bộ ca lỗi đã lập lịch. Target hit SQL là đối chiếu mã lỗi với taxonomy; cần audit ngữ nghĩa để xác nhận định vị đúng, chưa phải chứng minh lỗi được giải thích đúng.
Giá trị số, cấu trúc numeric claim và độ đúng toàn bộ là các kết quả khác nhau. Count phải bằng tuyệt đối; benchmark USD sai số tương đối <=0,5%; kiểm tra ô kết quả runtime ROUND_HALF_UP hai chữ số. Tham chiếu bằng 0 đòi kết quả bằng 0.
Sai→đúng/đúng→sai chỉ tính cặp có nhãn đánh giá xác định. Thiếu judge là unknown, runtime error là thất bại vận hành. Không công bố điểm tổng hoàn chỉnh khi còn nhãn unknown.

## Khả năng tái lập
Lưu code hashes, model ID, benchmark hash, candidates, results, scoring journal, replay inputs, verdicts và API ledger. Chi phí ước tính standard US geo cross-region theo bảng giá Anthropic; không cộng trùng shared draft. Usage không trả về được giữ dưới dạng unknown và dự phòng bảo thủ, không khai phí bằng 0.
Không thêm prompt rule theo test. Khóa protocol trước test; hai người duyệt độc lập là điều kiện bắt buộc cho kết quả test chính thức.
