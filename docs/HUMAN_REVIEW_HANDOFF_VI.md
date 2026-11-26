# Bàn giao chấm độc lập G03

Hai người duyệt điền phiếu riêng bằng tên thật và giữ bản ban đầu trước khi trao đổi. Kiểm tra đáp án số liệu bằng SQL trên Aave DuckDB. Với câu cơ chế, chỉ rõ đoạn tài liệu hỗ trợ. Ghi yêu cầu sửa nếu ý hỏi, nguồn, thời gian, đơn vị hoặc đáp án chưa xác minh được. Phiếu dev-20 và phiếu chấm final đã được hai người có tên trong phiếu xác nhận theo thông tin bàn giao ngày 26/11/2026. Khi tái lập thí nghiệm, dùng đúng phiên bản phiếu và mã băm đi kèm.

| Việc cần duyệt | Phiếu |
|---|---|
| Tham chiếu cho 20 câu dev và 40 câu test | `report/human-review/questions-v2/reviewer-1` và `reviewer-2`, gồm bản đọc Markdown và JSON điền kết quả |
| Rubric qua 24 đầu ra dev được che tên cấu hình | `report/g03-final/review-rubric/reviewer-1` và `reviewer-2` |
| Bản đúng/sai của checker | Quy trình và vị trí phiếu ở `report/g03-final/checker-review.md` |

Snapshot và hồ sơ khóa lưu metadata tại thời điểm chạy, gồm nhãn reviewer cũ. Xác nhận người duyệt được ghi nhận ngày 26/11/2026 áp dụng cho các phiếu hiện hành; khi tái lập, đối chiếu chúng với mã băm nguồn. Các bước dưới đây mô tả quy trình cho một phiên bản thí nghiệm mới.

## Trước khi khóa

Điền `approved` chỉ sau khi đã xác minh tham chiếu. Nếu cần sửa nội dung, xuất phiếu mới và xác minh lại phiên bản đã sửa. Khi chấm hiệu chuẩn, đọc rubric trong phiếu, điền điểm 0/1 và lý do, rồi đánh dấu `rubric_approved: true` khi đồng ý dùng phiên bản này. Nếu lệnh báo bất đồng, điền file phân xử được sinh ra và chạy lại với `--adjudication` trỏ đến file đó.

Phiếu benchmark v2 hiện có quyết định cho đủ 60 câu. Khi chuyển từ v1, 48 câu giữ nguyên mã băm nội dung; Q007–Q012, Q021–Q022, Q049–Q050 và Q053–Q054 được rà lại theo nội dung mới. Phiếu v1 được giữ tại `report/human-review/questions/`. Kho truy xuất đã bổ sung nguồn rút tài sản của Aave. Mã băm kho mới đã được cập nhật trong hồ sơ checker sau khi đối chiếu nội dung của đủ 32 bản nháp.

```powershell
$g03Python = '.\.venv\Scripts\python.exe'
& $g03Python -m aave_analyst.cli review-import data/benchmark/questions.jsonl report/human-review/questions-v2/reviewer-1.json report/human-review/questions-v2/reviewer-2.json
& $g03Python -m aave_analyst.g03_report calibrate report/g03-final/review-rubric/reviewer-1.json report/g03-final/review-rubric/reviewer-2.json --adjudication report/g03-final/review-rubric/calibration-adjudication.json
```

Hoàn tất duyệt checker theo hướng dẫn đi kèm. Giữ bộ ca ngoài lần sửa dev. Sau khi đạt hồi quy dev và hoàn tất các phiếu, đăng ký truy vết rồi khóa cấu hình.

```powershell
& $g03Python -m aave_analyst.cli trace-register
& $g03Python -m aave_analyst.cli freeze
& $g03Python -m aave_analyst.cli run --split test --modes B0 B1 P --repeats 3 --final --out runs/g03-final
```

## Sau khi có 360 đầu ra

Xuất phiếu chấm trước khi đối chiếu kết quả judge. Chỉ gửi thư mục phiếu cho hai người chấm vì log thô và file ánh xạ giữ tên cấu hình. Phiếu gộp các bản trả lời trùng cả nội dung và bằng chứng cho cùng một câu. Mỗi nhãn được ánh xạ về đầy đủ các lượt trong bảng kết quả. Người chấm đánh dấu `observed_refusal` theo nội dung câu trả lời cuối.

```powershell
& $g03Python -m aave_analyst.g03_report final-export runs/g03-final runs/g03-final/blind-review
& $g03Python -m aave_analyst.cli score runs/g03-final --judge
& $g03Python -m aave_analyst.g03_report final-import runs/g03-final runs/g03-final/blind-review/reviewer-1.json runs/g03-final/blind-review/reviewer-2.json
```

Nếu có bất đồng, hai người thống nhất điểm và lý do trong file phân xử do lệnh in đường dẫn. Chạy lại lệnh cuối với `--adjudication` trỏ đến file đã điền. Báo cáo được ghi vào `final-human-report.md`. File `final-human-summary.json` chứa các cặp B0 → P, B1 → P, độ trễ, chi phí, độ khớp với judge và case test được chọn cho slide. Đưa thêm bảng đánh giá checker độc lập vào report. Ghi riêng lỗi mới quan sát trên test để giữ nguyên cấu hình của đợt đánh giá.
