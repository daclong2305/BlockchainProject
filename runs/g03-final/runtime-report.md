# Độ trễ và chi phí benchmark G03

Chạy 40 câu × 3 lượt trên mỗi cấu hình, dùng 120 bản nháp chung. Đã xác nhận đủ 360 đầu ra và khớp hồ sơ khóa.

| Cấu hình | Đầu ra | Lỗi thực thi | Trung vị (giây) | p95 (giây) |
|---|---:|---:|---:|---:|
| B0 | 120 | 0 | 21.69 | 26.62 |
| B1 | 120 | 0 | 32.27 | 80.64 |
| P | 120 | 0 | 40.66 | 104.12 |

Thời gian đầu cuối của mỗi cấu hình gồm bước tạo bản nháp và thời gian chờ do giãn cách 8 giây giữa các lượt gọi. Chi phí benchmark tính mỗi bản nháp dùng chung một lần.

Chi phí API ước tính 7.17 USD cho 4,393,511 token đầu vào và 424,619 token đầu ra. Có 0 lượt thiếu thông tin token.

Hai phiếu chấm mù có 248 mục sau khi gộp các đầu ra cùng câu có nội dung và bằng chứng trùng khớp. Độ đúng, dẫn chứng và các chuyển đổi theo cặp sẽ được tổng hợp sau khi nhập điểm đã phân xử.
