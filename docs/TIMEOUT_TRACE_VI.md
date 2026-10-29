# Trace timeout Qwen và lỗi Claude trên UI so sánh

Ngày: 28/10/2026. Kiểm tra từ ảnh người dùng, log llama.cpp hiện tại `.tmp/qwen-server-error.log`, code deadline và cấu hình credentials cục bộ. Không gọi lại Bedrock, không in secret, không tăng deadline hoặc chạy lại inference để tìm kết quả đạt.

## Kết luận

Hai lỗi độc lập:

- Qwen chạm **deadline chung 120 giây cho toàn bộ câu hỏi**, không phải mỗi request có 120 giây riêng. Giới hạn ở Analyst (pipeline.py), comparison.py khởi tạo cùng deadline cho hai model; LocalQwenLLM nhận thời gian còn lại. Đoạn log khớp ảnh cho thấy các task 150, 205 hoàn tất rồi task 230 bị cancel khi deadline hết.
- Claude không tìm thấy AWS credentials. Không có env/.env trong project; các biến AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_SESSION_TOKEN, AWS_PROFILE không được đặt trong tiến trình kiểm tra; boto3 provider chain trả không có credentials. Chưa đi đến inference, nên đây không phải timeout hoặc kết quả so sánh chất lượng model.

## Phân rã từ log llama.cpp

| Task server | Đọc prompt | Sinh output | Tổng |
| --- | ---: | ---: | ---: |
| 150 | 3.527 token xử lý / 41,113 giây | 48 token / 1,503 giây | 42,616 giây |
| 205 | 3.745 token xử lý / 43,743 giây | 17 token / 0,503 giây | 44,246 giây |
| 230 | tiếp tục đọc prompt; đến 2.560 token đã mất 27,83 giây | chưa có thống kê hoàn tất | bị cancel sau khoảng 32,89 giây |

Task 150 bắt đầu tại 15:21,029 tính từ lúc server chạy; task 230 bị cancel tại 17:21,153: tổng khoảng 120,12 giây, phù hợp ảnh 120,0 giây. Riêng hai task đầu đọc prompt mất **84,856 giây**, chiếm khoảng 97,7% thời gian model của hai request. Tổng output 48+17=65 token khớp ảnh. Số token input native được xử lý không nhất thiết bằng usage API do cache/prefix reuse.

Không có log CUDA/Vulkan out-of-memory hoặc crash trong đoạn này. Server nhận tác vụ, trả được hai request và hủy request thứ ba sau client timeout. Đây là bottleneck prefill/prompt dài và deadline nhiều bước; không có bằng chứng network mất kết nối là nguyên nhân gốc.

Log native hiện tại không ghi role (plan/answer/review). Không gán role chắc chắn cho task chỉ dựa trên số thứ tự. Bản smoke trước đã lưu trong local-qwen-pipeline-smoke.json cho thấy plan + answer dùng gần hết 120 giây rồi claim_review timeout; planning sai kind=docs cho câu hỏi số liệu, không sinh SQL, answer thành "0". Ảnh hiện tại cũng có "0" và không có SQL, nhưng muốn kết luận routing của chính lượt đó phải đọc JSON/trace phiên tương ứng. Một câu "0" không được xem là số liệu đã xác minh.

## Đã thêm để trace được các lượt sau

- Ghi timeout_seconds còn lại và độ dài prompt vào trace adapter local; ghi timing server nếu endpoint trả về. Bedrock cũng ghi ngân sách lúc gọi.
- UI so sánh có mục **Trace từng bước model**: role, lần thử, elapsed, ngân sách còn lại, input/output token và lỗi. Không tự gọi lại model khi xem.
- Kết quả so sánh mới tự lưu vào **runs/comparisons/<id>.json**, có cấu hình, calls, input/code hashes và cả hai kết quả. Thư mục runs đã gitignore. Bản cũ chỉ có trong session/download JSON, không được giả mạo thành log mới.
- Token bằng 0 ở request timeout có thể là chưa nhận được usage từ server, không phải request không sử dụng tài nguyên.

## Hướng xử lý tiếp theo

Không chỉ tăng timeout rồi coi model đúng: cần giảm prompt/tài liệu không liên quan, và xử lý việc model chuyên Text-to-SQL chưa theo tốt schema planning/answer/review. Nếu thêm timeout cho tương tác phải áp dụng cùng ngân sách cho cả hai model và ghi rõ, tách khỏi benchmark 120 giây. Chưa thay prompt, đổi model, bỏ kiểm chứng hoặc thay protocol trong lượt trace này.

Claude: cấu hình credentials trong env/.env hoặc AWS profile theo README và khởi động lại app nếu cần; chưa có bằng chứng credentials/quyền Bedrock hợp lệ. Không đưa credentials vào chat, báo cáo hoặc Git. Chạy doctor không --live để kiểm tra có credentials; chỉ kiểm tra quyền model bằng inference khi người dùng chủ động chạy.


## Điều chỉnh theo yêu cầu tiếp theo của người dùng

Đã tăng mặc định tương tác UI từ 120 lên **600 giây mỗi model**; sidebar cho điều chỉnh 120–3600 giây. Cùng mức áp dụng cho hai bên so sánh và được lưu trong JSON; hội thoại cũng nhận mức này. Analyst/CLI/benchmark mặc định vẫn 120 giây, không thay protocol thí nghiệm. Không tự gọi lại model hoặc Bedrock khi đổi timeout. Mức cao hơn giảm lỗi deadline, không bảo đảm mọi câu hoàn tất và không giải quyết sai routing hoặc credentials.
