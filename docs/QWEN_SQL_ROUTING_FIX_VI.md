# Sửa lỗi Qwen không sinh/thực thi SQL — 29/10/2026

## Kết quả đã xác minh

Dùng đúng zhenlong54/qwen-vitext2sql-3b-GGUF, revision 579ae3d2f0db23dd25fd83076a57dbab79f68dd9; không đổi model, không fine-tune, không chèn SQL/đáp án chuẩn vào prompt. Câu chẩn đoán: “Có bao nhiêu giao dịch thanh lý trong tháng 8 năm 2026?”. Không tạo tập train/test hoặc chạy final benchmark.

Sau sửa, Qwen sinh SQL đếm distinct tx_hash, SQL được thực thi trên DuckDB và trả **107**, bằng truy vấn độc lập. Luồng P hoàn tất **150,74 giây**, không timeout, nhưng vẫn **unverified** do model review trả nhận xét chung chung “specific SQL mismatch with evidence”. Không đổi trạng thái thành passed. Đây là một kiểm tra chẩn đoán, không phải số đo accuracy toàn model.

Bản ghi thực: runs/diagnostics/qwen-fixed-draft-20261029T123135Z.json và qwen-fixed-result-20261029T123135Z.json. Tóm tắt kèm model config, input hashes và kiểm tra độc lập: docs/phase12-evidence/qwen-routing-fix-summary.json. Các lần thất bại trước sửa vẫn được giữ trong runs/diagnostics, không xóa hoặc ghi đè để tạo kết quả đẹp.

## Nguyên nhân và sửa đổi

1. Model trả kind=docs với metric=transactions; pipeline chấp nhận và bỏ bước SQL. Khi yêu cầu review, model có thể chuyển thành unanswerable dù có sẵn loaded-dataset liquidation metric/interval. Đã thêm kiểm tra mâu thuẫn routing và kiểm tra availability, một lần rà soát tối đa; nếu vẫn sai thì báo lỗi, không bịa số 0.
2. Adapter trước đây chỉ yêu cầu JSON object bất kỳ. Đã thêm JSON schema theo role và kiểm tra schema ở client. Plan giải mã metric trước, ràng buộc metric số liệu vào data/mixed; docs/unanswerable dùng metric=other. Không ràng buộc giá trị đáp án, SQL hay ngày theo câu chẩn đoán. Cấu hình ghi role_schema_version=2. Các request plan dùng cùng workflow instruction ở pipeline cho cả providers: dữ liệu giao dịch được lấy ở bước SQL tiếp theo, không cần đính kèm từng hàng ngay lúc planning.
3. SQL sinh ra dùng dấu nháy kép cho ngày ISO, khiến DuckDB hiểu thành tên cột và báo Binder Error. Thêm chuyển đổi AST hẹp: chỉ quoted identifier có giá trị ngày ISO hợp lệ, nằm trong toán hạng so sánh/BETWEEN với time/hour/source_timestamp. Không đổi aggregate, asset, khoảng thời gian hoặc giá trị; không thay tên cột bình thường. Bỏ qua CTE/date-shaped aliases để tránh thay đổi định danh có thật. SQL trước/sau lưu trong draft.planning.sql_normalizations và hiện trên UI. Cả hai providers dùng cùng chuyển đổi; allowlist SQL vẫn áp dụng.
4. Không còn ép scalar answer=0 thành chuỗi “0” ở pipeline: output answer phải đúng kiểu string. Điều này kiểm tra định dạng, không tự chứng minh nội dung đúng.

SQL gốc của lần thành công:

```sql
select count ( distinct tx_hash ) from liquidation_events
where time >= "2026-08-01" and time < "2026-09-01"
```

SQL thực thi:

```sql
SELECT COUNT(DISTINCT tx_hash) FROM liquidation_events
WHERE time >= '2026-08-01' AND time < '2026-09-01'
```

## Kiểm thử và giới hạn

**124 test offline đạt** tại pytest-qwen-routing.xml. Bao gồm routing review/fail-closed, JSON role contract, từ chối scalar answer, chuyển quote ngày, không chạm quoted columns/aliases/CTE và không vượt SQL guard. Kiểm tra chẩn đoán chạy Qwen local, không phát sinh thêm Bedrock calls trong quá trình sửa.

Lượt so sánh sau khi người dùng cấu hình AWS đã hoàn tất trước đó: runs/comparisons/1ad7e12ad7e64e7bacea423cb93a8337.json, Claude trả đúng 107 bằng SQL (22,36 giây, unverified do nhận xét reviewer); Qwen lúc đó trả 0, không SQL (146,11 giây). Không được trộn kết quả trước và sau sửa thành một lượt so sánh mới. Người dùng cần bấm chạy lại nếu muốn so sánh hai providers trên code hiện tại; một lần đúng không chứng minh chất lượng tương đương Claude.

Nguồn API schema llama.cpp: https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md — response_format hỗ trợ JSON schema. JSON schema giúp định dạng/quan hệ trường; không bảo đảm model hiểu đúng mọi câu hoặc viết SQL đúng ngữ nghĩa. Vẫn giữ verifier và timeout 600 giây UI.
