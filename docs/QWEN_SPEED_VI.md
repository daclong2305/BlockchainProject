# Đo tối ưu payload Qwen — 2026-10-29

Thay đổi chỉ áp dụng adapter local: plan nhận catalog ID/title/URL để phân loại ý định; toàn văn giữ trong context gốc, plan_review, answer và claim_review. Không cắt kết quả SQL hoặc nguồn ở bước trả lời/kiểm chứng. Bỏ retrieval telemetry khỏi answer transport. Không giảm số vòng kiểm chứng hoặc thay deadline. Adapter ghi payload version stage_payload_v2 trong config.

## Một lượt dev cùng câu health factor

| Lượt | B0 giây | P giây | P trạng thái |
|---|---:|---:|---|
| dev-protocol-smoke-20261029-01 | 88,68 | 120,02 | timeout |
| dev-compact-payload-20261029-01 | 102,63 | 120,01 | timeout |
| dev-stage-payload-20261029-01 | 51,79 | 95,10 | checks_passed |

Lượt mới: plan 1.874 input token / 6,37 giây; answer 3.445 input token / 45,34 giây. P không cần vòng sửa. Hash mã và dữ liệu đầu/cuối đều khớp. Bản trả lời nêu health factor là độ an toàn vị thế, dưới 1 có nguy cơ thanh lý. Trạng thái checker không phải đánh giá độc lập về độ đúng/dẫn chứng.

Đây là một mẫu dev, không phải benchmark tốc độ có kiểm soát cache hay phân bố độ trễ. Các lần trước có phiên bản prompt khác và cache khác, nên không quy toàn bộ chênh lệch cho một thay đổi. Cần đo trên nhiều câu dev, kiểm tra routing docs/data/mixed và chất lượng trước khi khóa final. Chưa có thay đổi runtime GPU, không tuyên bố đã tối ưu batch hoặc cache server.

Bằng chứng: runs/dev-stage-payload-20261029-01/config.json, results.jsonl, integrity.json. Toàn bộ test suite đã qua sau thay đổi.
