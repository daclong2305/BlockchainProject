# Tái lập thí nghiệm đề xuất

Chạy PowerShell tại `C:\BlockchainProject`, dùng `.venv\Scripts\python.exe`. Không in hoặc đưa AWS credentials vào báo cáo. Dữ liệu/runtime model đã có audit riêng trong DATA_ATTRIBUTION.md và PHASE12_READINESS_VI.md.

## Phát triển và xác minh

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\run-qwen.ps1 doctor
$env:AAVE_LLM_PROVIDER='local_qwen'
.\.venv\Scripts\python.exe -m aave_analyst.cli run --split dev --limit 1 --repeats 1
```

Lệnh dev ở đây là smoke thật, không chứng minh chất lượng test. Mỗi run dùng thư mục mới. CLI benchmark luôn 120 giây; cấu hình UI không thay deadline này.

Trước final: hoàn thiện câu hỏi/nguồn/đáp án; hai người xác minh độc lập cả 60 câu và stress SQL; giải quyết bất đồng, xuất lại phiếu nếu sửa nội dung. Các phiếu hiện tại ở data/benchmark/review là bản nháp chưa được duyệt. Không tự điền người hoặc đánh dấu approved thay họ.

Đăng ký truy vết đã có tại data/benchmark/trace_registration.json: hai câu mỗi nhóm, tổng 10, không dựa điểm model. Nếu sửa nội dung benchmark trước final, giữ lịch sử đăng ký cũ và tạo phiên bản đăng ký/review phù hợp; freeze kiểm tra hash nội dung. Không đổi lựa chọn sau khi xem kết quả test.

## Khóa và final

Sau khi import hai review hợp lệ, kiểm tra provider là Qwen, khóa toàn bộ mã/prompt/model/dữ liệu. Verifier dùng cùng adapter runtime; judge dùng Claude Bedrock. Cần cấu hình judge và đơn giá được xác minh trong protocol chính thức trước chạy cuối.

```powershell
$env:AAVE_LLM_PROVIDER='local_qwen'
.\.venv\Scripts\python.exe -m aave_analyst.cli freeze
.\.venv\Scripts\python.exe -m aave_analyst.cli run --split test --final --repeats 3 --out runs/final-qwen-v1
.\.venv\Scripts\python.exe -m aave_analyst.cli coverage runs/final-qwen-v1
.\.venv\Scripts\python.exe -m aave_analyst.cli score runs/final-qwen-v1 --judge
```

Không chạy bốn bộ thí nghiệm riêng cho E1–E4. Một run final chứa 40 câu × 3 lần × 6 cấu hình. Timeout và lỗi đều giữ trong output. Bản nháp ban đầu dùng chung theo câu/lần lặp. Thư mục chứa config và benchmark snapshot trước inference; results được flush từng dòng. Không chỉnh mã hay dữ liệu khi run đang chạy. integrity.json đối chiếu hash đầu/cuối; thay đổi trong khi final làm protocol không hợp lệ.

Chấm có gọi API và tính token judge riêng. Không ghi đè scores/audit cũ. Nếu cần chấm lại, bảo tồn cả thư mục cũ và tạo phiên bản đánh giá có provenance riêng; không trộn nhãn giữa hai judge/prompt. Khi chấm lỗi, kết quả giữ trạng thái chưa biết; không công bố điểm chỉ trên phần judge thành công như điểm toàn bộ.

Mỗi đánh giá được flush/fsync vào scoring_journal.jsonl cùng usage judge. Khi bị ngắt trước khi tạo báo cáo cuối, tiếp tục với cùng câu trả lời/model/mã:

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli score runs/final-qwen-v1 --judge --resume
```

Resume không chấm lại dòng đã ghi, và từ chối hash khác. Dòng JSON dở do crash được báo lỗi, không tự xóa; bảo tồn journal gốc trước phục hồi thủ công. Lượt API đang bay tại thời điểm crash có thể đã tính phí nhưng chưa được journal ghi nhận; cần đối chiếu AWS usage để xác định hóa đơn thật. Một lần judge trả lỗi đã được ghi vẫn là lỗi của lần đánh giá đó; resume không chọn lại kết quả thuận lợi hơn.

costs.json tách phí API runtime thực (bản nháp tính một lần), phí từng cấu hình khi triển khai riêng và phí judge. Giá tham chiếu cho Haiku 4.5 geo cross-region standard là 1,10 USD/triệu token vào và 5,50 USD/triệu token ra, theo bảng giá Anthropic ngày 2026-05-27 trang 6, kiểm tra 2026-10-29: https://www-cdn.anthropic.com/files/4zrzovbb/website/3684c2faafb97418665782cea0001f439f74b1d2.pdf . Chỉ áp dụng cho model profile us.anthropic.claude-haiku-4-5-20251001-v1:0 tại us-east-1; model/region khác giữ chưa biết. Giá account/thuế/chiết khấu và điện/phần cứng không được suy đoán. Cached tokens hiện làm ước tính chưa biết để tránh dùng nhầm giá.

## Người đánh giá và kết quả

Hai người chấm độc lập mẫu audit được chọn phân tầng theo mode/category, dùng review_context để mở câu hỏi, nguồn, đáp án chuẩn và ứng viên. Không xem nhãn người kia trước khi hoàn tất. Lưu danh tính, nhãn thật và giải quyết bất đồng riêng. Sau khi đủ nhãn:

Để tránh xem trước nhãn judge, xuất hai phiếu riêng. Chỉ gửi mỗi người booklet/JSON tương ứng; không gửi human_audit.json chứa nhãn máy. Phiếu ẩn tên cấu hình và điểm judge, giữ nguyên câu trả lời và trích dẫn để kiểm tra.

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli audit-export runs/final-qwen-v1 runs/final-qwen-v1/blinded-audit
.\.venv\Scripts\python.exe -m aave_analyst.cli audit-import runs/final-qwen-v1 runs/final-qwen-v1/blinded-audit/reviewer-1.json runs/final-qwen-v1/blinded-audit/reviewer-2.json
```

Import giữ nguyên nhãn judge, không tự giải quyết bất đồng người và không ghi đè completed audit. Mẫu dùng ceil(20% số đầu ra judge thành công), phân bổ tỷ lệ theo mode/category bằng phần dư lớn nhất. Nếu đủ 720 đầu ra có judge, mẫu đúng 144; runtime/judge lỗi vẫn ở mẫu số benchmark và được báo riêng trong audit_sampling.json. Không tuyên bố đã audit 20% toàn bộ khi số đủ điều kiện thấp hơn.

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli human-report runs/final-qwen-v1/human_audit.json
```

Đo truy vết theo phiếu data/benchmark/trace_measurements.json trên repeat 0 của sáu cấu hình: bắt đầu khi mở câu trả lời, dừng khi xác minh bằng chứng hoặc ghi nhận thất bại; ghi giây thực, nguồn đã mở và ghi chú. Không thay câu thất bại bằng câu dễ hơn.

Stress SQL riêng chỉ chạy test sau hai review hợp lệ:

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli stress --split test --out runs/stress-qwen-v1.jsonl
.\.venv\Scripts\python.exe -m aave_analyst.cli stress-report runs/stress-qwen-v1.jsonl
.\.venv\Scripts\python.exe -m aave_analyst.cli trace-report data/benchmark/trace_measurements.json
```

stress-report tạo báo cáo hành vi checker và một file `.human-review.jsonl` có hai người/nhãn `final_correct` để trống. Hai người kiểm tra độc lập đầu ra với SQL/rows chuẩn, không dùng trạng thái passed làm nhãn đúng. Khi đủ nhãn, chạy stress-report trên file human-review đã điền để tổng hợp sai→đúng, đúng→sai và bất đồng. Bộ đếm coverage stress chỉ chứng minh đủ wrong/correct trong các ID đã quan sát; cần đối chiếu danh sách stress test đã khóa để chứng minh không bỏ ca.

trace-report yêu cầu khớp chính xác 60 tổ hợp ID/mode/repeat đã đăng ký. Lượt chưa đo giữ pending; không gán thời gian 0. Thành công phải ghi nguồn thực sự đã kiểm tra, thất bại phải ghi lý do. Kết quả báo median/p95 trên số đo thật, giữ các ca thất bại trong thống kê.

Trước kết luận: kiểm tra coverage, lỗi/timeouts, đầy đủ judge, nhãn/audit 20%, Cohen kappa, stress, 10 câu truy vết và chi phí. report.md tự sinh chỉ là báo cáo số đo sẵn có; không thay phân tích sai số, kiểm định yêu cầu, giới hạn dữ liệu hay xác minh thủ công. Chưa có bằng chứng thì ghi chưa hoàn tất.
