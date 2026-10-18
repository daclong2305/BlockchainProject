# Quy trình thực nghiệm

## Trước khi mở tập kiểm thử

1. Đọc audit.json và dictionary.json. Xác minh đơn vị, UTC, snapshot vs observation, dữ liệu thiếu và giá trị điền tiếp.
2. Hai người độc lập kiểm tra 60 câu, đáp án, SQL và nguồn. Các lời giải cơ chế trong bản tạo tự động chỉ là dàn ý; sửa các câu mà nguồn chưa hỗ trợ đầy đủ. Không dùng nguồn ngoài kho cố định để tự ý bù vào kết quả chatbot.
3. Kiểm tra chính xác phân bố 4/8, 4/8, 6/12, 4/8, 2/4 và family không rò rỉ.
4. Điều chỉnh trên dev; chọn cấu hình, ghi phiên bản code. Khóa dữ liệu/benchmark/model bằng freeze. Không phê duyệt tên giả hoặc sao chép phê duyệt tự động.
5. Pilot để ước lượng số gọi, token, độ trễ. Kiểm tra hạn mức tài khoản trước 720 đầu ra. API lỗi được ghi; không tự chạy lại chỉ các câu sai để thay thế kết quả.

## E1–E4

| Thí nghiệm | So sánh | Quan sát |
|---|---|---|
| E1 | B0, B1, P | Độ đúng toàn bộ, số liệu, dẫn chứng, từ chối và chi phí |
| E2 | P, P-SQL | Lỗi đại lượng, tổng hợp, bộ lọc, đơn vị và nối bảng |
| E3 | P, P-Evidence | Citation precision/completeness và phát biểu thiếu căn cứ |
| E4 | P, P-Repair | Sai→đúng, đúng→sai, số lượt sửa, độ trễ và token |

Mỗi câu/lần chỉ có một bản nháp. Không đưa đáp án chuẩn vào luồng runtime. Dùng cùng 720 kết quả cho E1–E4; không tạo bốn đợt chạy riêng. Đơn vị phân tích là câu hỏi; báo cáo điểm qua ba lần chạy và số câu đúng/tổng số, không coi 120 output của một cấu hình là 120 câu độc lập.

## Chấm

- Factual: so giá trị được trả lời, đơn vị và độ chính xác; không so văn bản SQL. USD dùng Decimal ROUND_HALF_UP, số đếm khớp tuyệt đối. Judge kiểm tra ý nghĩa và phạm vi của phát biểu, không dùng đơn thuần số bằng nhau làm đúng toàn bộ.
- Judge: nhận câu hỏi, nguồn chuẩn, đáp án tham chiếu và câu trả lời kèm bằng chứng. Ba tiêu chí 0/1: correctness, faithfulness, citation quality. Tên mode không đưa vào prompt judge.
- Câu mixed phải qua kiểm tra numeric và cả ba tiêu chí. Câu unanswerable phải đúng giới hạn thực tế, không đoán và không từ chối sai câu trả lời được.
- Citation precision = số cặp phát biểu–nguồn được nguồn hỗ trợ / số cặp đã dẫn. Completeness = số phát biểu cần dẫn có ít nhất một nguồn hỗ trợ / tổng phát biểu cần dẫn. Không có mẫu số: null/N/A. Từ chối không tự nhận điểm dẫn chứng.
- Judge lỗi: giữ nguyên kết quả runtime, ghi judge_error và để điểm chưa chấm; phải xử lý minh bạch trước báo cáo cuối, không bỏ các câu này khỏi mẫu mà không giải thích.

## Kiểm tra bởi người

Sau score --judge, human_audit.json lấy xấp xỉ 20% phân tầng theo mode và loại câu, seed 2026. Hai người chấm riêng từng tiêu chí, không đọc điểm người kia. Ghi tên và 0/1; so với judge, báo cáo Cohen kappa cùng tỷ lệ đồng thuận. Nếu tất cả nhãn giống nhau khiến kappa không xác định, ghi N/A, không mặc định là 1.

Sau khi hai người điền xong, chạy `python -m aave_analyst.cli human-report runs/TEN_RUN/human_audit.json` để xuất human_agreement.json. Không tự lấp các nhãn chưa được chấm.

Chọn trước 10 ID test để đo truy vết nguồn; dùng cùng ID cho các cấu hình. Ghi người kiểm tra, có tìm đúng SQL/bản ghi/đoạn nguồn không và số giây. Không chọn riêng câu hệ thống làm tốt.

## Stress SQL

stress.jsonl tách riêng, không cộng vào 60 câu. Kiểm tra hai bản truy vấn đúng/sai của các lỗi metric/aggregation/filter/unit/join. Hai người xác minh trước khi chạy stress test; dev có thể dùng khi phát triển, test không dùng để điều chỉnh verifier. Lưu lỗi được phát hiện, sửa đúng, sửa hỏng trường hợp vốn đúng và chi phí.

## Kết quả bàn giao

- results.jsonl: SQL, kết quả, đầu ra, nguồn, trace, vòng sửa và chi phí token.
- benchmark_snapshot.jsonl và config.json: xác định dữ liệu và thiết lập của đợt chạy.
- scores.jsonl, summary.json: điểm từng câu/lần, tổng hợp theo nhóm và số lần chuyển đúng/sai.
- judge_usage.json: chi phí chấm riêng với chi phí chatbot.
- human_audit.json: phần người chấm và nguồn cho tính kappa.
- Báo cáo kết luận giới hạn theo dữ liệu/tác vụ đã thử. Nếu không cải thiện, phân tích lỗi, không mô tả kết quả kỳ vọng thành kết quả đã đạt.
