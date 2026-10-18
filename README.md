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
cd F:\Code\BlockchainProject
.\.venv\Scripts\python.exe -m aave_analyst.cli doctor
.\.venv\Scripts\python.exe -m streamlit run app.py --server.address localhost
```

Mở địa chỉ Streamlit in trên terminal (thường `http://localhost:8501`). Giao diện cần Bedrock để trả lời. Có thể chạy `powershell -ExecutionPolicy Bypass -File .\run.ps1 app`; script chỉ áp dụng chính sách cho tiến trình hiện tại, không thay đổi chính sách máy.

Chạy kiểm thử offline, không gọi AWS và không tiêu token:

```powershell
.\run.ps1 test
```

## Kết nối Claude Haiku 4.5

Thiết lập mặc định: AWS region `us-east-1`, profile `default`, model/inference profile `us.anthropic.claude-haiku-4-5-20251001-v1:0`.

1. Cấu hình đăng nhập AWS trên máy bằng cách tài khoản của bạn hỗ trợ, chẳng hạn AWS CLI/SSO. Profile phải có quyền gọi Bedrock và quyền truy cập model/inference profile tương ứng.
2. Chạy `doctor`: `credentials_available` phải là `true`. Lệnh này không gọi inference và không hiển thị thông tin bí mật.
3. Kiểm tra một lượt thật, có sử dụng API:

```powershell
$env:AWS_REGION='us-east-1'
$env:AWS_PROFILE='default'
$env:BEDROCK_MODEL_ID='us.anthropic.claude-haiku-4-5-20251001-v1:0'
.\.venv\Scripts\python.exe -m aave_analyst.cli doctor --live
.\.venv\Scripts\python.exe -m aave_analyst.cli ask 'Có bao nhiêu giao dịch thanh lý trong tháng 8/2026?' --mode P
```

Nếu tài khoản dùng inference profile khác, lấy đúng ID đã được cấp quyền từ Bedrock console và đặt biến `BEDROCK_MODEL_ID`; không tự suy đoán region/profile. `.env.example` chỉ là hướng dẫn, chương trình đọc **biến môi trường**, không tự nạp `.env`. Không gửi key vào chatbot hoặc commit credential.

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

Sáu cấu hình: B0, B1, P, P-SQL, P-Evidence, P-Repair. Mỗi câu/lần dùng cùng một bản nháp. Chi phí tạo nháp tính cho từng cấu hình khi so sánh. Mỗi cấu hình có tối đa 120 giây đầu cuối, hai vòng sửa chung; mỗi vòng tối đa một truy xuất và hai SQL (hiện một SQL sửa + một kiểm tra coverage). Không sử dụng thời gian chờ giữa các cấu hình làm thời gian xử lý của câu. Lỗi/timeout/từ chối nhầm vẫn lưu và tính.

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
