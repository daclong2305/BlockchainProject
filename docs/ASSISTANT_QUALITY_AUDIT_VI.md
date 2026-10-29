# Mở rộng kiểm tra chất lượng bằng assistant

Theo yêu cầu mở rộng của người dùng, đã tạo 75 ca bổ sung, giữ riêng bộ chính 60 câu và thiết kế 720 đầu ra của đề xuất.

## Kết quả kiểm tra kỹ thuật

| Hạng mục | Kết quả |
|---|---:|
| SQL benchmark chạy lại khớp kết quả đã lưu | 42/42 |
| SQL benchmark có kết quả khác bản đã lưu | 0 |
| Stress SQL chuẩn khớp reference | 20/20 |
| Stress SQL cố ý sai cho kết quả khác chuẩn | 20/20 |
| Ca bổ sung | 75 |
| Chuẩn bổ sung DuckDB khớp phép tính pandas | 75/75 |
| Truy vấn biến đổi bổ sung làm thay đổi kết quả | 75/75 |

75 ca bao phủ DAI, USDC, USDT, USDe, WETH; tháng 6/7/8 năm 2026; năm loại lỗi: đại lượng, tổng hợp, tài sản, đơn vị, thời gian. Chỉ mở rộng họ avg_debt đã thuộc dev, không dùng họ test để điều chỉnh checker. Các ca có số quan sát, SQL đúng/sai, giá trị chuẩn tính bằng hai engine và cờ đánh giá máy. Chưa chạy model trên 75 ca này; không báo độ chính xác model từ các kiểm tra số học.

## Bằng chứng và tái lập

- `runs/assistant-quality-audit-v1/audit.json`: kết quả từng câu và hash nguồn.
- `runs/assistant-quality-audit-v1/supplemental_dev.jsonl`: 75 ca riêng.
- `scripts/assistant_quality_audit.py`: mã tạo và kiểm tra; từ chối ghi đè thư mục đã có.

Reexecuting cùng SQL chỉ chứng minh kết quả được tái lập, không chứng minh SQL hiểu đúng câu hỏi. Pandas kiểm tra phép tính độc lập trên cùng dữ liệu, không xác minh tính đúng của dữ liệu gốc. Câu tài liệu và các giải thích vẫn cần đối chiếu nội dung nguồn; không gắn nhãn đã xác minh khi mới kiểm tra số. Các cờ phê duyệt người giữ nguyên, không nhập assistant thành hai reviewer.

Thêm số lượng giúp tăng độ bao phủ, không tự bảo đảm chất lượng. Báo cáo chính phải tách bộ bổ sung khỏi 60 câu và giữ cả thất bại khi chạy model thật.
