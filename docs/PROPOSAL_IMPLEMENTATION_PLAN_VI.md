# Kế hoạch thực hiện đủ đề xuất C.5

Bàn giao người đánh giá: xem HUMAN_REVIEW_HANDOFF_VI.md. Phiếu hiện hành là questions-v2 và stress-v1; không dùng phiếu lịch sử để mở final.

Goal đã được tạo ngày 2026-10-29. Hoàn thành mã và chạy kiểm thử phần mềm không đồng nghĩa hoàn thành thí nghiệm.

## Protocol dự kiến trước khi khóa

- Backbone chính: zhenlong54/qwen-vitext2sql-3b-GGUF, revision 579ae3d2f0db23dd25fd83076a57dbab79f68dd9. Sử dụng bản đã fine-tune; không yêu cầu tự huấn luyện lại.
- B0, B1, P, P-SQL, P-Evidence, P-Repair dùng cùng model và cùng bản nháp ban đầu cho mỗi câu/lần lặp. So sánh Qwen–Claude trên UI là thí nghiệm bổ sung.
- 60 câu: 20 dev, 40 test. Theo thứ tự cơ chế/tra cứu/phân tích/hỗn hợp/không trả lời được: dev 4/4/6/4/2, test 8/8/12/8/4.
- Các họ đếm giao dịch và cơ chế đã dùng để debug thuộc dev. Không chạy inference trên test để điều chỉnh hệ thống.
- Benchmark giới hạn 120 giây/câu, tối đa hai vòng sửa. Timeout UI 600 giây phục vụ khám phá, không thay giới hạn benchmark.
- Retrieval top 5, chunk 400 từ, overlap 60. Đếm phải chính xác; USD sai số tương đối tối đa 0,5%; giá trị chuẩn bằng 0 yêu cầu đúng 0.
- Judge độc lập dự kiến Claude Haiku 4.5 qua Bedrock; cấu hình và mã phải được khóa cùng dữ liệu trước final. Chưa tuyên bố protocol đã khóa.
- 40 câu × 3 lần × 6 cấu hình = 720 đầu ra; báo cáo lỗi/timeout trong mẫu số. Đơn vị phân tích là câu hỏi.

## Hạng mục và trạng thái thực

| Hạng mục | Trạng thái / phần còn lại |
|---|---|
| Dữ liệu Aave, từ điển, SQL chỉ đọc, nguồn tài liệu | Đã có triển khai và audit nguồn; giữ hash dữ liệu |
| Sinh bản nháp, kiểm chứng SQL/dẫn chứng, hai vòng sửa | Đã có; tiếp tục kiểm tra trên dev |
| Sáu cấu hình và tái sử dụng bản nháp | Đã có runner; cần kiểm tra độ phủ khi final |
| 60 câu, chống rò rỉ họ câu | Đã tạo bản nháp; chưa phải gold được duyệt |
| Hai người xác minh độc lập | Đã xuất phiếu trống; cần người thật điền và xử lý bất đồng |
| Khóa model/code/data/protocol | Có kiểm tra hash; chưa freeze vì chưa duyệt gold |
| 720 kết quả cuối | Chưa chạy; chỉ chạy sau khi đủ điều kiện khóa |
| Judge và audit người 20%, Cohen kappa | Có phần chấm/audit; chưa có kết quả và nhãn người |
| Stress SQL riêng | Đã tạo bản nháp và phiếu review; cần xác minh độc lập |
| Đo truy vết 10 câu | Đã đăng ký trước hai ID mỗi nhóm, seed 2026; 60 dòng đo trống cho lần lặp 0 của sáu cấu hình; chưa có đo người |
| E1–E4, chi phí, giới hạn, tái lập | Cần báo cáo từ kết quả thực; không điền số giả |

## Phiếu đã chuẩn bị

`data/benchmark/review/questions-v2/` và `data/benchmark/review/stress-v1/` chứa `reviewer-1.md`, `reviewer-2.md` và JSON tương ứng. Bộ questions-v2 bổ sung scope tài sản, đơn vị, các điều kiện WHERE và mốc thời gian từ SQL chuẩn; questions-v1 được giữ làm lịch sử, không dùng nhập review cho phiên bản hiện tại. Mỗi người đọc booklet riêng, kiểm tra SQL/nguồn/phạm vi rồi ghi tên và quyết định trong JSON của mình. Không xem quyết định người kia trước khi hoàn tất đánh giá độc lập.

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli review-import data/benchmark/questions.jsonl data/benchmark/review/questions-v2/reviewer-1.json data/benchmark/review/questions-v2/reviewer-2.json
```

Phiếu được gắn hash nội dung; thay câu hoặc đáp án phải xuất lại và review lại. Công cụ không chứng minh danh tính thực và không tự tạo nhãn người. Cần hoàn tất mã/protocol trước freeze; sau freeze thay đổi mã phải mở một phiên bản thí nghiệm mới.

## Độ phủ và truy vết

`data/benchmark/trace_registration.json` lưu 10 ID đã chọn trước, quy tắc chọn và hash nội dung. `trace_measurements.json` là phiếu trống, không phải kết quả đo. Việc nhập review không làm đổi hash nội dung câu; sửa câu/đáp án làm cổng freeze từ chối đăng ký cũ.

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli coverage runs/<final-run>
```

Lệnh này kiểm tra đủ 40 × 3 × 6 tổ hợp, trùng/thiếu, mã bản nháp dùng chung, và đếm lỗi runtime. Đủ độ phủ không chứng minh câu trả lời đúng. Manifest và snapshot được ghi trước inference; lần chạy bị ngắt vẫn có thông tin nguồn. Sau mỗi lần final phải kiểm tra cả coverage lẫn chấm độc lập.

## Chấm và báo cáo

`score <run-dir> --judge` tạo scores, summary, coverage, report E1–E4, usage judge và mẫu audit kèm đầy đủ ngữ cảnh nguồn/câu trả lời. Công cụ từ chối ghi đè kết quả chấm và nhãn người đã có. Không dùng `score` không có judge để kết luận chất lượng: trường chưa biết giữ `null` và báo khoảng dưới/trên thay vì loại khỏi mẫu số một cách im lặng.

Số liệu có hai tầng: `numeric_value_correct` kiểm tra số và đơn vị theo quy tắc chuẩn; `numeric_correct` còn đòi hỏi judge độc lập xác minh đại lượng, phép tổng hợp, tài sản, thời gian và nhãn kết quả. Các lỗi semantic có nhãn metric/aggregation/asset/time/unit/join/value/omission. Thiếu phán quyết phạm vi làm lần chấm chưa hoàn tất, không tự cho qua.

## Smoke dev thật ngày 2026-10-29

`runs/dev-protocol-smoke-20261029-01/` lưu một câu dev chạy Qwen thật, một lần lặp qua sáu cấu hình. B0 88,68 giây unchecked; B1 120,01 giây timeout; P 120,02 giây timeout; P-SQL 120,01 giây timeout; P-Evidence 88,68 giây checks_passed; P-Repair 97,43 giây unverified. Các trạng thái runtime không phải nhãn đúng/sai độc lập. Không gọi judge trong smoke này, vì thế báo cáo không đưa ra kết luận chất lượng.

Mục đích smoke là xác nhận runner ghi sáu đầu ra và giữ timeout thực. Mã tiếp tục được hoàn thiện trong thời gian smoke chạy; đây không phải final đã khóa. Snapshot/config/results/report được bảo tồn để truy vết. Kết quả cho thấy ngân sách 120 giây có thể bị bước sinh ban đầu sử dụng phần lớn; cần tiếp tục đo/tối ưu trên dev trước khi khóa.

## Scope v2 và payload gọn

Đã bổ sung metadata tài sản, đơn vị, điều kiện WHERE và mốc TIMESTAMPTZ cho 42/42 câu có SQL. Bản câu hỏi/scope và đăng ký truy vết cũ được giữ trong questions.scope-v1.jsonl và trace_registration.scope-v1.json. Danh sách 10 ID không đổi; hash nội dung đăng ký khớp bản mới; hiện vẫn 0 phê duyệt người.

`runs/dev-compact-payload-20261029-01/`: cùng câu dev, B0 102,63 giây, P timeout 120,01 giây. Prompt plan giảm từ 3.871 xuống 3.720 token nhờ JSON không khoảng trắng. Thời gian không cải thiện trong lượt này; cache/runtime và đầu ra khác nhau nên không suy ra quan hệ nhân quả từ hai lần smoke. integrity ghi sources_unchanged=true, code_unchanged=false vì phần báo cáo mã vẫn đang được hoàn thiện khi smoke chạy. Không dùng lượt này làm kết quả final hợp lệ hoặc kết luận chất lượng.

## Nhật ký chấm, stress và chi phí

Đã thêm scoring_journal.jsonl: mỗi đầu ra có hash, thứ tự, điểm và usage judge được flush/fsync; resume kiểm tra fingerprint toàn bộ đầu vào/judge/code, không gọi lại các dòng đã lưu. Lỗi dòng JSON dở được giữ để phục hồi thủ công, không tự xóa. Kiểm thử mô phỏng gián đoạn rồi tiếp tục xác nhận không mất usage và không gọi lại câu đã chấm.

Stress runner hiện giữ lỗi chuẩn bị ca và ghi cả bốn đầu ra wrong/correct × B1/P, không làm mất toàn lượt khi plan timeout. Kết quả stress được flush từng dòng và từ chối ghi đè file cũ. Chưa có kết quả stress test được người duyệt.

`runs/dev-independent-judge-20261029-01/` là đánh giá thử một đầu ra B0 dev đã có từ smoke đầu tiên. Không chạy lại sinh câu và không dùng câu test. Judge Bedrock trả answer_correctness=1, faithfulness=1, citation_quality=1, không lỗi; usage 4.311 input / 334 output token, ước tính phí API 0,0065791 USD theo giá standard geo cross-region đã dẫn trong costs.json. Đây chỉ là kiểm tra tích hợp: gold vẫn provisional, chưa có hai review người, nên không dùng điểm này kết luận E1–E4 hoặc xác nhận gold.

costs.json phân biệt phí API runtime thực, từng cấu hình riêng và judge; bản nháp chung chỉ tính một lần cho runtime thực. Token cache chưa có đơn giá áp dụng sẽ để chi phí chưa biết; local API bằng 0 không phải điện/phần cứng miễn phí. Final scoring còn yêu cầu integrity đầu/cuối hợp lệ bên cạnh coverage và hash judge/code.

## Báo cáo bổ sung

Audit judge đã có hai bộ phiếu riêng ẩn nhãn máy và tên cấu hình, kèm hash nguồn; import đòi hai tên khác nhau và đủ nhãn binary, giữ nguyên điểm judge. Lấy mẫu phân tầng dùng phần dư lớn nhất, đúng 144/720 nếu đủ 720 đầu ra judge thành công. Số đủ điều kiện, số lấy mẫu và tỷ lệ trên toàn bộ đầu ra được ghi riêng; không loại lỗi khỏi mẫu số benchmark.

Cổng freeze từ chối tên reviewer tương đương sau chuẩn hóa, approved không phải boolean true và mọi thao tác ghi đè khóa cũ. Các hash dữ liệu/model/judge được đọc trước khi tạo khóa để tránh để lại khóa thiếu dữ liệu khi prerequisite lỗi.

Đã có `trace-report` kiểm tra đủ đúng 60 tổ hợp của 10 ID đăng ký, không cho thay ca/nhân đôi. Thời gian phải hữu hạn, không âm; thành công có nguồn kiểm tra, thất bại có ghi chú. Chạy trên phiếu hiện tại tạo trace_measurements.report.json với measured=0, pending=60 và mọi median/p95=null.

Đã có `stress-report`: phân biệt initial flags với nhãn đúng thực, ghi độ phủ trong ID quan sát, latency và lỗi. Nhãn final_correct cần hai người khác nhau; bất đồng được báo riêng, không tự hòa giải. Chỉ đếm sửa đúng/làm sai khi hai nhãn người đồng ý. Xuất phiếu human-review trống mà không ghi đè nhãn đã có. Chưa có nhãn stress từ người thật.

## Stress dev thật và hồi quy đại lượng/tháng

`runs/dev-stress-smoke-20261029-01/` đã hoàn tất bốn đầu ra của một ca metric dev (wrong/correct × B1/P). B1 cho qua truy vấn sai đại lượng; P nêu lỗi ở cả hai bản, nhưng một phần là lỗi giả do bản phân tích chọn `supplied_usd` thay vì dư nợ và cận cuối tháng `2026-08-31T23:59:59Z`. Truy vấn chuẩn thực tế dùng `borrowed_usd` và cận trên loại trừ `2026-09-01`. Bản sai trả 2.178.906.496,656451 USD, chuẩn là 2.001.158.632,0983303 USD. Không gắn nhãn người hoặc lấy passed làm đúng.

Đã bổ sung guard độc lập dựa trên cụm từ đại lượng và tháng rõ ràng trong câu hỏi gốc, chỉ trong kiểm chứng SQL của P/ablation tương ứng. Không sửa plan chung hoặc đưa đáp án chuẩn vào runtime. Khi câu nêu hai đại lượng, phủ định hoặc nhiều khoảng tháng, guard không ép thành một yêu cầu đơn. Calendar guard xử lý đúng tháng 12 sang tháng 1; không suy diễn khoảng cho câu so sánh nhiều thời điểm.

`question-guard-audit.json` trong thư mục smoke lưu kiểm tra lại trên cùng chứng cứ dev: bản sai đổi từ chỉ time_filter thành question_metric; bản chuẩn đổi từ metric+time_filter thành không có lỗi từ guard. Đây là hồi quy checker bằng mã, không phải một lượt inference mới hay nhãn người. Hiệu quả end-to-end sau sửa vẫn cần đo dev/final theo protocol.
