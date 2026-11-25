# Đối chiếu 31 mục chấm mù còn bất đồng

Mở bản đọc chấm mù và tìm theo mã mục. Cả hai người đối chiếu câu trả lời với tham chiếu, SQL và đoạn nguồn, rồi điền 0 hoặc 1 vào từng trường đang trống trong final-adjudication.json. Ghi lý do chung cho từng mục. Các điểm đã thống nhất được giữ từ phiếu gốc.

| Mục | Tiêu chí bất đồng | Phiếu 1 | Phiếu 2 |
|---|---|---:|---:|
| `A0009` | Tính căn cứ | 0 | 1 |
| `A0020` | Tính căn cứ | 0 | 1 |
| `A0030` | Tính căn cứ | 1 | 0 |
| `A0030` | Chất lượng dẫn chứng | 1 | 0 |
| `A0036` | Chất lượng dẫn chứng | 1 | 0 |
| `A0040` | Tính căn cứ | 0 | 1 |
| `A0041` | Tính căn cứ | 1 | 0 |
| `A0041` | Chất lượng dẫn chứng | 1 | 0 |
| `A0044` | Chất lượng dẫn chứng | 1 | 0 |
| `A0045` | Đúng và đủ ý | 1 | 0 |
| `A0047` | Tính căn cứ | 1 | 0 |
| `A0049` | Đúng và đủ ý | 1 | 0 |
| `A0054` | Có từ chối | 1 | 0 |
| `A0063` | Đúng và đủ ý | 1 | 0 |
| `A0074` | Chất lượng dẫn chứng | 1 | 0 |
| `A0076` | Tính căn cứ | 0 | 1 |
| `A0076` | Chất lượng dẫn chứng | 0 | 1 |
| `A0077` | Có từ chối | 1 | 0 |
| `A0079` | Đúng và đủ ý | 1 | 0 |
| `A0084` | Đúng và đủ ý | 0 | 1 |
| `A0087` | Đúng và đủ ý | 1 | 0 |
| `A0087` | Tính căn cứ | 1 | 0 |
| `A0087` | Chất lượng dẫn chứng | 1 | 0 |
| `A0099` | Đúng và đủ ý | 1 | 0 |
| `A0119` | Đúng và đủ ý | 1 | 0 |
| `A0129` | Tính căn cứ | 1 | 0 |
| `A0129` | Chất lượng dẫn chứng | 1 | 0 |
| `A0130` | Tính căn cứ | 1 | 0 |
| `A0133` | Tính căn cứ | 0 | 1 |
| `A0133` | Chất lượng dẫn chứng | 0 | 1 |
| `A0145` | Tính căn cứ | 0 | 1 |
| `A0157` | Đúng và đủ ý | 1 | 0 |
| `A0158` | Tính căn cứ | 0 | 1 |
| `A0193` | Tính căn cứ | 0 | 1 |
| `A0193` | Chất lượng dẫn chứng | 0 | 1 |
| `A0196` | Tính căn cứ | 0 | 1 |
| `A0200` | Tính căn cứ | 0 | 1 |
| `A0226` | Tính căn cứ | 0 | 1 |
| `A0226` | Chất lượng dẫn chứng | 0 | 1 |
| `A0233` | Tính căn cứ | 0 | 1 |
| `A0233` | Chất lượng dẫn chứng | 0 | 1 |

## Ghi chú từ hai phiếu

### A0009

- **Phiếu 1** · Đúng số dư WETH và giới hạn suy luận nhân quả. Phần cảnh báo gán cho câu hỏi yêu cầu chứng minh quan hệ nhân quả, trong khi câu hỏi chỉ yêu cầu đánh giá liệu snapshot có đủ hay không.
- **Phiếu 2** · Số dư tại đúng giờ và cơ chế lãi có bằng chứng. Claim về dữ liệu cần cho việc quy nguyên nhân hoặc các dòng tiền thay thế không gắn mã cho phần giải thích đó. Tham chiếu 3,042,883,324.3152447 USD.

### A0020

- **Phiếu 1** · Đếm 0 sau khi lọc market theo tên giao thức làm mất các sự kiện hợp lệ. COUNT(*) theo đúng tháng 8/2026 cho 158 sự kiện.
- **Phiếu 2** · Báo 0 sau khi lọc market = 'Aave V3 Ethereum', dù tự nêu giới hạn bộ lọc. Tham chiếu đếm đủ 158 sự kiện toàn tháng. SQL sau lọc không trả lời tổng số được hỏi. Tham chiếu 158 count.

### A0030

- **Phiếu 1** · Các phát biểu trả lời được câu hỏi và có căn cứ trong DOC_WITHDRAW_000.
- **Phiếu 2** · Nêu đủ thanh khoản và điều kiện thế chấp. Claim nói phải theo dõi thường xuyên qua Dashboard như điều kiện rút. DOC_WITHDRAW_000 chỉ khuyến nghị theo dõi HF.

### A0036

- **Phiếu 1** · SQL1 khớp đáp án tham chiếu {value: 3042883324.3152447} cho phạm vi được hỏi.
- **Phiếu 2** · Số dư tại đúng giờ và cơ chế lãi có bằng chứng. Claim về dữ liệu cần cho việc quy nguyên nhân hoặc các dòng tiền thay thế không gắn mã cho phần giải thích đó. Tham chiếu 3,042,883,324.3152447 USD.

### A0040

- **Phiếu 1** · Đúng 63 sự kiện và giới hạn suy luận về các vị thế. DOC_LIQ_001 giải thích cơ chế thanh lý nhưng không xác nhận độ bao phủ của bộ dữ liệu đang xét.
- **Phiếu 2** · SQL1 đếm 63 sự kiện và DOC_LIQ_001 giải thích bên thanh lý phải thực hiện giao dịch. DOC_LIQ_001 không chứng minh độ phủ của việc thu thập dữ liệu on-chain. Tham chiếu 63 count.

### A0041

- **Phiếu 1** · SQL1 khớp đáp án tham chiếu {value: 3042883324.3152447} cho phạm vi được hỏi.
- **Phiếu 2** · SQL1 có năm mốc và không tách lãi, giá token, vay mới và trả nợ. Cảnh báo suy diễn quan hệ giữa độ đơn điệu của số dư USD với lãi mà không kiểm soát giá WETH. Tham chiếu 3,042,883,324.3152447 USD.

### A0044

- **Phiếu 1** · SQL1 khớp đáp án tham chiếu {value: 3042883324.3152447} cho phạm vi được hỏi.
- **Phiếu 2** · Số dư tại đúng giờ và cơ chế lãi có bằng chứng. Claim về dữ liệu cần cho việc quy nguyên nhân hoặc các dòng tiền thay thế không gắn mã cho phần giải thích đó. Tham chiếu 3,042,883,324.3152447 USD.

### A0045

- **Phiếu 1** · Giải thích đúng cơ chế chính nhưng gán cả HF = 0,95 vào nhánh 50%. DOC_LIQ_000 đặt điều kiện nhánh đó là HF > 0,95.
- **Phiếu 2** · DOC_LIQ_000 chỉ áp dụng giới hạn 50% khi HF > 0,95 và đủ điều kiện giá trị. Câu trả lời dùng ‘từ 0.95 trở lên’, xếp điểm biên 0,95 vào cả hai nhánh.

### A0047

- **Phiếu 1** · SQL1 và DOC_WITHDRAW_000 hỗ trợ số dư và điều kiện rút. Phát biểu về giới hạn thanh khoản khi rút lại trỏ DOC_BORROW_000, đoạn hướng dẫn vay.
- **Phiếu 2** · SQL1 và DOC_WITHDRAW_000 hỗ trợ số dư cùng các điều kiện rút. DOC_BORROW_000 nói utilization ảnh hưởng lãi suất chứ không xác nhận chiều nhân quả lãi suất làm thay đổi thanh khoản khả dụng. Tham chiếu 3,897,799,627.0425687 USD.

### A0049

- **Phiếu 1** · Tổng của SQL1 đúng 28.132.234,04 USD. Nhận xét về ngày cắt tri thức của mô hình và nguồn availability không được các bằng chứng trong phiếu xác nhận.
- **Phiếu 2** · SQL1 có kết quả cho kỳ yêu cầu. Cảnh báo lại xếp kỳ đó vào tương lai, ngoài phạm vi, hoặc nghi dữ liệu giả lập mà không đưa ra chứng cứ. Tham chiếu 28,132,234.04010158 USD.

### A0054

- **Phiếu 1** · Hệ thống không đưa được tổng USD cho WETH. Kết quả NULL khi lọc market='WETH' không chứng minh tháng đó thiếu sự kiện WETH vì ánh xạ token chưa được xác minh.
- **Phiếu 2** · Trình bày NULL như kết quả cho token và suy ra WETH không có sự kiện từ SUM=NULL của bộ lọc market chưa được xác minh. SQL1 không chứng minh kết luận theo token.

### A0063

- **Phiếu 1** · Hiệu hai quý khớp tham chiếu nhưng SQL1 chỉ trả về quý I. Số trung bình 2.286.878.458,77 USD của quý II không nằm trong kết quả được dẫn.
- **Phiếu 2** · Hiệu USDT trùng tham chiếu nhưng tự mâu thuẫn về quý có dữ liệu. SQL1 chỉ trả quý I, thiếu ô quý II được dùng để tính hiệu. Tham chiếu -1,725,488,668.2893205 USD.

### A0074

- **Phiếu 1** · SQL1 khớp đáp án tham chiếu {value: 1993676848.0321777} cho phạm vi được hỏi.
- **Phiếu 2** · Số dư tại đúng giờ và cơ chế lãi có bằng chứng. Claim về dữ liệu cần cho việc quy nguyên nhân hoặc các dòng tiền thay thế không gắn mã cho phần giải thích đó. Tham chiếu 1,993,676,848.0321777 USD.

### A0076

- **Phiếu 1** · Đáp án về lãi vay đúng. Câu cuối khẳng định chắc chắn vị thế sẽ bị thanh lý khi HF dưới 1, trong khi DOC_LIQ_000 chỉ xác nhận đủ điều kiện thanh lý.
- **Phiếu 2** · DOC_BORROW_000/001 xác nhận lãi tích lũy từ khi vay và lãi suất thay đổi theo mức sử dụng vốn, tham số quản trị.

### A0077

- **Phiếu 1** · Hệ thống không đưa được tổng USD cho WETH. Kết quả NULL khi lọc market='WETH' không chứng minh tháng đó thiếu sự kiện WETH vì ánh xạ token chưa được xác minh.
- **Phiếu 2** · Trình bày NULL như kết quả cho token và suy ra WETH không có sự kiện từ SUM=NULL của bộ lọc market chưa được xác minh. SQL1 không chứng minh kết luận theo token.

### A0079

- **Phiếu 1** · Giải thích đúng cơ chế chính nhưng gán cả HF = 0,95 vào nhánh 50%. DOC_LIQ_000 đặt điều kiện nhánh đó là HF > 0,95.
- **Phiếu 2** · DOC_LIQ_000 chỉ áp dụng giới hạn 50% khi HF > 0,95 và đủ điều kiện giá trị. Câu trả lời dùng ‘từ 0.95 trở lên’, xếp điểm biên 0,95 vào cả hai nhánh.

### A0084

- **Phiếu 1** · Ngưỡng và tỷ lệ trả nợ khớp tài liệu. Thiếu ý bắt buộc rằng HF dưới 1 xác lập điều kiện thanh lý nhưng chưa xác định thời điểm thanh lý thực tế.
- **Phiếu 2** · DOC_LIQ_000/001 giải thích khi HF dưới 1 thì bên thanh lý có thể thực hiện giao dịch, hoàn nợ và nhận thế chấp kèm thưởng.

### A0087

- **Phiếu 1** · DOC_WITHDRAW_000 hỗ trợ điều kiện thanh khoản và yêu cầu duy trì đủ thế chấp khi còn nợ.
- **Phiếu 2** · Tài liệu rút tiền nêu có thể cần trả nợ hoặc bổ sung thế chấp. Cách diễn đạt bắt buộc phải thực hiện một trong hai thao tác đã loại bỏ trường hợp vị thế vốn đủ an toàn để rút.

### A0099

- **Phiếu 1** · SQL1 xác nhận 63 sự kiện và 52 giao dịch. Cảnh báo sai khi đặt tháng 7/2026 sau tháng 9/2026, dù cuối cùng vẫn chấp nhận kết quả.
- **Phiếu 2** · SQL1 có kết quả cho kỳ yêu cầu. Cảnh báo lại xếp kỳ đó vào tương lai, ngoài phạm vi, hoặc nghi dữ liệu giả lập mà không đưa ra chứng cứ. Tham chiếu 52 count.

### A0119

- **Phiếu 1** · Ba ô SQL1 hỗ trợ hiệu −240.373.085,13 USD và hai trung bình quý. Phần cảnh báo viện dẫn metadata về USDe không được cung cấp.
- **Phiếu 2** · Hiệu USDe đúng ngay trong SQL1, nhưng cảnh báo nói chỉ quý II được xác minh dù SQL trả cả hai số trung bình cho hai quý trong phạm vi. Tham chiếu -240,373,085.12855375 USD.

### A0129

- **Phiếu 1** · COUNT(*) bằng 158 còn COUNT(DISTINCT tx_hash) bằng 107. Hai ô SQL1 trực tiếp giải thích vì sao số sự kiện và giao dịch có thể khác nhau.
- **Phiếu 2** · SQL1 chứng minh nhiều sự kiện trong một giao dịch bằng hai phép đếm. SQL1 và các tài liệu không xác định giao dịch xử lý nhiều vị thế, nhiều tài sản hay nhiều sự kiện trong cùng một lần gọi hàm. Tham chiếu 107 count.

### A0130

- **Phiếu 1** · SQL1 xác nhận dư nợ 1.993.676.848,03 USD và DOC_BORROW_001 giải thích lãi vay. Phát biểu riêng về giới hạn suy luận từ một quan sát thiếu trích dẫn.
- **Phiếu 2** · Số dư và kết luận giới hạn nhân quả đúng. Cảnh báo yêu cầu tuyệt đối không có giao dịch vay/trả giữa hai mốc, dù có thể định lượng và loại trừ ảnh hưởng của các dòng tiền. Tham chiếu 1,993,676,848.0321777 USD.

### A0133

- **Phiếu 1** · SQL1 và DOC_WITHDRAW_000 hỗ trợ số dư và điều kiện rút. DOC_BORROW_000 mô tả mức sử dụng ảnh hưởng lãi vay nhưng không chứng minh lãi vay tác động ngược trở lại thanh khoản.
- **Phiếu 2** · Đối chiếu SQL1 với tham chiếu [{"value": 3897799627.0425687}].

### A0145

- **Phiếu 1** · Nêu đúng không thể kết luận số giao dịch USDC vì market chưa được ánh xạ. Phần khẳng định không rõ cấu trúc bảng và viện dẫn repair_feedback không có bằng chứng trong phiếu.
- **Phiếu 2** · Phân biệt số 0 của bộ lọc market với số giao dịch USDC thực tế, từ chối kết luận theo token. Dẫn repair_feedback thay cho chứng cứ về giới hạn ánh xạ.

### A0157

- **Phiếu 1** · Phân biệt rõ 2.196.015.248,98 USD tại giờ cuối của SQL1 với dữ liệu trực tiếp và từ chối khẳng định giá trị hiện tại. Cảnh báo suy đoán dữ liệu thử nghiệm từ dấu thời gian.
- **Phiếu 2** · Đã nói không có giá trị thời gian thực, nhưng giải thích snapshot 15/9/2026 là tương lai hoặc dữ liệu giả lập. Ngày đó đã qua và SQL1 không hỗ trợ nhận định này.

### A0158

- **Phiếu 1** · Dòng 2 của SQL1 hỗ trợ con số USDC và không đủ quy biến động cho lãi vay. Nhận định có bốn lượt truy xuất hay dòng tiền chi phối không được các dòng SQL chứng minh.
- **Phiếu 2** · Số dư tại mốc yêu cầu và kết luận nhân quả đúng. Claim chênh lệch 4.300.049,87 USD trỏ vào ô số dư 1.993.676.848,03 USD thay vì chỉ rõ cặp ô dùng để tính chênh lệch. Tham chiếu 1,993,676,848.0321777 USD.

### A0193

- **Phiếu 1** · Tham chiếu yêu cầu từ chối số ngay bây giờ. Claim gán số lịch sử 15/09 thành ngay bây giờ vượt bằng chứng SQL1, dù phần chính ghi đúng thời điểm lịch sử.
- **Phiếu 2** · SQL1 hỗ trợ số dư và ngày của quan sát cuối 15/9/2026. Câu trả lời đưa số lịch sử ngoài phạm vi thay vì nêu rõ không thể cung cấp dư nợ thời gian thực.

### A0196

- **Phiếu 1** · Đúng số snapshot và hiệu giảm 4.300.049,87 giữa hai hàng 23–24, không quy nguyên nhân cho lãi. Numeric của hiệu lại trỏ ô borrowed_usd hàng 24 thay vì phép trừ; các claim nhân quả thiếu citation và cảnh báo coi truy vấn mở rộng là sai dù đã chọn đúng snapshot.
- **Phiếu 2** · Số dư tại mốc yêu cầu và kết luận nhân quả đúng. Claim chênh lệch 4.300.049,87 USD trỏ vào ô số dư 1.993.676.848,03 USD thay vì chỉ rõ cặp ô dùng để tính chênh lệch. Tham chiếu 1,993,676,848.0321777 USD.

### A0200

- **Phiếu 1** · Số WETH và kết luận không chứng minh nhân quả đúng. Claim bổ sung gọi quan sát mang tiếp dù is_carried=false không được SQL1 hỗ trợ; claim trung tâm về nhân quả để citations rỗng.
- **Phiếu 2** · Số dư tại đúng giờ và cơ chế lãi có bằng chứng. Claim về dữ liệu cần cho việc quy nguyên nhân hoặc các dòng tiền thay thế không gắn mã cho phần giải thích đó. Tham chiếu 3,042,883,324.3152447 USD.

### A0226

- **Phiếu 1** · Tháng 02/2026 và 2.647 giao dịch đúng. Claim thêm ngày 29/02/2026 không tồn tại và không được SQL1 xác nhận, nên tính căn cứ và dẫn chứng không đạt.
- **Phiếu 2** · Đối chiếu SQL1 với tham chiếu [{"month": "2026-02", "value": 2647}].

### A0233

- **Phiếu 1** · Đúng số USDC và thanh khoản nhưng chưa nêu cần còn đủ thế chấp sau rút hay trả nợ/thêm thế chấp. Claim HF<1 cho phép thanh lý tối đa 100% bỏ điều kiện HF≤0,95 hoặc giá trị dưới 2.000, trái DOC_LIQ_000/001.
- **Phiếu 2** · Số dư USDC, thanh khoản và HF được SQL1 cùng DOC_WITHDRAW_000/DOC_LIQ_000 hỗ trợ. Thiếu ý có thể cần trả bớt nợ hoặc bổ sung thế chấp trước khi rút. Tham chiếu 1,997,694,271.598428 USD.

