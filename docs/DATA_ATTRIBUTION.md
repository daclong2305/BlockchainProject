# Ghi công và nguồn giấy phép dữ liệu runtime

## Ghi công nguồn đã đối chiếu

**Chaffard, Owen (2026). Stablecoin DeFi Hourly Dataset - 2026-09-27. Zenodo.**

- DOI của bản tham chiếu: [10.5281/zenodo.22994363](https://doi.org/10.5281/zenodo.22994363).
- [Metadata publisher](https://zenodo.org/api/records/22994363) khai báo **CC BY 4.0**.
- [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) cho phép sao chép/chuyển thể nội dung thuộc giấy phép, với nghĩa vụ ghi công, dẫn giấy phép và nêu thay đổi. Không gán giấy phép này cho model weights hoặc mã nguồn GitHub chỉ từ metadata dataset.

## Snapshot thực sự đang chạy

Ứng dụng vẫn tải và dùng [GitHub release data-2026-09-15](https://github.com/MSCA-DN-Digital-Finance/stablecoin-onchain-data/releases/tag/data-2026-09-15), file aave_data.zip, SHA-256 `1d4d8025b5aed07707d341b5824b6954d9869b8416e11efa2832ceafeaedf91e`. Không thay bằng snapshot Zenodo tháng 9/27 hoặc latest.

ZIP gốc khác ZIP Zenodo. Tuy nhiên, kiểm tra ngày 29/10/2026 xác nhận **toàn bộ 146.914 dòng market và 25.121 sự kiện được runtime sử dụng**, sau cùng phép chuẩn hóa, đều có trong bản Zenodo tham chiếu, với **0 khóa thiếu và 0 ô khác nhau**. DuckDB runtime cũng khớp các bảng Parquet đã đối chiếu. Vì vậy bản Zenodo cung cấp nguồn nội dung công bố theo CC BY 4.0 tương ứng với các quan sát runtime này, không chỉ một tên dataset tương tự.

Bằng chứng: [data-license-content-audit.json](phase12-evidence/data-license-content-audit.json), gồm hash của hai Parquet, database, ZIP pin và ZIP tham chiếu. Đối chiếu chỉ bao phủ các trường được pipeline hiện tại dùng, không khẳng định toàn bộ 13 file/mọi cột trong ZIP gốc giống ZIP tham chiếu.

## Các thay đổi/biến đổi tại project

Chọn Aave V3 Ethereum, DAI/USDC/USDT/USDe/WETH và sự kiện thanh lý; chuẩn hóa timestamp UTC, tên trường và kiểu số; thêm thông tin source_file, is_carried, source_age_hours; kiểm tra khóa; tạo Parquet/DuckDB, coverage, audit và dictionary. Không dùng profitUSD/gas/APR hoặc mapping token thanh lý chưa kiểm chứng; không biến null thành 0. Không tạo train/test hoặc fine-tune trong bước audit này.

Bản tham chiếu, file giải nén và database phụ ở `.tools/data-license-reference/22994363/`, bị gitignore. Không công bố lại archive trong project. Tài liệu Aave truy xuất và weights Qwen có nguồn/điều kiện riêng; kết quả audit này không cấp hoặc xác minh giấy phép cho các artifact đó.

## Tái lập

```powershell
.\.venv\Scripts\python.exe scripts/audit_data_license_reference.py
```

Script xác minh kích thước và MD5 do Zenodo công bố, ghi thêm SHA-256, chỉ giải nén sáu file cần thiết vào thư mục riêng, so sánh từng trường theo khóa và xác nhận hash runtime không đổi. Lần đầu cần tải khoảng 35 MB; các khối tải xong được giữ để tiếp tục nếu mạng lỗi. Không chuyển latest và không gọi model/AWS.
