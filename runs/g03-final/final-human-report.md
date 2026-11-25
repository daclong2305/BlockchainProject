# Kết quả test G03

Hai người chấm độc lập theo rubric. Bảng tính trên 40 câu và 3 lượt mỗi cấu hình.

| Cấu hình | Đúng/tổng | Dẫn chứng đạt | Từ chối đúng | Từ chối nhầm | Lỗi runtime | Trung vị (s) | p95 (s) |
|---|---:|---:|---:|---:|---:|---:|---:|
| B0 | 75/120 | 77 | 0 | 0 | 0 | 21.69 | 26.62 |
| B1 | 48/120 | 49 | 0 | 1 | 0 | 32.27 | 80.64 |
| P | 48/120 | 48 | 0 | 1 | 0 | 40.66 | 104.12 |

| Cấu hình | Đúng lượt 1 / 40 | Đúng lượt 2 / 40 | Đúng lượt 3 / 40 |
|---|---:|---:|---:|
| B0 | 24 | 25 | 26 |
| B1 | 13 | 17 | 18 |
| P | 17 | 16 | 15 |

| So sánh | Lượt | Số cặp | Sai → đúng | Đúng → sai | Trong đó từ chối nhầm |
|---|---|---:|---:|---:|---:|
| B0 → P | Tất cả | 120 | 4 | 31 | 0 |
| B0 → P | 1 | 40 | 2 | 9 | 0 |
| B0 → P | 2 | 40 | 1 | 10 | 0 |
| B0 → P | 3 | 40 | 1 | 12 | 0 |
| B1 → P | Tất cả | 120 | 7 | 7 | 0 |
| B1 → P | 1 | 40 | 4 | 0 | 0 |
| B1 → P | 2 | 40 | 2 | 3 | 0 |
| B1 → P | 3 | 40 | 1 | 4 | 0 |

## Chi phí ước tính

| Phạm vi | Token vào | Token ra | Lượt thiếu usage | USD |
|---|---:|---:|---:|---:|
| Toàn bộ runtime | 4393511 | 424619 | 0 | 7.1682666 |
| B0 | 1122852 | 119205 | 0 | 1.8907647 |
| B1 | 2298997 | 254357 | 0 | 3.9278602 |
| P | 3217366 | 289467 | 0 | 5.1311711 |
| Judge | chưa có | chưa có | chưa có | chưa có |

Tổng chi phí runtime tính mỗi bản nháp dùng chung một lần. Chi phí từng cấu hình gồm phần tạo bản nháp khi triển khai riêng.

## Judge so với nhãn đã phân xử

| Tiêu chí | Khớp / có điểm judge |
|---|---:|
| answer_correctness | 0/0 |
| faithfulness | 0/0 |
| citation_quality | 0/0 |

## Case test cho slide

**Q011 · Lượt 2**

Việc rút tài sản đã cung cấp phụ thuộc vào điều kiện nào?

**B0**

Việc rút tài sản đã cung cấp phụ thuộc vào ba điều kiện chính: (1) Phải có đủ thanh khoản trong pool - người cung cấp chỉ có thể rút tối đa số tiền có sẵn trong pool mà không được vay; (2) Nếu tài sản được sử dụng làm tài sản thế chấp cho vị trí vay hoạt động, người dùng có thể cần phải hoàn trả một phần vị trí vay hoặc cung cấp thêm tài sản thế chấp để duy trì mức cân bằng lành mạnh trước khi có thể rút; (3) Phải duy trì health factor ở mức đủ cao - theo dõi thường xuyên health factor sẽ giúp quản lý hiệu quả để tránh tình trạng tài sản thế chấp bị thanh lý.

**P**

Việc rút tài sản đã cung cấp phụ thuộc vào các điều kiện sau: (1) Phải có đủ thanh khoản trong pool - người cung cấp chỉ có thể rút tối đa số tiền có sẵn trong pool mà không được vay hiện tại; (2) Nếu tài sản KHÔNG được sử dụng làm tài sản thế chấp cho vị trí vay hoạt động, có thể tiến hành rút mà không có hạn chế; (3) Nếu tài sản ĐƯỢC sử dụng làm tài sản thế chấp, người dùng có thể cần phải hoàn trả một phần vị trí vay hoặc cung cấp thêm tài sản thế chấp để duy trì mức cân bằng lành mạnh (health factor) trước khi có thể rút; (4) Theo dõi thường xuyên health factor từ Dashboard để quản lý hiệu quả và tránh thanh lý tài sản thế chấp.

**Đoạn nguồn · B0 · DOC_WITHDRAW_000**

Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read

**Đoạn nguồn · P · DOC_WITHDRAW_000**

Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read

**Cảnh báo checker**

- Claim states 'Nếu rút tài sản cơ sở mạng (ví dụ ETH), quá trình rút sẽ liên quan đến WrappedTokenGateway contract để unwrap và rút trong một giao dịch duy nhất' but DOC_WITHDRAW_000 describes WrappedTokenGateway only for the approval step when borrowing network base assets (ETH), not for withdrawal. The withdrawal section mentions WrappedTokenGateway only for unwrapping WETH to ETH during withdrawal, not as a general condition for withdrawing base assets.
- The question asks 'Việc rút tài sản đã cung cấp phụ thuộc vào điều kiện nào?' (What conditions does withdrawal of supplied assets depend on?). The answer lists three conditions but omits a fourth explicit condition from DOC_WITHDRAW_000 Step 3: 'If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount.' This establishes that withdrawal is unrestricted only when the token is NOT used as collateral—a distinct condition from the collateralized case mentioned in Step 5.

**Kết quả sau phân xử** · B0 đạt · P không đạt.

