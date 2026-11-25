# Phân tích cảnh báo checker trên tập độc lập

Checker chạy trên 32 bản nháp có nhãn đã được hai người xác minh. Lượt có giãn cách gọi Bedrock hoàn tất 32/32 bản. Log của lượt đầu, bị giới hạn tần suất ở 26 bản, được lưu tại `runs/g03-heldout-checker/`.

| Nhóm | Phát hiện trên bản sai | Báo nhầm trên bản đúng | Chưa đủ căn cứ | Trùng mã lỗi mục tiêu |
|---|---:|---:|---:|---:|
| Dẫn chứng | 6/6 | 1/6 | 0/12 | 3/6 |
| SQL | 10/10 | 0/10 | 0/20 | 6/10 |

## Báo nhầm ở phép so sánh hai mốc giờ

Ở EC03-B, câu hỏi yêu cầu lấy giá trị cung cấp USDC tại 00:00 UTC ngày 2/7/2025 trừ giá trị tại 00:00 UTC ngày 1/7/2025. Truy vấn dùng hai điều kiện `FILTER` khớp chính xác hai thời điểm. DuckDB có đúng một bản ghi cho mỗi thời điểm. Kết quả chênh lệch là 21.596.989,02 USD.

Checker cho rằng cận trên phải là 00:00 ngày 2/7 thay cho 01:00 cùng ngày. Cận trên trong SQL là cận loại trừ. Chạy lại với cận checker đề xuất loại mất mốc ngày 2/7 và trả `NULL`. Trong truy vấn ban đầu, mỗi phép `MAX` chỉ nhận một dòng sau `FILTER`, nên cho đúng giá trị tại mốc được hỏi.

## Mã cảnh báo và nội dung cảnh báo

Một số cảnh báo chỉ ra lỗi mục tiêu dù mã do mô hình đặt nằm ngoài danh sách đã dùng để tính chỉ số trùng mã:

| Bản nháp | Nội dung cảnh báo |
|---|---|
| EC03-A | Phát hiện câu trả lời đổi ngày 2/7 thành 3/7. Checker đồng thời đưa ra hai nhận xét sai về SQL, giống trên bản đối chứng đúng EC03-B. |
| EC04-B | Chỉ ra nguồn thanh lý được dùng để dẫn một phát biểu về cung cấp tài sản. |
| EC06-B | Chỉ ra câu trả lời gán số dư nợ DAI cho WETH và trỏ nhầm hàng trong SQL1. |
| S014-B và S019-A | Chỉ ra truy vấn chia giá trị USD cho một triệu rồi ghi kết quả như USD. |
| S015-A và S020-B | Chỉ ra phép nối với tài sản khác làm truy vấn tính khoảng chênh lệch từ hai tài sản. |

Giữ nguyên chỉ số trùng mã đã định nghĩa. Dùng ghi chú theo ca để trình bày cả lỗi mục tiêu được phát hiện và cảnh báo sai đi kèm.
