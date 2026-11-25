# Rubric chấm câu trả lời Aave

Đọc câu hỏi, phạm vi, đáp án đã duyệt, câu trả lời cuối và bằng chứng thực tế. Chấm từng tiêu chí bằng 0 hoặc 1. Đánh giá cả cảnh báo xuất hiện trong câu trả lời. Ghi phát biểu, ô SQL hoặc đoạn tài liệu giải thích điểm.

| Tiêu chí | 1 điểm | 0 điểm |
|---|---|---|
| Đúng và đủ nội dung `answer_correctness` | Trả lời đầy đủ các ý bắt buộc. Ví dụ, giải thích health factor dưới 1 khiến vị thế có thể bị thanh lý. Với câu số liệu, kiểm đúng đại lượng, tài sản, khoảng thời gian, đơn vị và phép tổng hợp. | Thiếu ý bắt buộc, trả lời sai phạm vi hoặc thêm cảnh báo làm thay đổi kết luận. Ví dụ, Q030 có số trung bình đúng nhưng khẳng định USDe tháng 8/2026 nằm ngoài dữ liệu. |
| Tính căn cứ `faithfulness` | Mọi phát biểu thực tế đều được tài liệu hoặc kết quả SQL có sẵn hỗ trợ. Ví dụ, tài liệu giải thích bổ sung thế chấp hoặc trả bớt nợ có thể cải thiện health factor. | Có phát biểu thiếu căn cứ hoặc trái nguồn. Ví dụ, khẳng định lãi suất gửi luôn cố định khi tài liệu mô tả lãi suất thay đổi. |
| Chất lượng dẫn chứng `citation_quality` | Mỗi phát biểu cần dẫn chứng trỏ đến nguồn hỗ trợ đúng phát biểu. Ví dụ, dư nợ USDC trỏ đến kết quả SQL lấy `borrowed_usd` cho đúng USDC và khoảng thời gian yêu cầu. | Thiếu mã nguồn, nguồn sai hoặc nguồn không chứng minh phát biểu. Ví dụ, trả đúng con số dư nợ USDC nhưng trỏ đến kết quả WETH. Độ đúng của con số và chất lượng dẫn chứng được chấm riêng. |

- Số đếm phải khớp tuyệt đối. Số liệu định lượng dùng ngưỡng của benchmark, mặc định sai số tương đối tối đa 0,5%. Khi đáp án tham chiếu bằng 0, kết quả phải bằng 0. Giá trị khớp vẫn cần đúng ngữ nghĩa và đơn vị.
- Khi câu hỏi có đủ dữ liệu, từ chối là sai. Khi tham chiếu yêu cầu từ chối, câu trả lời cần nêu lý do và tránh suy đoán. Chấm dẫn chứng cho các phát biểu thực tế trong phần giải thích.
- Chấm những gì câu hỏi yêu cầu. Ví dụ, một đáp án đủ ý về cách cải thiện health factor có thể đạt dù thiếu lời khuyên theo dõi thị trường.
- Hai người điền phiếu riêng trước khi trao đổi. Sau đó thống nhất từng tiêu chí bất đồng và ghi lý do. Đầu ra đạt khi cả ba tiêu chí đạt và quyết định trả lời hoặc từ chối phù hợp với tham chiếu đã xác minh. Timeout và lỗi thực thi tính là thất bại vận hành.
- Phiếu hiệu chuẩn dùng 24 đầu ra dev. Sau khi chấm thử, mỗi người xác nhận rubric bằng trường `rubric_approved`. Nếu rubric cần đổi, cập nhật rubric và xuất lại phiếu trước khi khóa.
