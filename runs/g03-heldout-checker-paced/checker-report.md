# Hiệu quả checker trên các bản nháp độc lập

| Nhóm | Câu gốc | Nhãn đã xác minh | Số bản | Báo lỗi | Cho qua | Chưa đủ căn cứ | Timeout | Lỗi chạy |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| Dẫn chứng | 6 | Đúng | 6 | 1/6 | 5/6 | 0/6 | 0/6 | 0/6 |
| Dẫn chứng | 6 | Sai | 6 | 6/6 | 0/6 | 0/6 | 0/6 | 0/6 |
| SQL | 4 | Đúng | 10 | 0/10 | 10/10 | 0/10 | 0/10 | 0/10 |
| SQL | 4 | Sai | 10 | 10/10 | 0/10 | 0/10 | 0/10 | 0/10 |

Báo lỗi trên bản sai được tính là phát hiện. Báo lỗi trên bản đúng được tính là báo nhầm.

| Nhóm | Mã cảnh báo khớp lỗi mục tiêu / tổng bản sai |
|---|---:|
| Dẫn chứng | 3/6 |
| SQL | 6/10 |

Đối chiếu nội dung từng cảnh báo trong summary.json trước khi kết luận checker đã chỉ ra đúng lỗi mục tiêu.
