# Báo cáo E1–E4

Final được khai báo: False. Độ phủ final đạt: False.
Đầu ra: 1/0 theo protocol final. Lỗi runtime: 0.
Độ phủ không chứng minh chất lượng hoặc phê duyệt của người. Báo cáo thiếu judge không được dùng kết luận hiệu quả.

| Cấu hình | Đầu ra | Đã chấm | Đúng toàn bộ | Độ đúng | Số liệu đúng/đã chấm | Median giây | p95 giây | Lỗi runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| B0 | 1 | 1 | 1 | 1.0000 | 0/0 | 88.6836 | 88.6836 | 0 |

## E1 — Hiệu quả tổng thể

So sánh B0, B1, P bằng độ đúng toàn bộ, dẫn chứng và từ chối. Điểm chưa chấm là chưa biết; timeout/lỗi là sai, không loại khỏi mẫu số.

## E2 — Ý nghĩa SQL

So sánh P với P-SQL. numeric_value_correct kiểm tra giá trị/đơn vị; numeric_correct còn yêu cầu judge kiểm tra đại lượng, tổng hợp, tài sản và thời gian. Stress SQL được báo cáo riêng.

## E3 — Dẫn chứng

| Cấu hình | Citation precision | Citation completeness | Phát biểu thiếu căn cứ | Từ chối sai |
|---|---:|---:|---:|---:|

## E4 — Vòng sửa

| P so với | Sai → đúng | Đúng → sai | Cặp đã chấm |
|---|---:|---:|---:|
| B0 | 0 | 0 | 0 |
| B1 | 0 | 0 | 0 |
| P-SQL | 0 | 0 | 0 |
| P-Evidence | 0 | 0 | 0 |
| P-Repair | 0 | 0 | 0 |

## Chi phí và giới hạn

Token và độ trễ thực có trong summary.json; token judge trong judge_usage.json. costs.json lưu ước tính phí API theo đơn giá đã kiểm tra cho đúng model/profile/region; cấu hình chưa có đơn giá giữ null. Chi phí điện/phần cứng chưa xác minh; phí API local bằng 0 không đồng nghĩa tổng chi phí bằng 0.
Bản nháp dùng chung được tính vào token mỗi cấu hình để so sánh khi triển khai riêng; không cộng sáu cấu hình để suy ra hóa đơn thực vì sẽ đếm trùng bản nháp.
Chưa kết luận H1–H3 nếu thiếu chấm độc lập, audit người 20%, Cohen kappa, stress SQL hoặc đo truy vết. Benchmark nhỏ và ba lần lặp không phải ba câu hỏi độc lập.
