# Bàn giao xác minh độc lập trước final

Hiện bộ đáp án có 60 câu nháp, chưa có phê duyệt của người. Stress SQL có 20 ca nháp, cũng chưa được duyệt. Không chạy final hoặc dùng điểm dev làm kết quả nghiên cứu cuối.

## Hai người cần làm ngay

Mỗi người chỉ nhận bộ của mình, tự kiểm tra trước khi trao đổi bất đồng:

| Người | Benchmark | Stress SQL |
|---|---|---|
| 1 | data/benchmark/review/questions-v2/reviewer-1.md và .json | data/benchmark/review/stress-v1/reviewer-1.md và .json |
| 2 | data/benchmark/review/questions-v2/reviewer-2.md và .json | data/benchmark/review/stress-v1/reviewer-2.md và .json |

Booklet có câu hỏi, nguồn, SQL và đáp án máy tạo. Người review phải kiểm tra độc lập bằng nguồn/SQL, không chỉ đọc và đồng ý với lời giải. Ghi tên thật trong reviewer_name. Mỗi item điền verdict, verified_answer, verified_sources, verified_scope và notes. Dùng changes_requested khi sai hoặc chưa rõ; không đánh dấu approved trước khi kiểm tra lại bản sửa. Không dùng questions-v1 vì đó là lịch sử trước bổ sung scope.

Yêu cầu trực tiếp trong đề xuất: “Hai thành viên kiểm tra độc lập đáp án bằng tài liệu và SQL/mã tính, sau đó thống nhất các bất đồng.” Đây là công việc xác minh người, không phải một bước assistant có thể thay bằng tên giả hoặc nhãn máy.

Khi cả hai hoàn tất, nhập hai bộ riêng:

```powershell
.\.venv\Scripts\python.exe -m aave_analyst.cli review-import data/benchmark/questions.jsonl data/benchmark/review/questions-v2/reviewer-1.json data/benchmark/review/questions-v2/reviewer-2.json
.\.venv\Scripts\python.exe -m aave_analyst.cli review-import data/benchmark/stress.jsonl data/benchmark/review/stress-v1/reviewer-1.json data/benchmark/review/stress-v1/reviewer-2.json
```

Nếu có bất đồng, giữ lịch sử, sửa nội dung và xuất bộ review mới; mọi người kiểm tra lại bản đã sửa. Công cụ kiểm tra hash để tránh dùng quyết định cho bản cũ. Chỉ sau khi hoàn thiện dev và review mới freeze rồi chạy 720 đầu ra. Quy trình đầy đủ ở REPRODUCE_PROPOSAL_VI.md.

## Sau khi có đầu ra final

Hai người tiếp tục audit độc lập mẫu judge qua audit-export/audit-import; phiếu không hiện nhãn judge hay tên cấu hình. Điểm và Cohen kappa được tính từ nhãn thật. Đo truy vết theo 10 câu đăng ký, ghi giây thực. Stress final cần hai nhãn final_correct để đếm sửa đúng/làm sai; trạng thái checks_passed không phải gold.
