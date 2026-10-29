# Báo cáo giai đoạn 1–2 — Aave / Qwen

Ngày thực hiện: **28/10/2026, Asia/Saigon**. Project: `C:\BlockchainProject`. Commit nền: `0917465821b2746e2ef1a6ad57f8f1f79cee2174`. Git sạch trước công việc; không tìm thấy AGENTS.md tại root project hoặc thư mục cha đã kiểm tra. Không sửa runtime hiện có; thêm hai script thu thập/audit và báo cáo. Chưa commit.

## Kết quả và phần chưa giải quyết

Đã dựng `.venv`, cài nguyên requirements-lock.txt, cài project editable, tải đúng snapshot pin, tạo Parquet/DuckDB/audit/dictionary, thu thập lại tài liệu Aave, hash các artifact và chạy **93 test đạt trong 14,44 giây**. Đây là kết quả mới trên máy này, không lấy từ docs/verification.json cũ.

Repo GGUF tồn tại và đọc được metadata. **Chưa xác minh được checkpoint Transformers thực sự sinh ra artifact text-to-SQL**, revision checkpoint đó, tokenizer tương ứng đầy đủ, dữ liệu fine-tune và quyền sử dụng phần fine-tune. Vì vậy chưa đủ điều kiện bắt đầu train hoặc khẳng định so sánh trước/sau fine-tune là cùng một checkpoint. Không thay artifact bằng model khác.

Trong giai đoạn 1–2 ban đầu: không tạo bộ train/test/benchmark mới, không fine-tune, chưa tải đầy đủ trọng số, không gọi paid Bedrock inference hay final benchmark. Sau yêu cầu dùng model của người dùng, đã tải đầy đủ GGUF và thử inference local như mục 10–11. Goal chuyển sang blocked sau ba lượt cùng thiếu nguồn checkpoint; kết quả điều tra và phần dữ liệu độc lập đã được lưu. Chưa đánh dấu hoàn thành.

## 1. Provenance model

Nguồn chính: [Hub API](https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF), [cây file tại revision pin](https://huggingface.co/api/models/zhenlong54/qwen-vitext2sql-3b-GGUF/tree/579ae3d2f0db23dd25fd83076a57dbab79f68dd9?recursive=true). Các phản hồi được lưu trong `phase12-evidence/hf_*.json` kèm URL và thời điểm thu thập.

| Thuộc tính | Bằng chứng |
| --- | --- |
| Repo | zhenlong54/qwen-vitext2sql-3b-GGUF; public, không gated/disabled |
| Revision | `579ae3d2f0db23dd25fd83076a57dbab79f68dd9` |
| File | `model-q4_k_m.gguf`, 1.929.902.496 byte |
| LFS SHA-256 do Hub công bố | `b34a028bc6c18d738b57552423bb75ca555d823c19722c4261acc792547a4cd2` — chưa kiểm tra hash toàn file vì không tải trọng số |
| Model card / license | Cây file chỉ có .gitattributes và GGUF; README tại revision trả 404, không có license riêng |
| GGUF | phiên bản 3; 434 tensors; 27 metadata entries; Hub báo 3.085.938.688 parameters |
| Tên nội bộ | Qwen2.5 Coder 3B Instruct; architecture qwen2; 36 layers; hidden 2048; context 32768 |
| Tokenizer nhúng | gpt2/qwen2; 151.936 tokens; 151.387 merges; BOS 151643, EOS/pad 151645 |

Đã đọc đúng **8 MiB** đầu file bằng HTTP Range (206); metadata kết thúc tại byte 5.931.230. Chỉ lưu bản tóm tắt metadata, không lưu mảng token/merges hoặc tensor weights. Điều này xác minh cấu trúc và tên khai báo, không xác minh lịch sử huấn luyện hay nội dung weights. Search API theo author + qwen chỉ trả repo này; không tìm được nguồn text-to-SQL công khai tương ứng qua các bước đã thực hiện. Không suy luận repo không tồn tại từ lỗi đọc trang hoặc README 404.

### Ứng viên đối chiếu, không phải checkpoint thay thế

[Qwen/Qwen2.5-Coder-3B-Instruct](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct) tại revision `488639f1ff808d1d3d0ba301aef8c11461451ec5` có Transformers/safetensors và file tokenizer. Config phù hợp các kích thước GGUF: qwen2, 36 layers, hidden 2048, intermediate 11008, 16 attention heads/2 KV heads, vocab 151936, BOS/EOS phù hợp. Config/tokenizer_config/card/LICENSE đã được tải ở revision pin để đối chiếu, không tải tokenizer.json hay weights đầy đủ.

Đây chỉ là **ứng viên backbone suy ra từ metadata**. Tên GGUF có thể giữ nguyên sau fine-tune; cấu hình trùng không chứng minh weights hoặc tokenizer hoàn toàn giống. Không có đường dẫn base_model, source revision, adapter, conversion log, training recipe hay dataset card trong repo GGUF để nối chuỗi provenance. Chữ “vitext2sql” không đủ để khẳng định đã dùng dataset ViText2SQL nào.

### Điều kiện giấy phép

[LICENSE của ứng viên Qwen tại revision pin](https://huggingface.co/Qwen/Qwen2.5-Coder-3B-Instruct/blob/488639f1ff808d1d3d0ba301aef8c11461451ec5/LICENSE) là **Qwen Research License**, không phải Apache 2.0. Văn bản cho phép dùng và sửa đổi cho nghiên cứu/đánh giá phi thương mại; sử dụng thương mại phải xin giấy phép riêng. Phân phối có yêu cầu kèm license, ghi sửa đổi/attribution, và tài liệu cho model được phân phối có nghĩa vụ ghi nhận Qwen. Điều khoản này chỉ là nguồn của ứng viên backbone; không tự giải quyết quyền với phần fine-tune hay dataset của bên upload GGUF.

Cần tác giả cung cấp: checkpoint Transformers hoặc merged/adapter weights + revision; nguồn backbone; tokenizer và chat template pin; recipe chuyển GGUF; danh sách dataset và license; điều kiện sử dụng/phân phối artifact. Chưa liên hệ tác giả hoặc gửi thông điệp ra ngoài.

## 2. Phần cứng và khả năng train

Bằng chứng cục bộ: cpu.json, ram.json, os.json, disk.json, gpu.csv trong thư mục evidence.

- CPU Intel Core i5-12400F; RAM 16.984.072.192 byte (~15,82 GiB).
- NVIDIA GTX 1650, 4096 MiB VRAM, compute capability 7.5, driver 616.64, WDDM. Khi đo dùng khoảng 1,3–1,4 GiB VRAM cho desktop; bộ nhớ khả dụng biến động.
- Ổ C: trước cài có ~12,68 GiB trống; disk.json ghi lại sau chuẩn bị. Không tải weights nhiều GB vào dung lượng ít còn lại.
- Python hệ thống 3.13.5 là interpreter duy nhất thấy qua py launcher. `.venv` dùng cùng phiên bản; không thay Python hệ thống.
- `nvidia-smi` hiển thị CUDA UMD 13.4 là thông tin driver; không chứng minh đã có CUDA Toolkit, PyTorch CUDA hoặc training stack hoạt động. Chưa cài torch/transformers/peft/bitsandbytes, không cài CUDA/driver.

**Đánh giá kỹ thuật:** GTX 1650 không bị loại chỉ vì compute capability: [bitsandbytes](https://huggingface.co/docs/bitsandbytes/main/en/installation) liệt kê NF4/FP4 yêu cầu CC >=6.0. Tuy nhiên 4 GiB VRAM đang dùng cho desktop không phải môi trường train 3B đáng tin cậy. Chỉ weights 3,086B ở FP16 đã khoảng 5,75 GiB; 4-bit lý tưởng khoảng 1,44 GiB còn chưa tính lớp không lượng tử, metadata, activation, gradient, adapter và optimizer. Chưa chạy thử train nên không khẳng định tuyệt đối không thể với mọi cấu hình/offload.

Đề xuất cho giai đoạn sau: máy Linux x86-64 với GPU NVIDIA **16–24 GiB VRAM**, RAM 32 GiB và SSD trống ít nhất 40–60 GiB, Python 3.11/3.12 trong môi trường train riêng. Đây là mức dự trù kỹ thuật để có dư địa, không phải mức tối thiểu đã đo. Pin bộ PyTorch/CUDA wheel/Transformers/PEFT/bitsandbytes tương thích, chạy kiểm tra GPU rồi smoke test một batch ngắn để đo peak VRAM trước khi xác nhận cấu hình.

[PEFT quantization guide](https://huggingface.co/docs/peft/developer_guides/quantization) mô tả 4-bit NF4 và LoRA adapter qua prepare_model_for_kbit_training; hướng dự kiến là QLoRA trên checkpoint Transformers đã xác minh, rồi chuyển sang cùng cấu hình GGUF khi cần đánh giá. Không coi GGUF Q4_K_M là checkpoint huấn luyện full precision. [Transformers GGUF](https://huggingface.co/docs/transformers/quantization/gguf) có cơ chế load/dequantize, nhưng khôi phục từ lượng tử không tái tạo chính xác weights gốc và không giải quyết provenance/license.

## 3. Môi trường đã dựng

Cài nguyên 50 package pin trong requirements-lock.txt thành công; `pip check`: No broken requirements found. Các phiên bản chính: Python 3.13.5, DuckDB 1.5.6, pandas 3.0.6, pyarrow 26.0.0, Streamlit 1.66.0, sqlglot 30.23.0, boto3 1.43.114, pytest 9.1.1. Danh sách thực tế nằm trong environment-freeze.txt. Project editable 0.1.0 trỏ tới workspace hiện tại.

93 test hiện có dùng dữ liệu/LLM giả lập, botocore Stubber và cấu hình test. Không gọi ask/run/stress/score --judge/doctor --live. Pytest XML và stdout mới nằm trong pytest.xml, pytest-output.txt. Các test này kiểm tra runtime offline, không chứng minh chất lượng Qwen hoặc Claude.

## 4. Snapshot, quyền sử dụng dữ liệu và hash

Dùng đúng [release data-2026-09-15](https://github.com/MSCA-DN-Digital-Finance/stablecoin-onchain-data/releases/tag/data-2026-09-15), asset aave_data.zip 34.902.111 byte. Không dùng latest.

SHA-256 tải về bằng digest GitHub công bố: `1d4d8025b5aed07707d341b5824b6954d9869b8416e11efa2832ceafeaedf91e`.

[Repository nguồn](https://github.com/MSCA-DN-Digital-Finance/stablecoin-onchain-data) mô tả dữ liệu Ethereum từ subgraph. GitHub API trả license=null; cây main tại thời điểm kiểm tra không có LICENSE; README và release body không chỉ ra quyền fine-tune/phân phối. Chưa xác minh điều khoản của tất cả nguồn subgraph hoặc nguồn lưu trữ khác. Tải công khai để audit cục bộ không được coi là giấy phép huấn luyện hoặc tái phân phối. Không công bố lại dữ liệu.

Artifact cục bộ: data/raw/aave_data.zip, data/raw/manifest.json, dữ liệu giải nén; data/processed/{market_hourly.parquet,liquidation_events.parquet,aave.duckdb,audit.json,dictionary.json}; data/documents/{SUPPLY.html,BORROW.html,LIQ.html,chunks.json}. Hash manifest bao phủ mọi file trong ba thư mục dữ liệu đó; báo cáo audit độc lập đọc từ database, không chỉ tin output prepare. Database có bảng market_hourly, liquidation_events, coverage; giờ được lưu TIMESTAMPTZ và truy vấn ở UTC.

## 5. Audit mới trên database

| Asset | Số dòng | Bắt đầu UTC | Kết thúc UTC | Giờ carried | Tuổi quan sát lớn nhất (giờ) |
| --- | ---: | --- | --- | ---: | ---: |
| DAI | 31.847 | 2023-01-27 08:00 | 2026-09-15 06:00 | 7.923 | 17,2903 |
| USDC | 31.848 | 2023-01-27 08:00 | 2026-09-15 07:00 | 515 | 5,2369 |
| USDT | 31.434 | 2023-02-13 14:00 | 2026-09-15 07:00 | 1.554 | 12,6836 |
| USDe | 19.937 | 2024-06-06 15:00 | 2026-09-15 07:00 | 5.057 | 26,1769 |
| WETH | 31.848 | 2023-01-27 08:00 | 2026-09-15 07:00 | 243 | 3,0636 |

Tổng **146.914** dòng. Mỗi asset: khóa (asset,hour) không trùng, không thiếu giờ giữa min/max, không lệch đầu giờ UTC; supplied_usd/borrowed_usd/source_timestamp không null; không source timestamp từ tương lai. Tất cả cột market chuẩn hóa không null theo audit prepare.

Có tổng **15.292 giờ carried**: is_carried khớp việc source_timestamp đã xuất hiện trước đó trong cùng asset, kiểm tra lại bằng window SQL có 0 mismatch. Lưới giờ liên tục không đồng nghĩa có quan sát on-chain mới mỗi giờ hoặc dữ liệu phản ánh trạng thái thực tế hoàn hảo. Chưa xác minh độ đúng số dư với node/subgraph độc lập.

Thanh lý: **25.121 events / 20.159 distinct tx**; 0 trùng event_id hoặc (tx_hash,log_index); time, amount_usd, log_index không null; event_id/tx_hash không rỗng hoặc chuỗi nan/None. Khoảng quan sát: 2023-01-30 19:11:47 đến 2026-09-15 05:53:59 UTC. Không suy ra sự vắng mặt sự kiện là mất dữ liệu hay hoạt động bằng không ngoài phạm vi nguồn. Chưa xác minh mapping market -> token collateral/debt; profitUSD, gas, APR và lọc thanh lý theo token vẫn loại khỏi phân tích.

Trong cửa sổ đánh giá `[2025-01-01,2026-09-01)` UTC: mỗi asset 14.592 giờ, 0 thiếu; 19.586 events thuộc 15.345 transactions. **Runtime giữ toàn bộ lịch sử**, không cắt theo cửa sổ đánh giá. Không tạo câu hỏi đánh giá mới.

## 6. Lệnh tái lập

Chạy từ PowerShell tại C:\BlockchainProject:

```powershell
python -m venv .venv  # chỉ khi môi trường chưa tồn tại
.\.venv\Scripts\python.exe -m pip install -r requirements-lock.txt
.\.venv\Scripts\python.exe -m pip install --no-deps -e .
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe scripts/collect_phase12_provenance.py
.\.venv\Scripts\python.exe -m aave_analyst.cli prepare
.\.venv\Scripts\python.exe -m aave_analyst.cli documents
.\.venv\Scripts\python.exe scripts/audit_phase12.py
.\.venv\Scripts\python.exe -m pytest --junitxml=docs/phase12-evidence/pytest.xml
```

Script provenance truy vấn metadata hiện tại rồi pin revision cho file model; lưu phản hồi mới nên có thể khác snapshot báo cáo nếu upstream thay đổi. Khi tái lập đúng bản này, dùng revision/hash ghi ở trên và kiểm tra digest. prepare tái dùng archive nếu đã tồn tại; audit_phase12.py xác minh lại digest với release API đã lưu. documents thu thập nội dung web hiện tại nên hash/ngày/chunks có thể đổi; dùng manifest đã lưu để đối chiếu bản chạy này. DuckDB có thể khác byte-level sau rebuild dù dữ liệu logic bằng nhau; kiểm tra SQL audit cùng hash input.

.venv, data/raw, data/processed, data/documents, .tmp và credentials đã được .gitignore loại trừ. Chỉ báo cáo, metadata, hash và script là thay đổi review được; không stage/commit dữ liệu hoặc credentials. Muốn bước sang train cần giải quyết provenance checkpoint và quyền dữ liệu/model trước, sau đó mới chốt môi trường train và protocol so sánh.


## 7. Kiểm tra bổ sung lịch sử công khai

Lượt tiếp tục ngày 28/10/2026 đã kiểm tra thêm Hub API và lưu phản hồi có thời điểm thu thập:

- `hf_commits.json`: chỉ có hai commit: initial `5d2a9cdb68b731ad877b6d6ceb027f1bb1c99c36` và upload GGUF `579ae3d2f0db23dd25fd83076a57dbab79f68dd9`. Commit messages không dẫn nguồn checkpoint.
- `hf_initial_tree.json`: commit đầu chỉ có .gitattributes, nên không có README/license/checkpoint nguồn từng xuất hiện rồi bị xóa trong lịch sử hai commit này.
- `hf_discussions.json`: không có thảo luận công khai để truy nguồn.
- `hf_author_models.json`, `hf_author_spaces.json`, `hf_author_datasets.json`: API công khai của tác giả chỉ liệt kê repo GGUF này, không có space/dataset công khai.
- `hf_global_search.json`: truy vấn vitext2sql trả 6 model, gồm một adapter Qwen **7B** của tác giả khác. Không có bằng chứng liên kết adapter đó với GGUF **3B**, nên không sử dụng làm nguồn thay thế.

Bằng chứng mới thu hẹp các đường tìm kiếm nhưng vẫn không xác minh được checkpoint huấn luyện nguồn. Không thể suy ra nội dung private/unlisted từ kết quả API công khai. Đã yêu cầu người dùng cung cấp link checkpoint hoặc notebook nếu có; không liên hệ bên thứ ba. Lượt trước được phân loại là có tiến triển (dựng môi trường/dữ liệu/audit); lượt này có tiến triển bằng chứng qua lịch sử repo, chưa đủ điều kiện goal complete.


## 8. Completion audit và trạng thái goal

Lần đối chiếu cuối xác nhận revision repo vẫn là `579ae3d2f0db23dd25fd83076a57dbab79f68dd9`, chỉ có .gitattributes + GGUF và không có model card. Kiểm tra lại SHA-256 của **24/24 file** trong hash manifest không có sai khác. Kết quả pytest 93 test và các artifact dữ liệu vẫn hiện diện.

Completion audit chi tiết nằm tại `phase12-evidence/goal_completion_audit.json`. Môi trường, phần cứng, snapshot, database, audit, kiểm thử offline và báo cáo tái lập đã có bằng chứng. Nguồn checkpoint Transformers thực sự, tokenizer/revision tương ứng và quyền với phần fine-tune còn chưa xác minh. Cùng điều kiện thiếu nguồn đã tồn tại trong ba lượt goal liên tiếp; không còn bước độc lập có thể chứng minh phần này bằng nguồn công khai đã tìm thấy. Goal **blocked**, không complete. Tiếp tục được khi có link checkpoint/adapter/notebook hoặc provenance từ tác giả; chưa gửi thông điệp cho tác giả.


## 9. Link Colab do người dùng cung cấp

Đã giải mã tham số fileId và tải trực tiếp [notebook Hugging Face](https://huggingface.co/zhenlong54/qwen-vitext2sql-3b-GGUF.ipynb), HTTP 200, nội dung JSON nbformat 4. Đây là endpoint notebook truy cập được dù cây file repo không có file .ipynb; lỗi đọc trang qua công cụ web không được dùng để kết luận notebook không tồn tại.

Đã đọc toàn bộ 4 cell: cài llama-cpp-python; phần mô tả Local Inference on GPU; Llama.from_pretrained trỏ repo GGUF hiện tại với filename model-q4_k_m.gguf; gọi create_chat_completion với chuỗi placeholder chưa có input example. Nội dung tự ghi là generated snippets và trỏ tới huggingface.js. Metadata chọn GPU T4 chỉ là cấu hình notebook, không phải bằng chứng tác giả đã huấn luyện trên T4.

Notebook này là ví dụ inference GGUF, không có AutoModelForCausalLM/checkpoint Transformers, adapter LoRA, tokenizer nguồn/revision, bước huấn luyện, dataset hoặc license. Vì vậy link mới chưa giải quyết blocker provenance; không chạy notebook, không cài llama-cpp-python, không tải weights. Phản hồi đầy đủ nằm tại provided_notebook_url.json; phân tích và SHA-256 nội dung nằm tại provided_notebook_assessment.json trong thư mục evidence. Cần notebook **huấn luyện/xuất GGUF** hoặc checkpoint/adapter nguồn để tiếp tục xác minh.


## 10. Quyết định sử dụng model của người dùng

Người dùng xác nhận model đã được developer khác fine-tune và yêu cầu dùng đúng artifact này. Chấp nhận **zhenlong54/qwen-vitext2sql-3b-GGUF**, revision `579ae3d2f0db23dd25fd83076a57dbab79f68dd9` làm model inference được chọn; không thay bằng Qwen backbone khác. Trạng thái đã fine-tune là thông tin người dùng cung cấp, chưa được độc lập xác minh. Thiếu checkpoint Transformers không cản dùng GGUF để inference cục bộ; hạn chế này chỉ còn liên quan tới tái lập fine-tune và huấn luyện tiếp.

Đã thêm adapter llama.cpp local, lựa chọn AAVE_LLM_PROVIDER=local_qwen cho CLI/giao diện, script tải model pin kèm xác minh SHA-256, runtime llama.cpp b11962 Vulkan và script khởi động loopback (cấu hình cuối: offload tất cả layers, batch 512, micro-batch 128, context 8192). Không cài CUDA/driver. Không gửi dữ liệu sang API bên ngoài qua adapter này. File model/runtime được gitignore. Bộ kiểm thử sau thay đổi: **101 passed** (pytest-local-qwen.xml); chưa coi đây là kết quả chạy model thật. Kết quả tải model và smoke inference sẽ được ghi riêng sau khi xác minh.


## 11. Kết quả chạy đúng GGUF người dùng chọn

Đã tải đầy đủ 1.929.902.496 byte và xác minh SHA-256 **b34a028bc6c18d738b57552423bb75ca555d823c19722c4261acc792547a4cd2**, bằng LFS digest Hub. Runtime Vulkan b11962 khớp SHA-256 **53341fccc5d29a0e63e5e7d207cb7fc0f28a1830ae5eb73d1825dda6ab3b0ff4**. Không thay model. Manifest tải ở models/qwen-vitext2sql-3b/manifest.json (ignored); bản metadata sao chép vào evidence/local-qwen-artifact.json.

Server loopback đã nạp được model trên GTX 1650, /health trả ok và /v1/models có đúng alias. Cấu hình cuối: GPU layers 99 (toàn bộ số layers có sẵn), batch 512, micro-batch 128, context 8192, một slot; GPU memory dùng khoảng 3,6 GiB trong lần đo, gồm cả phần desktop. Các giá trị thay đổi theo ứng dụng khác đang chạy.

Các kiểm tra thực tế dưới đây là smoke checks, **không phải benchmark**, không tạo train/test mới:

1. Sinh SQL trực tiếp, cấu hình đầu 20 layers: hỏi số giao dịch thanh lý tháng 8/2026. Model sinh COUNT(DISTINCT tx_hash) với khoảng UTC [2026-08-01,2026-09-01), chạy được và trả **107**, bằng truy vấn độc lập. 968 input / 67 output tokens, khoảng **41,60 giây**. Xem local-qwen-smoke-20layers.json.
2. Sau khi tăng offload và giảm batch để giảm độ trễ, cùng câu/prompt sinh SQL khác có lỗi: double-quote giá trị ngày khiến DuckDB hiểu là tên cột, đồng thời COUNT(*) không đúng ý nghĩa giao dịch. Xem local-qwen-smoke-fullgpu-failure.json. Lần này không lưu được response đầy đủ do script ban đầu dừng ở lỗi query; đã lưu phần lỗi từ traceback và sửa script để từ nay lưu riêng mọi lần thành công/thất bại, không ghi đè kết quả đạt cũ. Không được quy lỗi này cho GPU chỉ từ hai mẫu không deterministic (temperature 0.2).
3. Luồng đầy đủ chế độ P, cùng câu hỏi, dùng Qwen cho tất cả vai trò, không fallback cloud: **error / TimeoutError ở 120,01 giây**. Planning ra kind=docs, không có dates dù câu hỏi yêu cầu số liệu theo tháng; không sinh SQL. Sau bước answer, đến claim_review thì hết ngân sách. Xem local-qwen-pipeline-smoke.json. Do đó chưa xác nhận model thay Claude thành công cho toàn bộ vai trò hoặc chat chạy ổn định; không chỉ tăng timeout rồi coi lỗi ý nghĩa đã được giải quyết.

Kết luận thực tế: **đã dùng đúng artifact và chạy inference local được**; có một SQL check đúng và cũng có lỗi quan sát được. Việc model đã fine-tune Text-to-SQL không tự chứng minh khả năng planning, trả lời có citations và review theo schema của app. Giữ model này theo lựa chọn người dùng; chất lượng Aave và các vai trò cần được xử lý/đánh giá ở giai đoạn sau, chưa fine-tune tiếp. Tính năng local trong giao diện là lựa chọn thử nghiệm, không coi đã đủ chất lượng vận hành.

Chạy `powershell -ExecutionPolicy Bypass -File .\run-qwen.ps1 app` để chọn local rõ ràng; `run-qwen.ps1 doctor` kiểm tra server/config không chạy inference. Không cần gọi Bedrock để dùng đường local. Không thay đổi deadline benchmark 120 giây hoặc protocol đánh giá. Server đang chạy nền; PID lưu trong .tmp/qwen-server.pid.


## 12. Tiếp tục goal ngày 29/10/2026

Đã audit lại snapshot và hash, chạy lại toàn bộ test offline: **124 passed**. Dữ liệu vẫn 146.914 market rows, 25.121 liquidation events; digest archive khớp upstream. Không tạo tập train/test hay fine-tune. Đã dùng đúng GGUF để kiểm tra SQL sau sửa routing/quote ngày: truy vấn thực thi trả 107, khớp kiểm tra độc lập, luồng P 150,74 giây, unverified. Xem QWEN_SQL_ROUTING_FIX_VI.md và qwen-routing-fix-summary.json; đây không phải benchmark.

Hub API kiểm tra lại vẫn cùng revision và chỉ có .gitattributes/model-q4_k_m.gguf. Checkpoint Transformers trước lượng tử hóa và dataset fine-tune của tác giả vẫn chưa xác minh độc lập; không giả định backbone candidate là checkpoint đó.

### Đường fine-tune từ chính GGUF, không thay model

Tài liệu chính thức versioned của Transformers **v4.53.2** ghi hỗ trợ tải GGUF để training/fine-tuning sau **dequantize sang FP32**, liệt kê Qwen2 trong kiến trúc hỗ trợ và có API AutoTokenizer/AutoModelForCausalLM.from_pretrained(..., gguf_file=...). Nguồn pin: https://github.com/huggingface/transformers/blob/v4.53.2/docs/source/en/gguf.md ; phản hồi được lưu ở phase12-evidence/gguf-training-doc.json. Đây là bằng chứng về khả năng framework, **chưa kiểm tra convert thành công artifact này trên máy**; main hiện tại có hành vi load packed khác nên phải pin/test đúng version thay vì dùng hướng dẫn lẫn phiên bản.

Vì vậy, thiếu checkpoint nguyên bản không đồng nghĩa tuyệt đối không thể fine-tune tiếp bản người dùng chọn. Có đường khả thi có điều kiện: GGUF đã pin -> dequantize thành checkpoint/tokenizer Transformers dẫn xuất -> kiểm tra tokenizer/chat-template và parity inference -> LoRA/QLoRA trên dataset Aave được chuẩn bị/human-review ở giai đoạn sau -> xuất lại GGUF và ghi toàn bộ config/hash. Đây là model dẫn xuất từ weights lượng tử hóa, **không phải khôi phục chính xác checkpoint gốc trước lượng tử hóa**; phải báo cáo điều đó khi so sánh.

3.085.938.688 parameters ở FP32 chỉ riêng tensor weights khoảng **11,50 GiB** (chưa tính bản sao tạm, model objects và training buffers). Máy RAM ~15,82 GiB/GPU 4 GiB không phù hợp để thử chuyển đổi/train nặng trong phiên này. Chưa cài torch/Transformers/PEFT hoặc tải thêm weights. Môi trường train riêng và lượng bộ nhớ thực tế cần được smoke-test sau, không khẳng định một mức VRAM dự trù là bảo đảm.

Điểm chưa giải quyết của goal: provenance checkpoint gốc và quyền với dữ liệu fine-tune upstream. Đường chuyển đổi trên không giải quyết những thông tin đó. Quyết định dùng GGUF của người dùng đã được áp dụng cho inference; không tự thay model. Chưa đánh dấu goal complete khi các điểm provenance còn chưa xác minh.


## 13. Audit tokenizer và Unicode — 29/10/2026

Đã đọc tokenizer nhúng từ **file GGUF thực tế đã kiểm tra SHA-256**, không chỉ tin metadata Hub. Đối chiếu với tokenizer.json/tokenizer_config.json của Qwen/Qwen2.5-Coder-3B-Instruct tại revision `488639f1ff808d1d3d0ba301aef8c11461451ec5`:

- 151.665 ID được gán ở reference: **0 khác biệt nội dung token**; 22 added tokens đều khớp content.
- 151.387 BPE merges khớp toàn bộ và đúng thứ tự. Chat template khớp byte/string sau parse JSON.
- GGUF có 151.936 ID, dư 271 ID; tất cả đều có tên `[PAD<id>]`. Không tự coi những ID không có trong reference là token được gán tương đương.
- SHA-256 tokenizer.json reference: `c0382117ea329cdf097041132f6d735924b697924d6f6fc3945713e96ce87539`; tokenizer_config.json: `959e7f1d9a1b7641a6d6ce05ca97b75c7894fcb66cbe5a040406458fb1128ee4`. File tải về ở models/.../tokenizer-reference (ignored); bản tóm tắt audit ở phase12-evidence/gguf-tokenizer-audit.json.

### Kiểm tra hành vi, không chạy generation

Dùng tokenizers **0.22.1**, Jinja2 **3.1.6** trong môi trường tách riêng `.tools/tokenizer-audit-venv`, không thay bộ dependency runtime `.venv`. Gọi /tokenize, /detokenize, /apply-template của llama.cpp đã pin, không gọi /chat/completions, không gọi AWS và không tạo tập Text-to-SQL train/test. Có 8 chuỗi chẩn đoán cố định: tiếng Việt, SQL, ký hiệu/emoji, Unicode NFD, ChatML và tool token.

Kết quả raw: token IDs và decode khớp **7/8** chuỗi. Mẫu Unicode NFD có cùng hình thức hiển thị nhưng GGUF giữ dấu tách rời, trong khi reference tokenizer có normalizer `{type: NFC}`. Sau chuẩn hóa đầu vào NFC: **8/8** chuỗi khớp token IDs và decode. Một hội thoại system/user được /apply-template định dạng giống Jinja2 render của template reference.

Đã áp dụng **input_normalization=NFC** cho cả local Qwen và Bedrock, ghi trong model config. Chỉ chuẩn hóa văn bản gửi model; không sửa payload/câu hỏi gốc hoặc dữ liệu nguồn trên disk. Bộ test kiểm tra hai adapter bằng fake server/Bedrock Stubber để bảo đảm cùng chính sách, không làm phát sinh inference cloud. **126 test offline đạt**, xem pytest-tokenizer-audit.xml.

Điều này xác minh tương thích tokenizer ở mức metadata đầy đủ và các mẫu hành vi đã chạy; **không chứng minh mọi chuỗi đều khớp**, không chứng minh trọng số fine-tune giống backbone, không xác minh dataset/checkpoint gốc của tác giả. Chính sách NFC là lựa chọn tiền xử lý được ghi rõ, không phải khẳng định đã khôi phục tokenizer huấn luyện nguyên bản chưa công bố.

Lệnh tái lập:

```powershell
.\.venv\Scripts\python.exe scripts/audit_gguf_tokenizer.py
python -m venv .tools/tokenizer-audit-venv  # chỉ khi chưa tồn tại
.\.tools\tokenizer-audit-venv\Scripts\python.exe -m pip install -r docs/phase12-evidence/tokenizer-audit-environment.txt
.\run-qwen.ps1 doctor
.\.tools\tokenizer-audit-venv\Scripts\python.exe scripts/check_tokenizer_parity.py
```

Không chạy tokenizer parity khi server đang dùng model khác; kiểm tra /v1/models đúng alias trước. Kết quả chi tiết lưu gguf-tokenizer-parity.json; raw mismatch và kết quả sau NFC đều được giữ, không ghi đè mismatch thành “đạt”. Goal vẫn còn yêu cầu source checkpoint/fine-tune provenance chưa xác minh, nên chưa complete.


Đã kiểm tra thêm GGUF Q4_K_M chính thức từ Qwen/Qwen2.5-Coder-3B-Instruct-GGUF qua Hub API (official-gguf-hash-comparison.json). File chính thức có 2.104.932.800 byte, SHA-256 `724fb256bec1ff062b2f65e4569e871ad2e95ab2a3989723d1769c54294730b7`, khác artifact được chọn (1.929.902.496 byte, `b34a...`). Vì vậy không thể dùng hash để nối artifact này với GGUF chính thức. Khác hash/kích thước có thể do quá trình convert/quantization khác, không tự chứng minh có hay không có fine-tune.


## 14. Audit chốt phần độc lập và blocker sau khi resume

Kiểm tra cuối 29/10/2026: **24/24 file dữ liệu khớp hash**, pytest **126 passed / 0 failed / 0 errors**, báo cáo và scripts hiện diện. Hub API vẫn cùng revision, chỉ có .gitattributes + GGUF, không có model card/source checkpoint. Tokenizer audit và parity đã có bằng chứng riêng; không được dùng chúng thay cho bằng chứng provenance tensor weights.

Sau ba lượt goal liên tiếp kể từ yêu cầu resume, cùng điều kiện còn thiếu vẫn là checkpoint Transformers/adapter và recipe/dataset/license của phần fine-tune trước khi xuất GGUF. Các bước độc lập đã thực hiện; không còn thao tác cục bộ an toàn nào có thể xác lập lịch sử huấn luyện chưa công bố. Goal chuyển **blocked**, chưa complete. Cần link checkpoint/notebook **huấn luyện hoặc xuất GGUF** hay provenance từ tác giả để giải quyết phần này. Notebook inference mà người dùng cung cấp đã đọc và không chứa các thông tin đó. Không liên hệ tác giả, không thay model, không chạy train hoặc tạo train/test mới.

Trạng thái blocked của yêu cầu truy nguồn không ngăn người dùng tiếp tục inference/so sánh bằng GGUF đã chọn. Kết quả SQL 107 và các thay đổi routing/dialect/Unicode đã được lưu; không coi đó là hoàn thành yêu cầu xác minh checkpoint gốc.


## 15. Nguồn giấy phép Aave được xác minh thêm qua Zenodo

Kết luận “chưa thấy license dữ liệu” ở phần kiểm tra GitHub ban đầu đã được bổ sung bằng nguồn publisher: DOI 10.5281/zenodo.18339068 và các versions của cùng collection khai báo **CC BY 4.0**. Đã theo links API versions, không suy luận từ repository license=null. Hai bản gần snapshot pin là 22749379 (2026-09-14) và 22994363 (2026-09-27), đều có CC BY 4.0 nhưng archive khác kích thước/MD5. Không coi khác archive là bằng chứng nội dung mọi trường đều khác.

Đã tải bản tham chiếu **22994363**, 35.013.942 byte, MD5 do Zenodo công bố `ca330a58ca06df08194bba525c4bf785`, SHA-256 tính lại `82d5d74eacb2a89bc75b9321f1a114f1f208ebdde681d68503288cb54cbc68db`. Giữ riêng trong .tools, không đổi snapshot runtime.

Sau cùng chuẩn hóa với code runtime, reference có 148.127 market rows và 25.182 events. **Toàn bộ 146.914 market rows và 25.121 events của snapshot pin có mặt và khớp từng trường**, gồm giá trị USD, timestamp, tx_hash, log_index, market, cờ carried và tuổi quan sát; 0 khóa thiếu, 0 ô khác nhau. Kiểm tra DuckDB so với Parquet runtime cũng khớp hoàn toàn. Hash database/dictionary/documents trước và sau không đổi. Bằng chứng đầy đủ: phase12-evidence/data-license-content-audit.json.

Đây là nguồn nội dung được publisher công bố theo CC BY 4.0 khớp phần dữ liệu đã xử lý mà runtime dùng. Không tự mở rộng kết luận sang các trường/raw tables không dùng, mã nguồn repo, nội dung tài liệu Aave hoặc weights/model fine-tune. Thông tin ghi công, DOI và thay đổi đã lưu ở **DATA_ATTRIBUTION.md**. Chưa tạo train/test, chưa fine-tune, không công bố lại archive.

Lệnh tái lập: `.\.venv\Scripts\python.exe scripts/audit_data_license_reference.py`. Archive gốc data-2026-09-15 và mọi file runtime giữ nguyên. Những điểm nguồn checkpoint/dataset/license của phần fine-tune Qwen upstream vẫn chưa được thông tin Zenodo này giải quyết.


## 16. Audit sau khi hoàn tất đối chiếu Zenodo

Đã kiểm tra lại 24 file runtime theo hash manifest: không sai khác. Các quan sát processed khớp bản Zenodo CC BY 4.0 và DuckDB khớp Parquet; bằng chứng 126 test offline đạt và các báo cáo tái lập vẫn hiện diện. Toàn bộ kết quả điều tra độc lập được lưu.

Repo Qwen vẫn cùng revision, chỉ có .gitattributes/GGUF, không có card hoặc source link. Sau ba lượt goal liên tiếp từ lần tiếp tục vừa qua, phần chưa giải quyết vẫn là checkpoint Transformers/adapter/recipe và provenance fine-tune upstream. Không còn thao tác cục bộ hoặc nguồn công khai đã tìm thấy nào có thể chứng minh lịch sử huấn luyện chưa công bố. Goal **blocked**, không complete. Thông tin có thể gỡ chặn: link checkpoint/adapter hoặc notebook huấn luyện/xuất GGUF từ tác giả kèm revision và license. Không tự liên hệ tác giả.

Trạng thái này chỉ áp dụng cho yêu cầu xác minh provenance còn thiếu; vẫn có thể dùng đúng GGUF đã chọn trong UI và tiến hành công việc tiếp theo được người dùng cho phép. Không tạo train/test, không fine-tune hoặc chạy final benchmark trong lần audit này.
