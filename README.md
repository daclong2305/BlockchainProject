# Chatbot Aave V3 có dẫn chứng

Đồ án C.5: hỏi đáp tiếng Việt về giá trị tài sản cung cấp, dư nợ và thanh lý Aave V3 Ethereum. Hệ thống kết hợp tài liệu Aave và SQL; kiểm chứng ý nghĩa truy vấn, dẫn chứng từng phát biểu và sửa lỗi tối đa hai vòng.

## Trạng thái và phạm vi

- Đã tải release `data-2026-09-15`, chuẩn hóa 146.914 dòng thị trường và 25.121 sự kiện thuộc 20.159 giao dịch thanh lý.
- Năm tài sản: DAI, USDC, USDT, USDe, WETH. Benchmark giới hạn `[2025-01-01, 2026-09-01)` UTC; chatbot có thể dùng toàn bộ lịch sử có sẵn.
- Ba trang Aave được lưu HTML gốc, ngày thu thập, mã băm và 6 đoạn nguồn. Đây là kho tài liệu nhỏ; đánh giá truy xuất trên tập phát triển trước khi mở rộng.
- 60 câu và 20 trường hợp SQL sai ý nghĩa đã được tạo tại `data/benchmark/`. **Đây là bản dự thảo, chưa được hai người xác minh.** Không xem các đáp án tự động là ground truth đã kiểm chứng.
- Không bao gồm profitUSD, phí gas, APR hoặc thanh lý theo token vì chưa xác minh đầy đủ.
- Cần cấu hình quyền AWS/Bedrock để gọi mô hình thật. Chưa có kết quả thực nghiệm LLM hay kết luận P tốt hơn baseline.

## Chạy ngay trên máy này

Mở PowerShell:

```powershell
cd C:\BlockchainProject
.\.venv\Scripts\python.exe -m aave_analyst.cli doctor
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address localhost
```

Mở địa chỉ Streamlit in trên terminal (thường `http://localhost:8501`). Giao diện cần Bedrock để trả lời. Có thể chạy `powershell -ExecutionPolicy Bypass -File .\run.ps1 app`; script chỉ áp dụng chính sách cho tiến trình hiện tại, không thay đổi chính sách máy.

Giao diện **Aave Lens** hỗ trợ chat nhiều lượt trong một phiên, bốn câu hỏi gợi ý, chọn chế độ phân tích và nút **Cuộc trò chuyện mới**. Mỗi câu trả lời có trạng thái kiểm chứng, phần mở rộng để xem SQL/bảng dữ liệu/tài liệu nguồn và nút tải JSON riêng. Nút **Xuất hội thoại** tải toàn bộ phiên dưới dạng JSON. Các cảnh báo kiểm chứng thường gặp được giải thích bằng tiếng Việt; nhật ký kỹ thuật giữ nguyên để đối chiếu. Lịch sử không được lưu bền vững sau khi đóng hoặc tải lại phiên; bộ phân tích xử lý từng câu hỏi độc lập, nên cần nêu lại tài sản và khoảng thời gian khi hỏi tiếp.

Bước phân tích được cung cấp tài liệu truy xuất sơ bộ và phạm vi quan sát đọc trực tiếp từ database. Câu hỏi định nghĩa dùng tài liệu; câu hỏi kết hợp kiến thức và số liệu dùng cả tài liệu lẫn SQL. Mốc benchmark không được dùng làm giới hạn dữ liệu runtime. Nếu phân tích ban đầu yêu cầu làm rõ, cho rằng không thể trả lời, hoặc mâu thuẫn kiểu dữ liệu/ngày/chỉ số/đơn vị, hệ thống rà soát lại tối đa một lần trước khi tạo SQL. Yêu cầu thực sự thiếu thông tin vẫn được hỏi lại. Phân tích ban đầu và bản sửa nằm trong `draft.planning`; thời gian và token được tính vào cùng ngân sách câu hỏi. Min/max thời điểm quan sát không tự chứng minh dữ liệu liên tục hay đầy đủ.

Bộ kiểm tra SQL nhận câu hỏi, yêu cầu, truy vấn, kết quả và phạm vi database; nội dung tài liệu được kiểm tra riêng ở bước kiểm chứng câu trả lời. Quan hệ giữa khoảng thời gian yêu cầu và mốc sự kiện được code so sánh bằng UTC trong `interval_checks`, tránh suy luận sai thứ tự ngày. Ngày thu thập tài liệu không được xem là ngày chốt dữ liệu giao dịch.

Chạy kiểm thử offline, không gọi AWS và không tiêu token:

```powershell
.\run.ps1 test
```

## Kết nối Claude Haiku 4.5

Thiết lập mặc định: AWS region `us-east-1`, model/inference profile `us.anthropic.claude-haiku-4-5-20251001-v1:0`. Chương trình không ép dùng AWS profile khi đã cung cấp key.

1. Đặt file `env` hoặc `.env` trong thư mục project theo mẫu dưới đây (hoặc sao chép `.env.example`). Điền key trên máy, không đưa key vào mã nguồn:

```dotenv
AWS_ACCESS_KEY_ID=YOUR_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=YOUR_SECRET_KEY
AWS_SESSION_TOKEN=
AWS_DEFAULT_REGION=us-east-1
```

`AWS_SESSION_TOKEN` bắt buộc với credentials tạm thời; để trống với key dài hạn. Cũng có thể để trống các key và đặt `AWS_PROFILE` để dùng AWS CLI/SSO đã cấu hình. Tài khoản cần quyền gọi Bedrock và model/inference profile tương ứng.

2. Chạy `doctor`: `credentials_available` phải là `true`. Lệnh này chỉ kiểm tra tìm thấy credentials, chưa xác thực key hoặc quyền AWS; không gọi inference và không hiển thị thông tin bí mật.
3. Kiểm tra một lượt thật, có sử dụng API:

```powershell
$env:AWS_REGION='us-east-1'
$env:BEDROCK_MODEL_ID='us.anthropic.claude-haiku-4-5-20251001-v1:0'
.\.venv\Scripts\python.exe -m aave_analyst.cli doctor --live
.\.venv\Scripts\python.exe -m aave_analyst.cli ask 'Có bao nhiêu giao dịch thanh lý trong tháng 8/2026?' --mode P
```

Nếu tài khoản dùng inference profile khác, lấy đúng ID đã được cấp quyền từ Bedrock console và đặt biến `BEDROCK_MODEL_ID`; không tự suy đoán region/profile.

CLI và giao diện tự đọc `env` hoặc `.env`: tìm trong thư mục chạy lệnh trước, sau đó thư mục project chứa mã nguồn; nếu có cả hai tên trong cùng thư mục thì dùng `env`. Biến môi trường của tiến trình ưu tiên hơn file. Hỗ trợ cả `AWS_REGION` và `AWS_DEFAULT_REGION` (ưu tiên `AWS_REGION` trong cùng một nguồn), `BEDROCK_MODEL_ID`, `AWS_PROFILE` và `AAVE_PROJECT_ROOT`. Cú pháp file là `KEY=value`, hỗ trợ dòng chú thích `#`, `export KEY=value`, dấu nháy đơn/đôi và UTF-8 BOM; không thực thi lệnh hoặc nội suy biến. Khởi động lại ứng dụng sau khi đổi cấu hình. Cả `env` và `.env` đều bị loại khỏi Git; không gửi key vào chatbot hoặc commit credential.

## Cài lại trên máy khác

Python 3.11 trở lên:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
.\.venv\Scripts\python.exe -m aave_analyst.cli prepare
.\.venv\Scripts\python.exe -m aave_analyst.cli documents
.\.venv\Scripts\python.exe -m aave_analyst.cli benchmark
```

`prepare --source 'DUONG_DAN_THU_MUC_AAVE'` dùng dữ liệu đã giải nén. Lệnh chuẩn bị lưu bảng Parquet, database, báo cáo độ phủ và từ điển dữ liệu trong `data/processed/`. Kiểm tra giấy phép upstream trước khi phân phối lại dữ liệu; dữ liệu tải về và snapshot không được thêm vào Git mặc định.

## Hoàn thiện benchmark trước thí nghiệm

Trong `data/benchmark/questions.jsonl`, mỗi dòng có câu hỏi, family, split, nguồn, SQL chuẩn, đáp án và quy tắc số liệu. Hai thành viên cần đọc câu hỏi, chạy SQL và đọc đoạn nguồn, sửa các nội dung chưa phù hợp; sau đó điền:

```json
"review": {"reviewer_1": "TenNguoi1", "reviewer_2": "TenNguoi2", "approved": true, "notes": "Da doi chieu SQL va nguon"}
```

Tên reviewer phải khác nhau. Phần mềm kiểm tra trường phê duyệt, **không chứng minh việc kiểm tra thủ công đã xảy ra**. Xem `docs/EXPERIMENTS.md` để biết quy trình. Không tạo biến thể từ cùng một họ câu hỏi ở hai tập.

- Số đếm phải bằng tuyệt đối.
- USD bằng nhau sau làm tròn `ROUND_HALF_UP` đến hai chữ số, trừ khi câu hỏi quy định khác.
- So sánh giá trị kết quả; không bắt SQL hoặc alias cột phải giống nhau. Judge kiểm tra thêm ý nghĩa, tài sản, thời gian và dẫn chứng.
- Chỉ dùng 20 câu dev để điều chỉnh. Không đưa câu/đáp án/SQL chuẩn vào RAG hay prompt xử lý.

Lệnh `benchmark` không ghi đè file đã có; `--overwrite` chỉ dành cho lúc chủ động bỏ bản nháp cũ. Sau khi có phê duyệt:

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli freeze
```

Lệnh khóa hash dữ liệu, tài liệu, benchmark và cấu hình model. Nếu thay đổi nguồn phải ghi nhận phiên bản mới, không trộn kết quả.

## Thí nghiệm

```powershell
# Pilot: 2 câu dev, 1 lần, chỉ B0 và P; có gọi Bedrock.
.\.venv\Scripts\python.exe -m aave_analyst.cli run --split dev --limit 2 --repeats 1 --modes B0 P

# Chỉ sau khi khóa benchmark; 40 x 6 x 3 = 720 đầu ra, nhiều hơn 720 API calls.
.\.venv\Scripts\python.exe -m aave_analyst.cli run --split test --final

# Thay đường dẫn bằng thư mục run được in ra.
.\.venv\Scripts\python.exe -m aave_analyst.cli score 'runs\TEN_RUN' --judge
```

Không có `--judge` thì chỉ tính kiểm tra số liệu; độ đúng toàn bộ chưa chấm được để `null`, không xem là 0 hoặc 100%. Judge token được lưu riêng. Chi phí USD để trống đến khi điền giá thực tế của tài khoản, không suy đoán giá.

Sáu cấu hình: B0, B1, P, P-SQL, P-Evidence, P-Repair. Mỗi câu/lần dùng cùng một bản nháp. Chi phí tạo nháp tính cho từng cấu hình khi so sánh. Mỗi cấu hình có tối đa 120 giây đầu cuối, hai vòng sửa chung; mỗi vòng tối đa một truy xuất và hai SQL (hiện một SQL sửa + một kiểm tra coverage). Nếu mô hình trả JSON sai định dạng, mỗi lệnh gọi được yêu cầu trả lại tối đa một lần trong thời gian còn lại; đây là sửa định dạng, không tăng số vòng sửa nội dung. Token và thời gian của cả hai lần đều được ghi nhận. Chương trình không tự bỏ qua JSON thừa vì có thể làm mất kết quả kiểm chứng. Không sử dụng thời gian chờ giữa các cấu hình làm thời gian xử lý của câu. Lỗi/timeout/từ chối nhầm vẫn lưu và tính.

## Cấu trúc

```text
src/aave_analyst/
  data.py           Tải, chuẩn hóa, audit, từ điển dữ liệu
  database.py       DuckDB và kiểm tra quyền truy vấn chỉ đọc
  retrieval.py      Snapshot tài liệu và BM25
  llm.py            Bedrock Converse và prompt tách vai trò
  verification.py   Quy tắc SQL, coverage và kiểm chứng dẫn chứng
  pipeline.py       B0/B1/P, ablations và vòng sửa có giới hạn
  benchmark.py      Benchmark dự thảo, validation và khóa dữ liệu
  experiments.py    Chạy ghép cặp, judge, chỉ số và mẫu kiểm tra người
  stress.py         Các trường hợp SQL chạy được nhưng sai ý nghĩa
  cli.py            Lệnh thao tác
app.py              Giao diện Streamlit
tests/              Kiểm thử offline
docs/               Kế hoạch, tiến độ, quy trình thực nghiệm
```

## Giới hạn cần báo cáo

Quy tắc SQL không chứng minh truy vấn đúng tuyệt đối. LLM có thể trích xuất yêu cầu sai hoặc kiểm chứng sai. Haiku được dùng ở nhiều vai trò nên judge có thể có thiên lệch tương quan; mẫu hai người chấm độc lập là cần thiết. Kho ba trang không bao phủ toàn bộ Aave. 40 câu test là phạm vi thí nghiệm nhỏ; ba lần chạy cùng câu không tạo ra ba câu độc lập. `checks_passed` chỉ là trạng thái của bộ kiểm tra, không phải nhãn đúng của benchmark.

## Dùng Qwen ViText2SQL GGUF local

Model người dùng chọn: `zhenlong54/qwen-vitext2sql-3b-GGUF`, revision `579ae3d2f0db23dd25fd83076a57dbab79f68dd9`, file Q4_K_M. Trạng thái đã fine-tune do người dùng cung cấp; chưa có recipe/checkpoint nguồn để tái lập phần fine-tune đó.

```powershell
cd C:\BlockchainProject
.\.venv\Scripts\python.exe scripts/setup_local_qwen.py
.\run-qwen.ps1 doctor
.\run-qwen.ps1 app
```

Setup tải khoảng 1,93 GB model và runtime llama.cpp b11962 Vulkan, kiểm tra SHA-256 trước khi dùng. `run-qwen.ps1` chọn local_qwen cho tất cả vai trò runtime, tự khởi động server 127.0.0.1:8081 với context 8192, offload toàn bộ layers, batch 512 và micro-batch 128; không cần cài CUDA. Server tiếp tục chạy để tái sử dụng sau khi đóng app. PID và log ở `.tmp/qwen-server.*`; muốn dừng, kiểm tra PID thuộc llama-server rồi dừng tiến trình đó.

Có thể khởi động server thủ công bằng `scripts/start_local_qwen.ps1 -GpuLayers 0` để dùng CPU khi VRAM không đủ; đặt AAVE_LLM_PROVIDER=local_qwen và QWEN_BASE_URL=http://127.0.0.1:8081 trong terminal gọi CLI/app. `run.ps1` cũ vẫn dùng cấu hình provider hiện tại (mặc định Bedrock); dùng `run-qwen.ps1` để chọn Qwen rõ ràng. Chấm điểm bằng `score --judge` vẫn chọn Bedrock riêng và có phí; không chạy trong bước này.

Thử một câu SQL cục bộ sau khi server sẵn sàng:

```powershell
.\.venv\Scripts\python.exe scripts/smoke_local_qwen.py
```

Đây là smoke test riêng, không phải benchmark và không tạo bộ train/test. Qwen 3B có thể chưa theo tốt schema JSON hoặc các vai trò kiểm chứng dài; cần đánh giá riêng trước khi kết luận chất lượng. Timeout tương tác UI mặc định 600 giây/model, điều chỉnh từ 120 đến 3600 giây trong sidebar. CLI/benchmark vẫn mặc định 120 giây. Model/runtime/dữ liệu và logs bị loại khỏi Git.

Kết quả smoke trên máy này: một truy vấn Qwen trả đúng 107 giao dịch tháng 8/2026; lần sinh khác lỗi SQL. Luồng P dùng Qwen cho mọi vai trò chưa đạt (planning sai routing và timeout 120 giây). Đường local đã kết nối được nhưng hiện là lựa chọn thử nghiệm; xem docs/PHASE12_READINESS_VI.md, mục 11. Không coi kết quả này là benchmark hay bằng chứng Qwen thay thế đầy đủ Claude.

## So sánh Qwen – Claude trên UI

Trong sidebar, chọn **Không gian làm việc → So sánh Qwen – Claude**, nhập một câu hỏi và chọn phương pháp dùng chung (B0/B1/P/...). Bấm **Chạy so sánh Qwen + Claude** để thực hiện. Mỗi lần bấm chạy sẽ gọi Qwen local và Claude qua Bedrock; **Bedrock có phát sinh phí**. Đổi lựa chọn, tải JSON hoặc repaint giao diện không tự gửi yêu cầu mới.

Hai bên dùng cùng database, kho tài liệu, câu hỏi, phương pháp, prompts/runtime và deadline dùng chung do người dùng chọn (mặc định 600 giây/model); chạy lần lượt Qwen rồi Claude. UI hiển thị câu trả lời, SQL/bảng kết quả, tài liệu/dẫn chứng, trạng thái kiểm chứng, số vòng sửa, thời gian, số lượt gọi và token vào/ra cạnh nhau. Lỗi hoặc timeout giữ nguyên trên bên bị lỗi, bên còn lại vẫn được thực hiện; không có fallback model. Snapshot database/dictionary/chunks được hash trước và sau; cảnh báo nếu thay đổi. JSON xuất ra có cấu hình model, input/code hashes và kết quả từng bên. Đây là so sánh từng câu tương tác, không tự tạo/chạy final benchmark hoặc kết luận model thắng.

Khởi động Qwen bằng `run-qwen.ps1 app`; server local cần sẵn sàng ở 127.0.0.1:8081, Claude cần credentials/quyền Bedrock như hướng dẫn bên trên. Trong **Hội thoại**, ô **Model hội thoại** cho chọn Qwen local, Claude Bedrock hoặc theo cấu hình khởi động. Lựa chọn ở hội thoại không thay đổi hai model cố định của phần so sánh. Lịch sử so sánh chỉ giữ trong phiên; tải JSON trước khi đóng trang để lưu kết quả.

Timeout UI áp dụng cho cả hội thoại và so sánh, trên toàn bộ các bước của một câu hỏi; hai model nhận cùng ngân sách. Kết quả so sánh ghi deadline_seconds_per_model; kết quả hội thoại ghi deadline_seconds để phân biệt các lần chạy. Thay đổi mức này không tự chạy lại câu hỏi và không thay protocol benchmark 120 giây. Tăng timeout không sửa lỗi routing/SQL hoặc thiếu credentials Bedrock.


Cập nhật 29/10/2026: đã sửa routing bỏ qua SQL bằng role JSON schema/kiểm tra kế hoạch, và chuyển đổi hẹp quote ngày ISO cho DuckDB (có lưu SQL gốc). Kiểm tra thực tế Qwen đã thực thi COUNT(DISTINCT tx_hash) trả 107, khớp truy vấn độc lập; luồng P 150,74 giây, vẫn unverified do reviewer của model. **124 test offline đạt**. Xem docs/QWEN_SQL_ROUTING_FIX_VI.md; các kết quả lỗi ở phần trên là trước sửa, không phải benchmark.


Nguồn giấy phép số liệu Aave: [DATA_ATTRIBUTION.md](docs/DATA_ATTRIBUTION.md). Audit đối chiếu toàn bộ các quan sát runtime với một bản Zenodo của cùng publisher khai báo CC BY 4.0; snapshot runtime vẫn pin data-2026-09-15. Xem file này để ghi công và phân biệt giấy phép dataset với model/tài liệu/mã nguồn.
