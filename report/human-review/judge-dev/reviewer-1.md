# Independent audit

Assess each answer against the supplied reference and sources. Do not inspect machine labels or the other reviewer’s decisions.
Record 0 or 1 for correctness, faithfulness and citation quality; give reasons. Do not infer correctness from a runtime passed status. Gold must already have independent review for a final experiment.

## A0001

```json
{
  "question": "Giá trị dư nợ trung bình theo giờ của DAI trong tháng 2026-06 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 98282885.63031632
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-06-01' AND hour < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": 98282885.63031632
        }
      ]
    }
  ],
  "system_answer": "Giá trị dư nợ trung bình theo giờ của DAI trong tháng 2026-06 là 98,282,885.63 USD, dựa trên bộ dữ liệu hiện có.",
  "system_claims": [
    {
      "text": "Giá trị dư nợ trung bình theo giờ của DAI trong khoảng thời gian từ 2026-06-01T00:00:00Z đến 2026-07-01T00:00:00Z là 98,282,885.63 USD",
      "citations": [
        "[SQL1]"
      ],
      "numeric": {
        "value": 98282885.63,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_borrowed_usd_dai_june_2026"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT AVG(borrowed_usd) AS avg_borrowed_usd_dai_june_2026 FROM market_hourly WHERE asset = 'DAI' AND hour >= '2026-06-01T00:00:00Z' AND hour < '2026-07-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_borrowed_usd_dai_june_2026"
    ],
    "rows": [
      {
        "avg_borrowed_usd_dai_june_2026": 98282885.63031632
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0002

```json
{
  "question": "Dư nợ USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1993676848.0321777
        }
      ]
    }
  ],
  "system_answer": "Dư nợ USDC lúc 00:00 UTC ngày 2026-08-15 là 1,993,676,848.03 USD, theo bộ dữ liệu hiện có từ bảng market_hourly. Quan sát này được lấy từ nguồn tại 2026-08-14T23:58:35 UTC (khoảng 1 phút 25 giây trước grid hour).",
  "system_claims": [
    {
      "text": "Dư nợ USDC tại 2026-08-15T00:00:00 UTC là 1,993,676,848.03 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1993676848.03,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd_snapshot"
      }
    },
    {
      "text": "Dữ liệu này không phải quan sát mới tại grid hour mà được mang từ nguồn trước đó (is_carried = false cho biết đây là quan sát trực tiếp, không được mang từ hour trước)",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 0,
        "unit": "other",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "is_carried"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, borrowed_usd AS borrowed_usd_snapshot, source_timestamp, is_carried FROM market_hourly WHERE asset = 'USDC' AND hour >= '2026-08-15T00:00:00Z' AND hour < '2026-08-15T01:00:00Z' ORDER BY hour",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd_snapshot",
      "source_timestamp",
      "is_carried"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "borrowed_usd_snapshot": 1993676848.0321777,
        "source_timestamp": "2026-08-14T23:58:35+00:00",
        "is_carried": false
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0003

```json
{
  "question": "Cung cấp tài sản trên Aave V3 là gì?",
  "reference_answer": {
    "required_points": [
      "Cung cấp token vào pool; phân biệt cung cấp với vay, không bảo đảm mức lãi cố định."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can"
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "system_answer": "Cung cấp tài sản trên Aave V3 là quá trình chuyển token của bạn vào nhóm thanh khoản của Aave thông qua các hợp đồng thông minh. Khi bạn cung cấp token, chúng được thêm vào nhóm thanh khoản và có sẵn cho những người vay. Các token được cung cấp sẽ tự động tích lũy lãi suất bằng cách cập nhật số dư theo tỷ lệ cung cấp hiện tại trên thị trường. Lãi suất được xác định bởi tỷ lệ sử dụng vay (tỷ lệ giữa tài sản được vay và tổng tài sản được cung cấp trong nhóm) và các thông số quản trị có thể được điều chỉnh thông qua quyết định của cộng đồng. Bạn cũng có thể sử dụng các token được cung cấp làm tài sản thế chấp để vay.",
  "system_claims": [
    {
      "text": "Khi token được cung cấp, chúng được chuyển vào nhóm thanh khoản Aave, một hệ thống các hợp đồng thông minh tạo điều kiện cho việc vay token được thế chấp quá mức",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Các token được cung cấp sẽ bắt đầu kiếm lãi ngay lập tức, lãi suất tích lũy động khi số dư của các token được cung cấp tăng tuyến tính theo thời gian",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Lãi suất cho các token được cung cấp được xác định bởi tỷ lệ sử dụng vay (tỷ lệ giữa tài sản hiện đang được vay so với tổng tài sản được cung cấp trong nhóm) và các thông số quản trị có thể được điều chỉnh thông qua quyết định của cộng đồng",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Bạn có thể sử dụng các token được cung cấp làm tài sản thế chấp",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 1.5042149877429303
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.4521542201091049
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.3938221003879567
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 1.3719929055749946
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.1204499709813494
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0004

```json
{
  "question": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Dư nợ là số dư tại thời điểm; không coi là tổng số tiền vay mới trong tháng."
    ],
    "sql_result": [
      {
        "value": 3042883324.3152447
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
      "rows": [
        {
          "value": 3042883324.3152447
        }
      ]
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là 3,042,883,324.32 USD [SQL1]. Không thể coi đây là tổng tiền vay mới trong tháng vì lý do sau: (1) Giá trị này là một 'snapshot' - tồn kho nợ tại một thời điểm cụ thể, không phải luồng vay mới. Theo tài liệu, 'borrowed_usd' là 'USD debt stock at hour, never SUM over time' [dictionary], nghĩa là nó đo lường tổng dư nợ hiện tại, không phải vay mới. (2) Để tính tiền vay mới trong tháng, cần so sánh dư nợ tại đầu tháng với cuối tháng hoặc theo dõi các sự kiện vay riêng lẻ, không phải dùng một snapshot đơn lẻ. (3) Dư nợ này bao gồm cả lãi suất tích lũy - tài liệu nêu rõ 'interest on the borrowed tokens begins to accrue immediately' [DOC_BORROW_001], do đó phần tăng có thể do lãi suất, không phải vay mới.",
  "system_claims": [
    {
      "text": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là 3,042,883,324.32 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 3042883324.32,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "weth_borrowed_usd_at_snapshot"
      }
    },
    {
      "text": "borrowed_usd là tồn kho nợ (debt stock) tại một giờ cụ thể, không bao giờ được tính tổng theo thời gian",
      "citations": [
        "dictionary"
      ]
    },
    {
      "text": "Lãi suất trên các token được vay bắt đầu tích lũy ngay lập tức và được điều chỉnh động dựa trên tỷ lệ sử dụng vay",
      "citations": [
        "DOC_BORROW_001"
      ]
    },
    {
      "text": "Để tính tiền vay mới trong tháng, cần so sánh dư nợ tại các thời điểm khác nhau hoặc theo dõi các sự kiện vay riêng lẻ, không phải dùng một snapshot đơn lẻ",
      "citations": [
        "DOC_BORROW_000",
        "DOC_BORROW_001"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 3.5076459907350617
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.6444574664132487
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.4970938941352956
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 0.9686956651770642
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.807323076503812
    }
  ],
  "sql": "SELECT asset, hour, borrowed_usd AS weth_borrowed_usd_at_snapshot, is_carried, source_timestamp FROM market_hourly WHERE asset = 'WETH' AND hour = '2026-07-15T00:00:00Z' LIMIT 1;",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "weth_borrowed_usd_at_snapshot",
      "is_carried",
      "source_timestamp"
    ],
    "rows": [
      {
        "asset": "WETH",
        "hour": "2026-07-15T00:00:00+00:00",
        "weth_borrowed_usd_at_snapshot": 3042883324.3152447,
        "is_carried": false,
        "source_timestamp": "2026-07-14T23:59:59+00:00"
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0005

```json
{
  "question": "Giá trị tài sản cung cấp trung bình theo giờ của USDT trong tháng 2026-07 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 2831780087.9296083
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-07-01' AND hour < TIMESTAMPTZ '2026-08-01'",
      "rows": [
        {
          "value": 2831780087.9296083
        }
      ]
    }
  ],
  "system_answer": "Giá trị tài sản cung cấp trung bình theo giờ của USDT trong tháng 2026-07 là 2,831,780,087.93 USD, dựa trên bộ dữ liệu hiện có.\n\nChưa thể xác minh đầy đủ: Truy vấn yêu cầu dữ liệu từ tháng 7-2026, nhưng ngày hiện tại là trước 2026-07-01. Dữ liệu USDT trong bộ dữ liệu chỉ có sẵn đến 2026-09-15T07:00:00Z theo availability metadata, tuy nhiên đây là dữ liệu tương lai so với thời điểm hiện tại.; SQL truy vấn chính xác về mặt cú pháp. Khoảng thời gian 2026-07-01 đến 2026-08-01 nằm trong phạm vi dữ liệu USDT có sẵn (2023-02-13T14:00:00Z đến 2026-09-15T07:00:00Z). Kết quả trả về 1 hàng với giá trị trung bình.; Câu trả lời được hỗ trợ bởi SQL result. Giá trị 2,831,780,087.93 USD là trung bình số học của cột supplied_usd cho tất cả các hàng USDT trong khoảng thời gian được chỉ định. Không có tài liệu nguồn được cung cấp để xác minh thêm.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp trung bình theo giờ của USDT trong khoảng thời gian từ 2026-07-01 đến 2026-08-01 là 2,831,780,087.93 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 2831780087.93,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_supplied_usd"
      }
    },
    {
      "text": "Dữ liệu USDT trong bộ dữ liệu hiện có bao gồm các quan sát từ 2023-02-13T14:00:00Z đến 2026-09-15T07:00:00Z",
      "citations": [
        "availability"
      ]
    }
  ],
  "documents": [],
  "sql": "SELECT AVG(\"supplied_usd\") AS avg_supplied_usd FROM \"market_hourly\" WHERE \"asset\" = 'USDT' AND \"hour\" >= '2026-07-01T00:00:00Z' AND \"hour\" < '2026-08-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_supplied_usd"
    ],
    "rows": [
      {
        "avg_supplied_usd": 2831780087.9296083
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0006

```json
{
  "question": "Dư nợ WETH lúc 00:00 UTC ngày 2025-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 10023005896.239573
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2025-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 10023005896.239573
        }
      ]
    }
  ],
  "system_answer": "Dư nợ WETH lúc 00:00 UTC ngày 2025-08-15 là 10,023,005,896.24 USD, theo bộ dữ liệu hiện có từ bảng market_hourly.",
  "system_claims": [
    {
      "text": "Dư nợ WETH (borrowed_usd) lúc 00:00 UTC ngày 2025-08-15 là 10,023,005,896.24 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 10023005896.24,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, borrowed_usd FROM market_hourly WHERE asset = 'WETH' AND hour >= '2025-08-15T00:00:00Z' AND hour < '2025-08-15T01:00:00Z' ORDER BY hour",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd"
    ],
    "rows": [
      {
        "asset": "WETH",
        "hour": "2025-08-15T00:00:00+00:00",
        "borrowed_usd": 10023005896.239573
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0007

```json
{
  "question": "Tài sản thế chấp có vai trò gì khi vay trên Aave V3? Hãy trả lời ngắn gọn và dẫn nguồn.",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Tài sản thế chấp trên Aave V3 có vai trò then chốt: (1) Cho phép vay: Người dùng phải cung cấp tài sản thế chấp để truy cập thanh khoản và vay token [DOC_BORROW_000]. (2) Xác định khả năng vay: Giá trị thế chấp được sử dụng để tính Health Factor = (Tổng giá trị thế chấp × Trọng số Ngưỡng thanh lý trung bình) / Tổng giá trị vay [DOC_LIQ_000]. (3) Bảo vệ chống thanh lý: Phải duy trì Health Factor > 1 để tránh thanh lý; nếu Health Factor < 1, vị thế có nguy cơ bị thanh lý [DOC_LIQ_000]. (4) Quản lý rủi ro: Người vay phải giám sát thường xuyên và có thể cung cấp thêm thế chấp hoặc trả lại khoản vay để duy trì sự an toàn [DOC_BORROW_000].",
  "system_claims": [
    {
      "text": "Tài sản thế chấp cho phép người dùng truy cập thanh khoản và vay token từ Aave Protocol",
      "citations": [
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Health Factor được tính bằng công thức: (Tổng giá trị thế chấp × Trọng số Ngưỡng thanh lý trung bình) / Tổng giá trị vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Health Factor dưới 1 báo hiệu rủi ro thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Người vay phải duy trì Health Factor trên 1 để tránh thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Để cải thiện Health Factor, người vay có thể cung cấp thêm thế chấp hoặc trả lại một phần khoản vay",
      "citations": [
        "DOC_BORROW_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.8990474021112234
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.854258546537117
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.793707409879604
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.636978214687525
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.6683151106511598
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0008

```json
{
  "question": "Giá trị tài sản cung cấp WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Có thể coi đây là lợi nhuận người cung cấp đã thu được không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Giá trị cung cấp là số dư, không phải lợi nhuận thu được."
    ],
    "sql_result": [
      {
        "value": 3897799627.0425687
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
      "rows": [
        {
          "value": 3897799627.0425687
        }
      ]
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can"
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "system_answer": "Giá trị tài sản cung cấp WETH lúc 00:00 UTC 2026-07-15 là 3.897.799.627,04 USD trong bộ dữ liệu hiện có. Tuy nhiên, không thể coi đây là lợi nhuận người cung cấp đã thu được vì lý do sau: (1) Giá trị này là một snapshot của tổng USD của tất cả WETH được cung cấp tại thời điểm đó, không phải lợi nhuận của một người cung cấp cụ thể. (2) Theo tài liệu Aave, lợi nhuận người cung cấp được tạo ra thông qua cơ chế lãi suất động - số dư WETH được cung cấp tự động tích lũy lãi suất bằng cách cập nhật số dư theo tỷ lệ cung cấp thị trường hiện tại. Điều này có nghĩa lợi nhuận là sự gia tăng số lượng token hoặc giá trị theo thời gian, không phải giá trị tuyệt đối tại một thời điểm. (3) Để xác định lợi nhuận thực tế, cần so sánh giá trị cung cấp giữa hai thời điểm khác nhau hoặc tính toán sự thay đổi số dư token.\n\nChưa thể xác minh đầy đủ: Answer is well-supported by source data and SQL result. The snapshot value (3,897,799,627.04 USD) is correctly extracted from the query result. The explanation correctly distinguishes between a stock balance snapshot and accrued earnings, citing DOC_SUPPLY_000 which explicitly describes interest accrual as dynamic balance updates over time, not a point-in-time value. The answer appropriately notes that comparing two time periods would be needed to measure actual earnings.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp WETH lúc 00:00 UTC 2026-07-15 là 3.897.799.627,04 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 3897799627.04,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "weth_supplied_usd_at_snapshot"
      }
    },
    {
      "text": "Giá trị snapshot này không thể coi là lợi nhuận người cung cấp vì nó là tổng giá trị tài sản cung cấp tại một thời điểm, không phải lợi nhuận",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Lợi nhuận người cung cấp được tạo ra thông qua cơ chế lãi suất động - số dư WETH được cung cấp tự động tích lũy lãi suất bằng cách cập nhật số dư theo tỷ lệ cung cấp thị trường hiện tại, phản ánh sự gia tăng giá trị theo thời gian",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Để xác định lợi nhuận thực tế, cần so sánh giá trị cung cấp giữa hai thời điểm khác nhau hoặc tính toán sự thay đổi số dư token theo thời gian",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 3.0420445442042103
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 0.28186567708729404
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.23562127435973954
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.2241707276306713
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 0.0
    }
  ],
  "sql": "SELECT asset, hour, supplied_usd AS weth_supplied_usd_at_snapshot FROM market_hourly WHERE asset = 'WETH' AND hour = '2026-07-15T00:00:00Z' LIMIT 1",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "weth_supplied_usd_at_snapshot"
    ],
    "rows": [
      {
        "asset": "WETH",
        "hour": "2026-07-15T00:00:00+00:00",
        "weth_supplied_usd_at_snapshot": 3897799627.0425687
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0009

```json
{
  "question": "Giá trị dư nợ trung bình theo giờ của USDT trong tháng 2026-07 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 2337819599.9938083
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-07-01' AND hour < TIMESTAMPTZ '2026-08-01'",
      "rows": [
        {
          "value": 2337819599.9938083
        }
      ]
    }
  ],
  "system_answer": "Giá trị dư nợ trung bình theo giờ của USDT trong tháng 2026-07 (từ 2026-07-01 đến 2026-08-01) là 2,337,819,599.99 USD, dựa trên bộ dữ liệu hiện có.\n\nChưa thể xác minh đầy đủ: USDT data in market_hourly ends at 2026-09-15T07:00:00Z, but requested interval 2026-07-01 to 2026-08-01 is within observed bounds. However, availability shows USDT start is 2023-02-13T14:00:00Z with 31434 observed_hours. The query requests July 2026 (744 hours), which falls within the observed range. No coverage gap detected for the requested month.; borrowed_usd is a stock metric (debt balance at a point in time). The SQL uses AVG(borrowed_usd) across hourly observations within July 2026. Dictionary confirms 'borrowed_usd: USD debt stock at hour, never SUM over time'. Averaging a stock across hourly grid points is semantically valid when the question explicitly requests an average. Question asks 'giá trị dư nợ trung bình theo giờ' (average debt value by hour), confirming AVG is the correct aggregation.; SQL uses hour >= '2026-07-01T00:00:00Z' AND hour < '2026-08-01T00:00:00Z', which correctly implements the calendar month [2026-07-01, 2026-08-01) with exclusive upper bound. This matches requirements and question_anchors.; SQL filters WHERE asset = 'USDT', matching the requirements assets list and question specification.",
  "system_claims": [
    {
      "text": "Giá trị dư nợ trung bình theo giờ của USDT trong tháng 2026-07 là 2,337,819,599.99 USD",
      "citations": [
        "[SQL1]"
      ],
      "numeric": {
        "value": 2337819599.99,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_borrowed_usd_july_2026"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT AVG(borrowed_usd) AS avg_borrowed_usd_july_2026 FROM market_hourly WHERE asset = 'USDT' AND hour >= '2026-07-01T00:00:00Z' AND hour < '2026-08-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_borrowed_usd_july_2026"
    ],
    "rows": [
      {
        "avg_borrowed_usd_july_2026": 2337819599.9938083
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0010

```json
{
  "question": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1997694271.598428
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1997694271.598428
        }
      ]
    }
  ],
  "system_answer": "Giá trị tài sản USDC được cung cấp lúc 00:00 UTC ngày 2026-08-15 là 1,997,694,271.60 USD, theo dữ liệu trong bộ dữ liệu hiện có.\n\nChưa thể xác minh đầy đủ: Requested hour 2026-08-15T00:00:00Z is within the observed availability window for USDC (end_utc: 2026-09-15T07:00:00+00:00), but the question asks for a snapshot at a specific UTC hour. The SQL query correctly filters for this hour and returned 1 row with supplied_usd = 1997694271.598428 USD. However, this is a future date relative to typical analysis contexts. Verify that 2026-08-15 data is intentional and that the loaded dataset actually contains observations for this date.; Khoảng thời gian yêu cầu 2026-08-15T00:00:00Z nằm ngoài phạm vi dữ liệu quan sát được. Dữ liệu USDC trong market_hourly kết thúc lúc 2026-09-15T07:00:00Z, nhưng điểm dữ liệu được trả về (2026-08-15T00:00:00Z) nằm trong khoảng này. Tuy nhiên, cần xác nhận rằng đây không phải là dự báo tương lai. Nếu ngày hôm nay trước 2026-08-15, đây là dữ liệu tương lai và không thể xác minh.; Trường documents rỗng. Không có tài liệu nguồn nào được truy xuất để hỗ trợ hoặc xác thực giá trị supplied_usd được báo cáo từ SQL.; Giá trị supplied_usd_snapshot = 1,997,694,271.60 USD được trích xuất từ kết quả SQL duy nhất. Không có tài liệu tham khảo, nhận xét hoặc xác thực độc lập nào được cung cấp để xác nhận tính chính xác của con số này hoặc phương pháp tính toán.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC ngày 2026-08-15 là 1,997,694,271.60 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1997694271.6,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "supplied_usd_snapshot"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, supplied_usd AS supplied_usd_snapshot FROM market_hourly WHERE asset = 'USDC' AND hour = '2026-08-15T00:00:00Z' LIMIT 1",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "supplied_usd_snapshot"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "supplied_usd_snapshot": 1997694271.598428
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0011

```json
{
  "question": "Cung cấp tài sản trên Aave V3 là gì?",
  "reference_answer": {
    "required_points": [
      "Cung cấp token vào pool; phân biệt cung cấp với vay, không bảo đảm mức lãi cố định."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can"
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "system_answer": "Cung cấp tài sản trên Aave V3 là quá trình chuyển token của bạn vào nhóm thanh khoản của Aave thông qua các hợp đồng thông minh. Khi bạn cung cấp token, chúng được thêm vào nhóm thanh khoản và có sẵn cho những người vay. Các token được cung cấp sẽ tự động tích lũy lãi suất bằng cách cập nhật số dư theo tỷ lệ cung cấp hiện tại trên thị trường. Lãi suất được xác định bởi tỷ lệ sử dụng vay (tỷ lệ giữa tài sản được vay và tổng tài sản được cung cấp trong nhóm) và các thông số quản trị có thể được điều chỉnh thông qua quyết định của cộng đồng. Bạn cũng có thể sử dụng các token được cung cấp làm tài sản thế chấp để vay.",
  "system_claims": [
    {
      "text": "Khi token được cung cấp, chúng được chuyển vào nhóm thanh khoản Aave, một hệ thống các hợp đồng thông minh tạo điều kiện cho việc vay token được thế chấp quá mức",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Các token được cung cấp sẽ bắt đầu kiếm lãi ngay lập tức, lãi suất tích lũy động khi số dư của các token được cung cấp tăng tuyến tính theo thời gian",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Lãi suất cho các token được cung cấp được xác định bởi tỷ lệ sử dụng vay (tỷ lệ giữa tài sản hiện đang được vay so với tổng tài sản được cung cấp trong nhóm) và các thông số quản trị có thể được điều chỉnh thông qua quyết định của cộng đồng",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Bạn có thể sử dụng các token được cung cấp làm tài sản thế chấp",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 1.5042149877429303
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.4521542201091049
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.3938221003879567
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 1.3719929055749946
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.1204499709813494
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0012

```json
{
  "question": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Dư nợ là số dư tại thời điểm; không coi là tổng số tiền vay mới trong tháng."
    ],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1993676848.0321777
        }
      ]
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là 1,993,676,848.00 USD (từ bộ dữ liệu hiện có) [SQL1]. Không thể coi đây là tổng tiền vay mới trong tháng vì lý do sau: (1) Số liệu này là một 'stock' (dư nợ tức thời) chứ không phải 'flow' (tiền vay mới). Nó đại diện cho tổng nợ còn lại tại một thời điểm, không phải tổng tiền vay mới phát sinh trong tháng 8. (2) Dư nợ này bao gồm các khoản vay từ các tháng trước cộng với lãi suất tích lũy động theo thời gian [DOC_BORROW_000, DOC_BORROW_001]. (3) Để xác định tiền vay mới trong tháng, cần so sánh snapshot này với dữ liệu từ đầu tháng (2026-08-01T00:00:00Z) và loại trừ phần lãi suất tích lũy, nhưng bộ dữ liệu hiện có không cung cấp đủ thông tin để tách riêng các thành phần này.\n\nChưa thể xác minh đầy đủ: Missing requested start boundary 2026-08-15T00:00:00Z; Missing requested end boundary 2026-08-15T01:00:00Z; Requirements specify end='2026-08-15T01:00:00Z' (1-hour window), but SQL filters hour < '2026-08-16T00:00:00Z' (full day). For a snapshot at 2026-08-15T00:00:00Z, the exclusive end should be '2026-08-15T01:00:00Z', not the next calendar day.; Requirements specify aggregation='snapshot' for a single point-in-time value at 2026-08-15T00:00:00Z, but SQL returns all hourly rows from 2026-08-01 through 2026-08-15. A snapshot requires filtering to exactly one hour row, not a time series.; Question asks 'Có thể coi đây là tổng tiền vay mới trong tháng không?' (Can this be considered total new borrowing in the month?). A single borrowed_usd snapshot is a stock balance, not a flow. New borrowing in August requires transaction-level borrow events summed over the month, not a point-in-time debt stock. The snapshot cannot answer the flow question.",
  "system_claims": [
    {
      "text": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là 1,993,676,848.00 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1993676848.0,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd_snapshot"
      }
    },
    {
      "text": "Số liệu dư nợ là một stock (dư nợ tức thời) chứ không phải flow (tiền vay mới)",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Dư nợ bao gồm các khoản vay từ các tháng trước cộng với lãi suất tích lũy động theo thời gian",
      "citations": [
        "DOC_BORROW_000",
        "DOC_BORROW_001"
      ]
    },
    {
      "text": "Lãi suất trên các khoản vay bắt đầu tích lũy ngay lập tức và được điều chỉnh động dựa trên borrow utilization rate",
      "citations": [
        "DOC_BORROW_001"
      ]
    },
    {
      "text": "Không thể coi snapshot dư nợ tại 2026-08-15T00:00:00Z là tổng tiền vay mới trong tháng 8 vì nó là một điểm dữ liệu tức thời, không phải tổng hợp luồng hoạt động mới trong suốt tháng",
      "citations": [
        "SQL1"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.7032670712231535
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.4683022404306918
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.344979433214291
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.4483414552613426
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 0.3529037929017164
    }
  ],
  "sql": "SELECT asset, hour, borrowed_usd AS borrowed_usd_snapshot, source_timestamp, is_carried FROM market_hourly WHERE asset = 'USDC' AND hour >= '2026-08-01T00:00:00Z' AND hour < '2026-08-16T00:00:00Z' ORDER BY hour;",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd_snapshot",
      "source_timestamp",
      "is_carried"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-01T00:00:00+00:00",
        "borrowed_usd_snapshot": 1940447808.541687,
        "source_timestamp": "2026-07-31T23:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T01:00:00+00:00",
        "borrowed_usd_snapshot": 1940495458.2797034,
        "source_timestamp": "2026-08-01T00:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T02:00:00+00:00",
        "borrowed_usd_snapshot": 1940481665.0593674,
        "source_timestamp": "2026-08-01T01:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T03:00:00+00:00",
        "borrowed_usd_snapshot": 1940482665.20737,
        "source_timestamp": "2026-08-01T02:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T04:00:00+00:00",
        "borrowed_usd_snapshot": 1940492189.9950166,
        "source_timestamp": "2026-08-01T03:55:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T05:00:00+00:00",
        "borrowed_usd_snapshot": 1940217462.7659476,
        "source_timestamp": "2026-08-01T04:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T06:00:00+00:00",
        "borrowed_usd_snapshot": 1940462899.7895942,
        "source_timestamp": "2026-08-01T05:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T07:00:00+00:00",
        "borrowed_usd_snapshot": 1940474662.8437881,
        "source_timestamp": "2026-08-01T06:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T08:00:00+00:00",
        "borrowed_usd_snapshot": 1940595013.0560744,
        "source_timestamp": "2026-08-01T07:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T09:00:00+00:00",
        "borrowed_usd_snapshot": 1940623950.638068,
        "source_timestamp": "2026-08-01T08:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T10:00:00+00:00",
        "borrowed_usd_snapshot": 1940696582.3329494,
        "source_timestamp": "2026-08-01T09:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T11:00:00+00:00",
        "borrowed_usd_snapshot": 1940690215.3137188,
        "source_timestamp": "2026-08-01T10:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T12:00:00+00:00",
        "borrowed_usd_snapshot": 1940548529.112959,
        "source_timestamp": "2026-08-01T11:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T13:00:00+00:00",
        "borrowed_usd_snapshot": 1940515832.804648,
        "source_timestamp": "2026-08-01T12:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T14:00:00+00:00",
        "borrowed_usd_snapshot": 1940546192.2126434,
        "source_timestamp": "2026-08-01T13:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T15:00:00+00:00",
        "borrowed_usd_snapshot": 1940595343.446808,
        "source_timestamp": "2026-08-01T14:55:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T16:00:00+00:00",
        "borrowed_usd_snapshot": 1940460998.7437544,
        "source_timestamp": "2026-08-01T15:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T17:00:00+00:00",
        "borrowed_usd_snapshot": 1940520887.980357,
        "source_timestamp": "2026-08-01T16:57:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T18:00:00+00:00",
        "borrowed_usd_snapshot": 1940493993.1850977,
        "source_timestamp": "2026-08-01T17:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T19:00:00+00:00",
        "borrowed_usd_snapshot": 1940513498.8068287,
        "source_timestamp": "2026-08-01T18:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T20:00:00+00:00",
        "borrowed_usd_snapshot": 1940357639.0623484,
        "source_timestamp": "2026-08-01T19:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T21:00:00+00:00",
        "borrowed_usd_snapshot": 1940286980.5574667,
        "source_timestamp": "2026-08-01T20:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T22:00:00+00:00",
        "borrowed_usd_snapshot": 1940318063.8521137,
        "source_timestamp": "2026-08-01T21:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-01T23:00:00+00:00",
        "borrowed_usd_snapshot": 1940531002.7566378,
        "source_timestamp": "2026-08-01T22:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T00:00:00+00:00",
        "borrowed_usd_snapshot": 1940775099.5192487,
        "source_timestamp": "2026-08-01T23:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T01:00:00+00:00",
        "borrowed_usd_snapshot": 1940777755.8295138,
        "source_timestamp": "2026-08-02T00:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T02:00:00+00:00",
        "borrowed_usd_snapshot": 1940788409.28861,
        "source_timestamp": "2026-08-02T01:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T03:00:00+00:00",
        "borrowed_usd_snapshot": 1940801315.1363554,
        "source_timestamp": "2026-08-02T02:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T04:00:00+00:00",
        "borrowed_usd_snapshot": 1940818343.2012527,
        "source_timestamp": "2026-08-02T03:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T05:00:00+00:00",
        "borrowed_usd_snapshot": 1940827046.3959193,
        "source_timestamp": "2026-08-02T04:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T06:00:00+00:00",
        "borrowed_usd_snapshot": 1940843092.5304744,
        "source_timestamp": "2026-08-02T05:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T07:00:00+00:00",
        "borrowed_usd_snapshot": 1940828653.7838595,
        "source_timestamp": "2026-08-02T06:56:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T08:00:00+00:00",
        "borrowed_usd_snapshot": 1941142607.556518,
        "source_timestamp": "2026-08-02T07:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T09:00:00+00:00",
        "borrowed_usd_snapshot": 1941061824.7329674,
        "source_timestamp": "2026-08-02T08:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T10:00:00+00:00",
        "borrowed_usd_snapshot": 1941058539.247926,
        "source_timestamp": "2026-08-02T09:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T11:00:00+00:00",
        "borrowed_usd_snapshot": 1941237641.6796288,
        "source_timestamp": "2026-08-02T10:54:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T12:00:00+00:00",
        "borrowed_usd_snapshot": 1940775729.398761,
        "source_timestamp": "2026-08-02T11:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T13:00:00+00:00",
        "borrowed_usd_snapshot": 1940805089.0685008,
        "source_timestamp": "2026-08-02T12:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T14:00:00+00:00",
        "borrowed_usd_snapshot": 1940809782.1870384,
        "source_timestamp": "2026-08-02T13:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T15:00:00+00:00",
        "borrowed_usd_snapshot": 1941089493.9116342,
        "source_timestamp": "2026-08-02T14:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T16:00:00+00:00",
        "borrowed_usd_snapshot": 1941175576.4571645,
        "source_timestamp": "2026-08-02T15:52:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T17:00:00+00:00",
        "borrowed_usd_snapshot": 1941160492.319851,
        "source_timestamp": "2026-08-02T16:57:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T18:00:00+00:00",
        "borrowed_usd_snapshot": 1940580370.911544,
        "source_timestamp": "2026-08-02T17:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T19:00:00+00:00",
        "borrowed_usd_snapshot": 1940669047.8714666,
        "source_timestamp": "2026-08-02T18:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T20:00:00+00:00",
        "borrowed_usd_snapshot": 1940114626.986181,
        "source_timestamp": "2026-08-02T19:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T21:00:00+00:00",
        "borrowed_usd_snapshot": 1940133169.5435762,
        "source_timestamp": "2026-08-02T20:57:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T22:00:00+00:00",
        "borrowed_usd_snapshot": 1940187182.6106536,
        "source_timestamp": "2026-08-02T21:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-02T23:00:00+00:00",
        "borrowed_usd_snapshot": 1940014920.9001324,
        "source_timestamp": "2026-08-02T22:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T00:00:00+00:00",
        "borrowed_usd_snapshot": 1940475319.783242,
        "source_timestamp": "2026-08-02T23:51:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T01:00:00+00:00",
        "borrowed_usd_snapshot": 1940499381.1113389,
        "source_timestamp": "2026-08-03T00:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T02:00:00+00:00",
        "borrowed_usd_snapshot": 1940514120.1371493,
        "source_timestamp": "2026-08-03T01:54:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T03:00:00+00:00",
        "borrowed_usd_snapshot": 1940542168.515114,
        "source_timestamp": "2026-08-03T02:53:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T04:00:00+00:00",
        "borrowed_usd_snapshot": 1940658892.5707762,
        "source_timestamp": "2026-08-03T03:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T05:00:00+00:00",
        "borrowed_usd_snapshot": 1940548417.9971058,
        "source_timestamp": "2026-08-03T04:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T06:00:00+00:00",
        "borrowed_usd_snapshot": 1940500186.7961385,
        "source_timestamp": "2026-08-03T05:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T07:00:00+00:00",
        "borrowed_usd_snapshot": 1940670458.141786,
        "source_timestamp": "2026-08-03T06:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T08:00:00+00:00",
        "borrowed_usd_snapshot": 1940622216.146181,
        "source_timestamp": "2026-08-03T07:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T09:00:00+00:00",
        "borrowed_usd_snapshot": 1940712984.2565594,
        "source_timestamp": "2026-08-03T08:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T10:00:00+00:00",
        "borrowed_usd_snapshot": 1940877700.4785566,
        "source_timestamp": "2026-08-03T09:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T11:00:00+00:00",
        "borrowed_usd_snapshot": 1940964363.3217978,
        "source_timestamp": "2026-08-03T10:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T12:00:00+00:00",
        "borrowed_usd_snapshot": 1940940187.6927602,
        "source_timestamp": "2026-08-03T11:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T13:00:00+00:00",
        "borrowed_usd_snapshot": 1941028910.303424,
        "source_timestamp": "2026-08-03T12:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T14:00:00+00:00",
        "borrowed_usd_snapshot": 1941598643.631781,
        "source_timestamp": "2026-08-03T13:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T15:00:00+00:00",
        "borrowed_usd_snapshot": 1941273933.908662,
        "source_timestamp": "2026-08-03T14:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T16:00:00+00:00",
        "borrowed_usd_snapshot": 1941200853.964076,
        "source_timestamp": "2026-08-03T15:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T17:00:00+00:00",
        "borrowed_usd_snapshot": 1941333309.6066835,
        "source_timestamp": "2026-08-03T16:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T18:00:00+00:00",
        "borrowed_usd_snapshot": 1942773077.9494011,
        "source_timestamp": "2026-08-03T17:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T19:00:00+00:00",
        "borrowed_usd_snapshot": 1942883636.2208726,
        "source_timestamp": "2026-08-03T18:58:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T20:00:00+00:00",
        "borrowed_usd_snapshot": 1942952146.544506,
        "source_timestamp": "2026-08-03T19:57:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T21:00:00+00:00",
        "borrowed_usd_snapshot": 1943306567.8938494,
        "source_timestamp": "2026-08-03T20:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T22:00:00+00:00",
        "borrowed_usd_snapshot": 1943296320.646719,
        "source_timestamp": "2026-08-03T21:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-03T23:00:00+00:00",
        "borrowed_usd_snapshot": 1943337770.8801045,
        "source_timestamp": "2026-08-03T22:56:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T00:00:00+00:00",
        "borrowed_usd_snapshot": 1943331020.4162447,
        "source_timestamp": "2026-08-03T23:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T01:00:00+00:00",
        "borrowed_usd_snapshot": 1951074153.9042745,
        "source_timestamp": "2026-08-04T00:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T02:00:00+00:00",
        "borrowed_usd_snapshot": 1939085594.0376527,
        "source_timestamp": "2026-08-04T01:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T03:00:00+00:00",
        "borrowed_usd_snapshot": 1952888311.2693546,
        "source_timestamp": "2026-08-04T02:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T04:00:00+00:00",
        "borrowed_usd_snapshot": 1952794786.8674748,
        "source_timestamp": "2026-08-04T03:54:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T05:00:00+00:00",
        "borrowed_usd_snapshot": 1952801098.6709685,
        "source_timestamp": "2026-08-04T04:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T06:00:00+00:00",
        "borrowed_usd_snapshot": 1964807846.8581014,
        "source_timestamp": "2026-08-04T05:55:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T07:00:00+00:00",
        "borrowed_usd_snapshot": 1964867012.5195723,
        "source_timestamp": "2026-08-04T06:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T08:00:00+00:00",
        "borrowed_usd_snapshot": 1964854376.1664093,
        "source_timestamp": "2026-08-04T07:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T09:00:00+00:00",
        "borrowed_usd_snapshot": 1960786155.2111228,
        "source_timestamp": "2026-08-04T08:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T10:00:00+00:00",
        "borrowed_usd_snapshot": 1960786453.7220445,
        "source_timestamp": "2026-08-04T09:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T11:00:00+00:00",
        "borrowed_usd_snapshot": 1960836324.6292481,
        "source_timestamp": "2026-08-04T10:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T12:00:00+00:00",
        "borrowed_usd_snapshot": 1961764755.0930724,
        "source_timestamp": "2026-08-04T11:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T13:00:00+00:00",
        "borrowed_usd_snapshot": 1961395182.7729158,
        "source_timestamp": "2026-08-04T12:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T14:00:00+00:00",
        "borrowed_usd_snapshot": 1961617070.1195734,
        "source_timestamp": "2026-08-04T13:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T15:00:00+00:00",
        "borrowed_usd_snapshot": 1961788144.8329682,
        "source_timestamp": "2026-08-04T14:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T16:00:00+00:00",
        "borrowed_usd_snapshot": 1960870018.809708,
        "source_timestamp": "2026-08-04T15:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T17:00:00+00:00",
        "borrowed_usd_snapshot": 1959450641.1419294,
        "source_timestamp": "2026-08-04T16:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T18:00:00+00:00",
        "borrowed_usd_snapshot": 1959458313.4434514,
        "source_timestamp": "2026-08-04T17:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T19:00:00+00:00",
        "borrowed_usd_snapshot": 1959741383.6639948,
        "source_timestamp": "2026-08-04T18:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T20:00:00+00:00",
        "borrowed_usd_snapshot": 1959921089.938211,
        "source_timestamp": "2026-08-04T19:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T21:00:00+00:00",
        "borrowed_usd_snapshot": 1959944290.2621646,
        "source_timestamp": "2026-08-04T20:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T22:00:00+00:00",
        "borrowed_usd_snapshot": 1959939766.066996,
        "source_timestamp": "2026-08-04T21:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-04T23:00:00+00:00",
        "borrowed_usd_snapshot": 1959749528.814863,
        "source_timestamp": "2026-08-04T22:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T00:00:00+00:00",
        "borrowed_usd_snapshot": 1959174168.231505,
        "source_timestamp": "2026-08-04T23:56:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T01:00:00+00:00",
        "borrowed_usd_snapshot": 1959188117.6851075,
        "source_timestamp": "2026-08-05T00:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T02:00:00+00:00",
        "borrowed_usd_snapshot": 1959187817.357929,
        "source_timestamp": "2026-08-05T01:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T03:00:00+00:00",
        "borrowed_usd_snapshot": 1959292700.3530464,
        "source_timestamp": "2026-08-05T02:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T04:00:00+00:00",
        "borrowed_usd_snapshot": 1959317161.060954,
        "source_timestamp": "2026-08-05T03:56:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T05:00:00+00:00",
        "borrowed_usd_snapshot": 1959317420.656567,
        "source_timestamp": "2026-08-05T04:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T06:00:00+00:00",
        "borrowed_usd_snapshot": 1959362882.328728,
        "source_timestamp": "2026-08-05T05:57:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T07:00:00+00:00",
        "borrowed_usd_snapshot": 1959368929.3662755,
        "source_timestamp": "2026-08-05T06:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T08:00:00+00:00",
        "borrowed_usd_snapshot": 1971233504.5401876,
        "source_timestamp": "2026-08-05T07:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T09:00:00+00:00",
        "borrowed_usd_snapshot": 1971230412.113093,
        "source_timestamp": "2026-08-05T08:58:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T10:00:00+00:00",
        "borrowed_usd_snapshot": 1981326528.4145293,
        "source_timestamp": "2026-08-05T09:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T11:00:00+00:00",
        "borrowed_usd_snapshot": 1989322095.8013318,
        "source_timestamp": "2026-08-05T10:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T12:00:00+00:00",
        "borrowed_usd_snapshot": 1981024617.4770298,
        "source_timestamp": "2026-08-05T11:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T13:00:00+00:00",
        "borrowed_usd_snapshot": 1981176719.661952,
        "source_timestamp": "2026-08-05T12:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T14:00:00+00:00",
        "borrowed_usd_snapshot": 1981645115.1957355,
        "source_timestamp": "2026-08-05T13:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T15:00:00+00:00",
        "borrowed_usd_snapshot": 1981860239.8083346,
        "source_timestamp": "2026-08-05T14:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T16:00:00+00:00",
        "borrowed_usd_snapshot": 1974800089.0811396,
        "source_timestamp": "2026-08-05T15:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T17:00:00+00:00",
        "borrowed_usd_snapshot": 1974971379.0743394,
        "source_timestamp": "2026-08-05T16:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T18:00:00+00:00",
        "borrowed_usd_snapshot": 1974823594.6015098,
        "source_timestamp": "2026-08-05T17:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T19:00:00+00:00",
        "borrowed_usd_snapshot": 1979848960.059325,
        "source_timestamp": "2026-08-05T18:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T20:00:00+00:00",
        "borrowed_usd_snapshot": 1979444459.9680014,
        "source_timestamp": "2026-08-05T19:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T21:00:00+00:00",
        "borrowed_usd_snapshot": 1979690853.6234841,
        "source_timestamp": "2026-08-05T20:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T22:00:00+00:00",
        "borrowed_usd_snapshot": 1979693491.9213212,
        "source_timestamp": "2026-08-05T21:57:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-05T23:00:00+00:00",
        "borrowed_usd_snapshot": 1978542349.99098,
        "source_timestamp": "2026-08-05T22:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T00:00:00+00:00",
        "borrowed_usd_snapshot": 1978545173.9714565,
        "source_timestamp": "2026-08-05T23:56:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T01:00:00+00:00",
        "borrowed_usd_snapshot": 1979005898.1299818,
        "source_timestamp": "2026-08-06T00:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T02:00:00+00:00",
        "borrowed_usd_snapshot": 1979899259.1922426,
        "source_timestamp": "2026-08-06T01:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T03:00:00+00:00",
        "borrowed_usd_snapshot": 1979025372.3675776,
        "source_timestamp": "2026-08-06T02:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T04:00:00+00:00",
        "borrowed_usd_snapshot": 1979050051.8797276,
        "source_timestamp": "2026-08-06T03:55:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T05:00:00+00:00",
        "borrowed_usd_snapshot": 1979066835.5688925,
        "source_timestamp": "2026-08-06T04:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T06:00:00+00:00",
        "borrowed_usd_snapshot": 1979879460.2533846,
        "source_timestamp": "2026-08-06T05:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T07:00:00+00:00",
        "borrowed_usd_snapshot": 1979804824.0179706,
        "source_timestamp": "2026-08-06T06:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T08:00:00+00:00",
        "borrowed_usd_snapshot": 1980008310.1667054,
        "source_timestamp": "2026-08-06T07:58:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T09:00:00+00:00",
        "borrowed_usd_snapshot": 1979966610.8407705,
        "source_timestamp": "2026-08-06T08:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T10:00:00+00:00",
        "borrowed_usd_snapshot": 1980032595.2323914,
        "source_timestamp": "2026-08-06T09:56:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T11:00:00+00:00",
        "borrowed_usd_snapshot": 1979582000.0051389,
        "source_timestamp": "2026-08-06T10:56:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T12:00:00+00:00",
        "borrowed_usd_snapshot": 1979985222.4206948,
        "source_timestamp": "2026-08-06T11:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T13:00:00+00:00",
        "borrowed_usd_snapshot": 1979993216.118927,
        "source_timestamp": "2026-08-06T12:57:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T14:00:00+00:00",
        "borrowed_usd_snapshot": 1979840341.3623853,
        "source_timestamp": "2026-08-06T13:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T15:00:00+00:00",
        "borrowed_usd_snapshot": 1979938186.0284798,
        "source_timestamp": "2026-08-06T14:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T16:00:00+00:00",
        "borrowed_usd_snapshot": 1986777335.00783,
        "source_timestamp": "2026-08-06T15:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T17:00:00+00:00",
        "borrowed_usd_snapshot": 1986455566.9701478,
        "source_timestamp": "2026-08-06T16:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T18:00:00+00:00",
        "borrowed_usd_snapshot": 1986412766.7842734,
        "source_timestamp": "2026-08-06T17:56:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T19:00:00+00:00",
        "borrowed_usd_snapshot": 1986412584.9769285,
        "source_timestamp": "2026-08-06T18:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T20:00:00+00:00",
        "borrowed_usd_snapshot": 1986417592.8828452,
        "source_timestamp": "2026-08-06T19:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T21:00:00+00:00",
        "borrowed_usd_snapshot": 1986497744.2796645,
        "source_timestamp": "2026-08-06T20:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T22:00:00+00:00",
        "borrowed_usd_snapshot": 1986500724.8078568,
        "source_timestamp": "2026-08-06T21:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-06T23:00:00+00:00",
        "borrowed_usd_snapshot": 1986037429.109098,
        "source_timestamp": "2026-08-06T22:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T00:00:00+00:00",
        "borrowed_usd_snapshot": 1985836737.0095296,
        "source_timestamp": "2026-08-06T23:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T01:00:00+00:00",
        "borrowed_usd_snapshot": 1985984035.3835008,
        "source_timestamp": "2026-08-07T00:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T02:00:00+00:00",
        "borrowed_usd_snapshot": 1985993633.5924332,
        "source_timestamp": "2026-08-07T01:56:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T03:00:00+00:00",
        "borrowed_usd_snapshot": 1986049802.1497238,
        "source_timestamp": "2026-08-07T02:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T04:00:00+00:00",
        "borrowed_usd_snapshot": 1986082790.7628043,
        "source_timestamp": "2026-08-07T03:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T05:00:00+00:00",
        "borrowed_usd_snapshot": 1986093829.5024755,
        "source_timestamp": "2026-08-07T04:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T06:00:00+00:00",
        "borrowed_usd_snapshot": 1986227848.7431872,
        "source_timestamp": "2026-08-07T05:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T07:00:00+00:00",
        "borrowed_usd_snapshot": 1986313343.3112605,
        "source_timestamp": "2026-08-07T06:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T08:00:00+00:00",
        "borrowed_usd_snapshot": 1985732991.5823274,
        "source_timestamp": "2026-08-07T07:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T09:00:00+00:00",
        "borrowed_usd_snapshot": 1985575432.8519256,
        "source_timestamp": "2026-08-07T08:58:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T10:00:00+00:00",
        "borrowed_usd_snapshot": 1987050442.123127,
        "source_timestamp": "2026-08-07T09:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T11:00:00+00:00",
        "borrowed_usd_snapshot": 1976981471.1003134,
        "source_timestamp": "2026-08-07T10:57:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T12:00:00+00:00",
        "borrowed_usd_snapshot": 1977034245.2077549,
        "source_timestamp": "2026-08-07T11:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T13:00:00+00:00",
        "borrowed_usd_snapshot": 1977229310.51669,
        "source_timestamp": "2026-08-07T12:59:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T14:00:00+00:00",
        "borrowed_usd_snapshot": 1977185966.1942768,
        "source_timestamp": "2026-08-07T13:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T15:00:00+00:00",
        "borrowed_usd_snapshot": 1975998989.9139302,
        "source_timestamp": "2026-08-07T14:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T16:00:00+00:00",
        "borrowed_usd_snapshot": 1976394438.2961082,
        "source_timestamp": "2026-08-07T15:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T17:00:00+00:00",
        "borrowed_usd_snapshot": 1976515175.5360873,
        "source_timestamp": "2026-08-07T16:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T18:00:00+00:00",
        "borrowed_usd_snapshot": 1981973164.9651036,
        "source_timestamp": "2026-08-07T17:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T19:00:00+00:00",
        "borrowed_usd_snapshot": 1982051460.3105834,
        "source_timestamp": "2026-08-07T18:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T20:00:00+00:00",
        "borrowed_usd_snapshot": 1982060445.8145478,
        "source_timestamp": "2026-08-07T19:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T21:00:00+00:00",
        "borrowed_usd_snapshot": 1983767206.6436553,
        "source_timestamp": "2026-08-07T20:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T22:00:00+00:00",
        "borrowed_usd_snapshot": 1983597572.4474263,
        "source_timestamp": "2026-08-07T21:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-07T23:00:00+00:00",
        "borrowed_usd_snapshot": 1983711436.9380875,
        "source_timestamp": "2026-08-07T22:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T00:00:00+00:00",
        "borrowed_usd_snapshot": 1983415496.7360232,
        "source_timestamp": "2026-08-07T23:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T01:00:00+00:00",
        "borrowed_usd_snapshot": 1985470253.9521575,
        "source_timestamp": "2026-08-08T00:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T02:00:00+00:00",
        "borrowed_usd_snapshot": 1986724813.857801,
        "source_timestamp": "2026-08-08T01:58:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T03:00:00+00:00",
        "borrowed_usd_snapshot": 1985808471.10878,
        "source_timestamp": "2026-08-08T02:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T04:00:00+00:00",
        "borrowed_usd_snapshot": 1985310779.9322503,
        "source_timestamp": "2026-08-08T03:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T05:00:00+00:00",
        "borrowed_usd_snapshot": 1985238847.1879394,
        "source_timestamp": "2026-08-08T04:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T06:00:00+00:00",
        "borrowed_usd_snapshot": 1985350185.825879,
        "source_timestamp": "2026-08-08T05:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T07:00:00+00:00",
        "borrowed_usd_snapshot": 1985248638.5936773,
        "source_timestamp": "2026-08-08T06:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T08:00:00+00:00",
        "borrowed_usd_snapshot": 1985260647.1214519,
        "source_timestamp": "2026-08-08T07:55:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T09:00:00+00:00",
        "borrowed_usd_snapshot": 1985279799.8397124,
        "source_timestamp": "2026-08-08T08:56:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T10:00:00+00:00",
        "borrowed_usd_snapshot": 1985255285.4414608,
        "source_timestamp": "2026-08-08T09:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T11:00:00+00:00",
        "borrowed_usd_snapshot": 1985204383.972904,
        "source_timestamp": "2026-08-08T10:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T12:00:00+00:00",
        "borrowed_usd_snapshot": 1985280339.5801911,
        "source_timestamp": "2026-08-08T11:58:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T13:00:00+00:00",
        "borrowed_usd_snapshot": 1985333278.7819703,
        "source_timestamp": "2026-08-08T12:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T14:00:00+00:00",
        "borrowed_usd_snapshot": 1985755011.0657532,
        "source_timestamp": "2026-08-08T13:58:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T15:00:00+00:00",
        "borrowed_usd_snapshot": 1985680660.3032386,
        "source_timestamp": "2026-08-08T14:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T16:00:00+00:00",
        "borrowed_usd_snapshot": 1985739836.267461,
        "source_timestamp": "2026-08-08T15:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T17:00:00+00:00",
        "borrowed_usd_snapshot": 1985769698.5592892,
        "source_timestamp": "2026-08-08T16:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T18:00:00+00:00",
        "borrowed_usd_snapshot": 1985905487.6791437,
        "source_timestamp": "2026-08-08T17:59:35+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T19:00:00+00:00",
        "borrowed_usd_snapshot": 1985921466.1695487,
        "source_timestamp": "2026-08-08T18:59:11+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T20:00:00+00:00",
        "borrowed_usd_snapshot": 1985944065.890237,
        "source_timestamp": "2026-08-08T19:57:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T21:00:00+00:00",
        "borrowed_usd_snapshot": 1986043616.5026753,
        "source_timestamp": "2026-08-08T20:58:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T22:00:00+00:00",
        "borrowed_usd_snapshot": 1985991815.7872097,
        "source_timestamp": "2026-08-08T21:54:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-08T23:00:00+00:00",
        "borrowed_usd_snapshot": 1986117367.7786493,
        "source_timestamp": "2026-08-08T22:55:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T00:00:00+00:00",
        "borrowed_usd_snapshot": 1985969937.3793864,
        "source_timestamp": "2026-08-08T23:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T01:00:00+00:00",
        "borrowed_usd_snapshot": 1984961885.1565611,
        "source_timestamp": "2026-08-09T00:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T02:00:00+00:00",
        "borrowed_usd_snapshot": 1984470457.7004395,
        "source_timestamp": "2026-08-09T01:53:23+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T03:00:00+00:00",
        "borrowed_usd_snapshot": 1984479959.1172082,
        "source_timestamp": "2026-08-09T02:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T04:00:00+00:00",
        "borrowed_usd_snapshot": 1984422859.8680687,
        "source_timestamp": "2026-08-09T03:59:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T05:00:00+00:00",
        "borrowed_usd_snapshot": 1984431970.7943728,
        "source_timestamp": "2026-08-09T04:59:47+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T06:00:00+00:00",
        "borrowed_usd_snapshot": 1984444942.6525013,
        "source_timestamp": "2026-08-09T05:57:59+00:00",
        "is_carried": false
      },
      {
        "asset": "USDC",
        "hour": "2026-08-09T07:00:00+00:00",
        "borrowed_usd_snapshot": 1984489689.6280525,
        "source_timestamp": "2026-08-09T06:58:11+00:00",
        "is_carried": false
      }
    ],
    "truncated": true,
    "total_rows": 201
  }
}
```

## A0013

```json
{
  "question": "Giá trị dư nợ trung bình theo giờ của USDe trong tháng 2026-08 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 521264061.9902388
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 521264061.9902388
        }
      ]
    }
  ],
  "system_answer": "Giá trị dư nợ trung bình theo giờ của USDe trong tháng 2026-08 là 521,264,061.99 USD, dựa trên dữ liệu trong bộ dữ liệu hiện có.",
  "system_claims": [
    {
      "text": "Giá trị dư nợ trung bình theo giờ của USDe từ 2026-08-01T00:00:00Z đến 2026-09-01T00:00:00Z là 521,264,061.99 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 521264061.99,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_borrowed_usd"
      }
    },
    {
      "text": "Dữ liệu USDe trong bộ dữ liệu hiện có bao gồm khoảng thời gian từ 2024-06-06T15:00:00Z đến 2026-09-15T07:00:00Z với 19,937 hàng quan sát theo giờ",
      "citations": [
        "availability"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 3.877176256709714
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 2.64150479075121
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 2.3550636923150394
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 2.0010949767733552
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.4521799036801282
    }
  ],
  "sql": "SELECT AVG(borrowed_usd) AS avg_borrowed_usd FROM market_hourly WHERE asset = 'USDe' AND hour >= '2026-08-01T00:00:00Z' AND hour < '2026-09-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_borrowed_usd"
    ],
    "rows": [
      {
        "avg_borrowed_usd": 521264061.9902388
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0014

```json
{
  "question": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1997694271.598428
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1997694271.598428
        }
      ]
    }
  ],
  "system_answer": "Giá trị tài sản USDC được cung cấp lúc 00:00 UTC ngày 2026-08-15 là 1,997,694,271.60 USD, theo dữ liệu trong bộ dữ liệu hiện có.\n\nChưa thể xác minh đầy đủ: Requested hour 2026-08-15T00:00:00Z is within the observed availability window for USDC (end_utc: 2026-09-15T07:00:00+00:00), but the question asks for a snapshot at a specific UTC hour. The SQL query correctly filters for this hour and returned 1 row with supplied_usd = 1997694271.598428 USD. However, this is a future date relative to typical analysis contexts. Verify that 2026-08-15 data is intentional and that the loaded dataset actually contains observations for this date.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC ngày 2026-08-15 là 1,997,694,271.60 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1997694271.6,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "supplied_usd_snapshot"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, supplied_usd AS supplied_usd_snapshot FROM market_hourly WHERE asset = 'USDC' AND hour = '2026-08-15T00:00:00Z' LIMIT 1",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "supplied_usd_snapshot"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "supplied_usd_snapshot": 1997694271.598428
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0015

```json
{
  "question": "Tài sản thế chấp có vai trò gì khi vay trên Aave V3? Hãy trả lời ngắn gọn và dẫn nguồn.",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Tài sản thế chấp trên Aave V3 có vai trò then chốt: (1) Cho phép vay: Người dùng phải cung cấp tài sản thế chấp để truy cập thanh khoản và vay token [DOC_BORROW_000]. (2) Xác định khả năng vay: Giá trị thế chấp được sử dụng để tính Health Factor = (Tổng giá trị thế chấp × Trọng số Ngưỡng thanh lý trung bình) / Tổng giá trị vay [DOC_LIQ_000]. (3) Bảo vệ chống thanh lý: Phải duy trì Health Factor > 1 để tránh thanh lý; nếu Health Factor < 1, vị thế có nguy cơ bị thanh lý [DOC_LIQ_000]. (4) Quản lý rủi ro: Người vay phải giám sát thường xuyên và có thể cung cấp thêm thế chấp hoặc trả lại khoản vay để duy trì sự an toàn [DOC_BORROW_000].",
  "system_claims": [
    {
      "text": "Tài sản thế chấp cho phép người dùng truy cập thanh khoản và vay token từ Aave Protocol",
      "citations": [
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Health Factor được tính bằng công thức: (Tổng giá trị thế chấp × Trọng số Ngưỡng thanh lý trung bình) / Tổng giá trị vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Health Factor dưới 1 báo hiệu rủi ro thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Người vay phải duy trì Health Factor trên 1 để tránh thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Để cải thiện Health Factor, người vay có thể cung cấp thêm thế chấp hoặc trả lại một phần khoản vay",
      "citations": [
        "DOC_BORROW_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.8990474021112234
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.854258546537117
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.793707409879604
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.636978214687525
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.6683151106511598
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0016

```json
{
  "question": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Dư nợ là số dư tại thời điểm; không coi là tổng số tiền vay mới trong tháng."
    ],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1993676848.0321777
        }
      ]
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là $1,993,676,848.03 USD [SQL1]. Không thể coi đây là tổng tiền vay mới trong tháng vì ba lý do: (1) Giá trị này là **snapshot của tổng dư nợ hiện tại** (stock), không phải luồng tiền vay mới (flow) trong tháng [DOC_SUPPLY_000]. (2) Dư nợ này bao gồm cả tiền vay từ các tháng trước đó cộng với lãi suất tích lũy động theo thời gian [DOC_SUPPLY_000, DOC_BORROW_000]. (3) Lãi suất trên tiền vay được tính động dựa trên tỷ lệ sử dụng vay (borrow utilization rate) và các tham số quản trị, không phải là tiền vay mới [DOC_SUPPLY_000, DOC_BORROW_000]. Để xác định tiền vay mới trong tháng, cần so sánh snapshot này với dữ liệu từ đầu tháng 8 và loại trừ phần lãi suất tích lũy.\n\nChưa thể xác minh đầy đủ: Requested timestamp 2026-08-15T00:00:00Z is beyond the observed data availability for USDC market_hourly (end_utc: 2026-09-15T07:00:00Z). While the date falls within the availability window, the source_timestamp 2026-08-14T23:58:35Z is 2 minutes before the grid hour, indicating a carried observation. The query returns a single snapshot, but this is a stock metric (borrowed_usd) at a future date relative to typical analysis. Verify that 2026-08-15 data collection is complete and not partial.; The SQL correctly retrieves borrowed_usd as a stock snapshot at 2026-08-15T00:00:00Z (not summed over time). However, the question asks 'Có thể coi đây là tổng tiền vay mới trong tháng không?' (Can this be considered total new borrowing in the month?). A stock balance at a single point in time cannot represent monthly new borrowing (a flow metric). The snapshot shows outstanding debt, not new borrowing volume. This is a semantic mismatch between the retrieved metric type and the second part of the question.; The question conflates two distinct concepts: (1) borrowed_usd at 2026-08-15T00:00:00Z is a stock (outstanding debt balance), and (2) 'tổng tiền vay mới trong tháng' (total new borrowing in the month) is a flow (cumulative borrow events in August 2026). The SQL metric is correct for the first part but cannot answer the second part. To measure new borrowing, liquidation_events or a borrow transaction table would be required, not a stock balance snapshot.",
  "system_claims": [
    {
      "text": "Dư nợ USDC lúc 00:00 UTC 2026-08-15 là $1,993,676,848.03 USD trong bộ dữ liệu hiện có",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1993676848.03,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd_snapshot"
      }
    },
    {
      "text": "Giá trị dư nợ là một snapshot của tổng dư nợ hiện tại (stock), không phải luồng tiền vay mới (flow)",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Dư nợ bao gồm tiền vay từ các tháng trước cộng với lãi suất tích lũy động theo thời gian",
      "citations": [
        "DOC_SUPPLY_000",
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Lãi suất trên tiền vay được tính động dựa trên tỷ lệ sử dụng vay (borrow utilization rate) và các tham số quản trị",
      "citations": [
        "DOC_SUPPLY_000",
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Để xác định tiền vay mới trong tháng cần so sánh snapshot đầu tháng với snapshot cuối tháng và loại trừ phần lãi suất tích lũy",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 3.08011155937312
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.7560104224122217
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.503625279456373
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.5831523488731407
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 0.3951365249869238
    }
  ],
  "sql": "SELECT asset, hour, borrowed_usd AS borrowed_usd_snapshot, source_timestamp, is_carried FROM market_hourly WHERE asset = 'USDC' AND hour >= '2026-08-15T00:00:00Z' AND hour < '2026-08-15T01:00:00Z' ORDER BY hour;",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd_snapshot",
      "source_timestamp",
      "is_carried"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "borrowed_usd_snapshot": 1993676848.0321777,
        "source_timestamp": "2026-08-14T23:58:35+00:00",
        "is_carried": false
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0017

```json
{
  "question": "Giá trị tài sản cung cấp trung bình theo giờ của USDe trong tháng 2026-08 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 749295298.141774
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 749295298.141774
        }
      ]
    }
  ],
  "system_answer": "Giá trị tài sản cung cấp trung bình theo giờ của USDe trong tháng 2026-08 là 749,295,298.14 USD, dựa trên bộ dữ liệu hiện có từ bảng market_hourly.\n\nChưa thể xác minh đầy đủ: USDe data availability ends 2026-09-15T07:00:00Z but query requests interval [2026-08-01T00:00:00Z, 2026-09-01T00:00:00Z). USDe first observed 2024-06-06T15:00:00Z. The requested August 2026 interval is within observed bounds (2024-06-06 to 2026-09-15), so data should exist if collected. However, verify that August 2026 hourly observations for USDe are actually present in market_hourly; availability shows only 19937 total rows for USDe across ~2 years.; Truy vấn yêu cầu tài liệu nhưng danh sách documents trống. Retrieval_runs ghi lại 5 document_ids được trả về (DOC_SUPPLY_000, DOC_SUPPLY_001, DOC_BORROW_000, DOC_BORROW_001, DOC_LIQ_000) nhưng không có nội dung tài liệu được cung cấp để xác minh kết quả SQL.; Dữ liệu USDe có sẵn từ 2024-06-06T15:00:00Z đến 2026-09-15T07:00:00Z (19,937 hàng quan sát). Khoảng thời gian yêu cầu 2026-08-01 đến 2026-09-01 nằm trong phạm vi này, nhưng availability chỉ báo cáo 'observed timestamp bounds, not guarantees of gap-free coverage'. Không thể xác nhận rằng tất cả 744 giờ trong tháng 8 năm 2026 đều có dữ liệu hoặc không có khoảng trống.; Câu trả lời khẳng định giá trị dựa trên 'bộ dữ liệu hiện có' nhưng không báo cáo số lượng hàng thực tế được trả về từ truy vấn SQL cho khoảng thời gian 2026-08-01 đến 2026-09-01. Cần COUNT(*) để xác minh rằng trung bình được tính từ bao nhiêu quan sát.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp trung bình theo giờ của USDe trong khoảng thời gian từ 2026-08-01 đến 2026-09-01 là 749,295,298.14 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 749295298.14,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_supplied_usd"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT AVG(supplied_usd) AS avg_supplied_usd FROM market_hourly WHERE asset = 'USDe' AND hour >= '2026-08-01T00:00:00Z' AND hour < '2026-09-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_supplied_usd"
    ],
    "rows": [
      {
        "avg_supplied_usd": 749295298.141774
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0018

```json
{
  "question": "Dư nợ WETH lúc 00:00 UTC ngày 2025-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 10023005896.239573
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2025-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 10023005896.239573
        }
      ]
    }
  ],
  "system_answer": "Dư nợ WETH lúc 00:00 UTC ngày 2025-08-15 là 10,023,005,896.24 USD, theo bộ dữ liệu hiện có từ bảng market_hourly.\n\nChưa thể xác minh đầy đủ: Requested date 2025-08-15 is beyond the observed data availability for market_hourly WETH (end_utc: 2026-09-15T07:00:00+00:00 shows data extends to September 2026, but the question asks for August 2025 which is in the past relative to the availability window start 2023-01-27). However, the availability end date 2026-09-15T07:00:00+00:00 indicates data collection extends to mid-September 2026, making 2025-08-15 well within observed bounds. The SQL result returned 1 row with borrowed_usd=10023005896.239573, confirming the data point exists.; Requirements specify aggregation='snapshot' and grain='hour', but the time range [2025-08-15T00:00:00Z, 2025-08-15T01:00:00Z) spans one full hour. A snapshot should represent a single point-in-time value (the state at 2025-08-15T00:00:00Z), not an interval. The SQL correctly filters to hour='2025-08-15T00:00:00Z' and returns one row, which is the correct snapshot semantics for a stock metric (borrowed_usd must not be summed or averaged over the hour). The result is semantically correct: it reports the debt balance at the requested UTC hour.; Ngày 2025-08-15 nằm ngoài phạm vi dữ liệu quan sát được. Dữ liệu WETH trong market_hourly chỉ có từ 2023-01-27T08:00:00Z đến 2026-09-15T07:00:00Z. Ngày 2025-08-15 là trong tương lai so với ngày thu thập dữ liệu cuối cùng (2026-09-15).; SQL trả về kết quả cho 2025-08-15T00:00:00Z nhưng availability cho WETH kết thúc tại 2026-09-15T07:00:00Z. Mặc dù 2025-08-15 nằm trong khoảng này về mặt lý thuyết, nhưng đây là dữ liệu lịch sử từ quá khứ (so với ngày thu thập 2026-09-15). Câu trả lời không làm rõ rằng đây là dữ liệu lịch sử, không phải dữ liệu thời gian thực.; Câu trả lời không ghi chú rằng giá trị 10,023,005,896.24 USD là một quan sát lịch sử từ tháng 8 năm 2025, không phải dữ liệu hiện tại. Người dùng có thể hiểu nhầm đây là dữ liệu thời gian thực.",
  "system_claims": [
    {
      "text": "Dư nợ WETH (borrowed_usd) lúc 00:00 UTC ngày 2025-08-15 là 10,023,005,896.24 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 10023005896.24,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, borrowed_usd FROM market_hourly WHERE asset = 'WETH' AND hour >= '2025-08-15T00:00:00Z' AND hour < '2025-08-15T01:00:00Z' ORDER BY hour",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd"
    ],
    "rows": [
      {
        "asset": "WETH",
        "hour": "2025-08-15T00:00:00+00:00",
        "borrowed_usd": 10023005896.239573
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0019

```json
{
  "question": "Tài sản thế chấp có vai trò gì khi vay trên Aave V3?",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Tài sản thế chấp đóng vai trò then chốt trong vay trên Aave V3. Thứ nhất, người vay phải cung cấp đủ tài sản thế chấp để có thể vay được token. Thứ hai, giá trị của tài sản thế chấp được sử dụng để tính toán Health Factor, một chỉ số quan trọng đo lường độ an toàn của vị thế vay: Health Factor = (Tổng Giá Trị Tài Sản Thế Chấp × Trung Bình Gia Quyền Ngưỡng Thanh Lý) / Tổng Giá Trị Vay. Khi Health Factor giảm dưới 1, vị thế vay sẽ bị rủi ro thanh lý. Thứ ba, mỗi tài sản thế chấp có một Ngưỡng Thanh Lý (Liquidation Threshold) do Aave Governance xác định, quy định phần trăm tối đa của giá trị tài sản có thể được vay. Ví dụ, nếu cung cấp 10.000 USD ETH với ngưỡng thanh lý 80%, chỉ có thể vay tối đa 8.000 USD. Cuối cùng, nếu Health Factor rơi dưới 1, tài sản thế chấp sẽ bị thanh lý để trả nợ, và người thanh lý sẽ nhận được giá trị tương đương cộng với phí thanh lý từ tài sản thế chấp của người vay.",
  "system_claims": [
    {
      "text": "Health Factor được tính bằng công thức: (Tổng Giá Trị Tài Sản Thế Chấp × Trung Bình Gia Quyền Ngưỡng Thanh Lý) / Tổng Giá Trị Vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Health Factor dưới 1 báo hiệu rủi ro thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Ngưỡng Thanh Lý được Aave Governance xác định cho mỗi tài sản thế chấp và quy định phần trăm tối đa của giá trị có thể được vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Ví dụ: cung cấp 10.000 USD ETH với ngưỡng thanh lý 80% và vay 6.000 USD GHO sẽ có Health Factor là 1.333",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Người vay phải duy trì tài sản thế chấp đủ để bao phủ số tiền vay, nếu không sẽ bị thanh lý",
      "citations": [
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Khi thanh lý xảy ra, người thanh lý trả nợ thay cho người vay và nhận giá trị tương đương cộng với phí thanh lý từ tài sản thế chấp",
      "citations": [
        "DOC_LIQ_001"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.8990474021112234
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.854258546537117
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.793707409879604
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.636978214687525
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.6683151106511598
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0020

```json
{
  "question": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Dư nợ là số dư tại thời điểm; không coi là tổng số tiền vay mới trong tháng."
    ],
    "sql_result": [
      {
        "value": 3042883324.3152447
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
      "rows": [
        {
          "value": 3042883324.3152447
        }
      ]
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là 3,042,883,324.32 USD [SQL1]. Không thể coi đây là tổng tiền vay mới trong tháng vì lý do sau: (1) Giá trị này là một 'snapshot' - tồn kho nợ tại một thời điểm cụ thể, không phải luồng vay mới. Theo tài liệu, 'borrowed_usd' là 'USD debt stock at hour, never SUM over time' [dictionary], nghĩa là nó đo lường tổng dư nợ hiện tại, không phải vay mới. (2) Để tính tiền vay mới trong tháng, cần so sánh dư nợ tại đầu tháng với cuối tháng hoặc theo dõi các sự kiện vay riêng lẻ, không phải dùng một snapshot đơn lẻ. (3) Dư nợ này bao gồm cả lãi suất tích lũy - tài liệu nêu rõ 'interest on the borrowed tokens begins to accrue immediately' [DOC_BORROW_001], do đó phần tăng có thể do lãi suất, không phải vay mới.\n\nChưa thể xác minh đầy đủ: Question asks 'Có thể coi đây là tổng tiền vay mới trong tháng không?' (Can this be considered total new borrowing in the month?). This conflates a stock snapshot (borrowed_usd at 2026-07-15T00:00:00Z = 3,042,883,324 USD) with a flow metric (new borrowing during July 2026). Dictionary explicitly states 'borrowed_usd: USD debt stock at hour, never SUM over time'. A single hourly snapshot cannot represent monthly new borrowing flow. The SQL correctly retrieves a stock; the question's second part requests flow semantics that require different data (e.g., borrow events or daily deltas).; Requirements specify 'start': '2026-07-15T00:00:00Z', 'end': '2026-07-15T01:00:00Z' with 'aggregation': 'snapshot' and 'grain': 'hour'. SQL correctly queries a single hour (2026-07-15T00:00:00Z). However, the end time 2026-07-15T01:00:00Z suggests a one-hour interval, which contradicts snapshot semantics. For a snapshot, only the start hour is needed; the end bound is redundant. This is a requirements specification inconsistency, not a SQL error, but clarifies that the result is a point-in-time stock, not an interval aggregate.; Missing or invalid citation ID; Answer cites '[dictionary]' as evidence for 'borrowed_usd' definition, but the dictionary provided defines market_hourly.borrowed_usd as 'USD debt stock at hour, never SUM over time'—this supports the claim that it is a stock metric, not a flow. However, the citation format '[dictionary]' is imprecise; the actual source is the supplied data dictionary, not a document.; Answer states 'Để tính tiền vay mới trong tháng, cần so sánh dư nợ tại các thời điểm khác nhau hoặc theo dõi các sự kiện vay riêng lẻ' but cites only DOC_BORROW_000 and DOC_BORROW_001. These documents describe the borrowing process and interest accrual mechanics but do not explicitly explain why a single snapshot cannot represent monthly new borrowing or how to calculate new borrowing from stock differences. The claim is logically sound (stock ≠ flow) but the cited documents do not directly support the methodological statement.; The question asks 'Có thể coi đây là tổng tiền vay mới trong tháng không?' (Can this be considered total new borrowing in the month?). The answer correctly states 'No' and explains why, but does not provide the actual monthly new borrowing figure or indicate whether such data is available in the dataset. The answer addresses the conceptual distinction but leaves the second part of the question (what IS the new borrowing) unanswered.; Answer cites 'DOC_BORROW_001' for the claim about interest accrual. DOC_BORROW_001 does state 'interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate.' This is accurate and well-supported.; SQL result shows weth_borrowed_usd_at_snapshot = 3042883324.3152447. Answer rounds to 3,042,883,324.32 USD. Rounding to 2 decimal places (cents) is appropriate for USD currency display.",
  "system_claims": [
    {
      "text": "Dư nợ WETH lúc 00:00 UTC 2026-07-15 là 3,042,883,324.32 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 3042883324.32,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "weth_borrowed_usd_at_snapshot"
      }
    },
    {
      "text": "borrowed_usd là tồn kho nợ (debt stock) tại một giờ cụ thể, không bao giờ được tính tổng theo thời gian",
      "citations": [
        "dictionary"
      ]
    },
    {
      "text": "Lãi suất trên các token được vay bắt đầu tích lũy ngay lập tức và được điều chỉnh động dựa trên tỷ lệ sử dụng vay",
      "citations": [
        "DOC_BORROW_001"
      ]
    },
    {
      "text": "Để tính tiền vay mới trong tháng, cần so sánh dư nợ tại các thời điểm khác nhau hoặc theo dõi các sự kiện vay riêng lẻ, không phải dùng một snapshot đơn lẻ",
      "citations": [
        "DOC_BORROW_000",
        "DOC_BORROW_001"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 3.5076459907350617
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.6444574664132487
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.4970938941352956
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 0.9686956651770642
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.807323076503812
    }
  ],
  "sql": "SELECT asset, hour, borrowed_usd AS weth_borrowed_usd_at_snapshot, is_carried, source_timestamp FROM market_hourly WHERE asset = 'WETH' AND hour = '2026-07-15T00:00:00Z' LIMIT 1;",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "weth_borrowed_usd_at_snapshot",
      "is_carried",
      "source_timestamp"
    ],
    "rows": [
      {
        "asset": "WETH",
        "hour": "2026-07-15T00:00:00+00:00",
        "weth_borrowed_usd_at_snapshot": 3042883324.3152447,
        "is_carried": false,
        "source_timestamp": "2026-07-14T23:59:59+00:00"
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0021

```json
{
  "question": "Giá trị tài sản cung cấp trung bình theo giờ của DAI trong tháng 2026-06 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 118343676.63059068
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-06-01' AND hour < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": 118343676.63059068
        }
      ]
    }
  ],
  "system_answer": "Giá trị tài sản cung cấp trung bình theo giờ của DAI trong tháng 2026-06 là 118,343,676.63 USD, dựa trên dữ liệu từ bộ dữ liệu hiện có (market_hourly). Khoảng thời gian yêu cầu từ 2026-06-01 đến 2026-07-01 nằm trong phạm vi quan sát được của DAI (2023-01-27 đến 2026-09-15).\n\nChưa thể xác minh đầy đủ: Khoảng thời gian yêu cầu [2026-06-01, 2026-07-01) nằm ngoài phạm vi dữ liệu quan sát được. DAI có dữ liệu đến 2026-09-15T06:00:00Z, nhưng tháng 6/2026 là tương lai so với ngày hiện tại. Câu trả lời báo cáo giá trị từ SQL nhưng không xác nhận rằng dữ liệu thực sự tồn tại cho toàn bộ khoảng thời gian này.; Câu trả lời khẳng định 'Khoảng thời gian yêu cầu từ 2026-06-01 đến 2026-07-01 nằm trong phạm vi quan sát được của DAI (2023-01-27 đến 2026-09-15)' nhưng điều này không được hỗ trợ. Availability cho DAI kết thúc tại 2026-09-15T06:00:00Z, và tháng 6/2026 nằm trong khoảng này. Tuy nhiên, không có bằng chứng từ tài liệu hoặc metadata rằng dữ liệu được thu thập cho tháng 6/2026 hay bất kỳ ngày cụ thể nào trong tương lai.; Không có tài liệu được truy xuất (documents: []). Retrieval_runs cho thấy truy vấn được thực hiện nhưng không trả về tài liệu hỗ trợ. Không thể xác minh tính hợp lệ của dữ liệu 2026-06 từ các nguồn Aave V3.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp trung bình theo giờ của DAI trong tháng 2026-06 là 118,343,676.63 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 118343676.63,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "avg_supplied_usd_dai_june_2026"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT AVG(\"supplied_usd\") AS avg_supplied_usd_dai_june_2026 FROM \"market_hourly\" WHERE \"asset\" = 'DAI' AND \"hour\" >= '2026-06-01T00:00:00Z' AND \"hour\" < '2026-07-01T00:00:00Z'",
  "query_result": {
    "columns": [
      "avg_supplied_usd_dai_june_2026"
    ],
    "rows": [
      {
        "avg_supplied_usd_dai_june_2026": 118343676.63059068
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0022

```json
{
  "question": "Dư nợ USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1993676848.0321777
        }
      ]
    }
  ],
  "system_answer": "Dư nợ USDC tại 2026-08-15T00:00:00 UTC trong bộ dữ liệu hiện có là 1,993,676,848.03 USD. Tuy nhiên, giá trị này được mang (carried) từ một quan sát nguồn tại 2026-08-14T23:58:35 UTC (khoảng 1 phút 25 giây trước grid hour). Cờ is_carried = false cho biết quan sát này đã được sử dụng ở một grid hour trước đó, không phải là quan sát mới tại grid hour 2026-08-15T00:00:00Z. Do đó, giá trị này không nhất thiết phản ánh chính xác dư nợ USDC tại thời điểm 00:00 UTC ngày 2026-08-15.\n\nChưa thể xác minh đầy đủ: Numeric claim unit differs from requested unit; Claim value does not match executed result cell; Answer claims is_carried = false means 'observation already used at earlier grid hour', but dictionary defines is_carried as a boolean flag indicating whether source observation was carried forward. The value false indicates this IS a fresh observation at this grid hour, not a reused one. Answer inverts the flag semantics.; Answer states 'giá trị này không nhất thiết phản ánh chính xác dư nợ USDC' based on source_timestamp being 1m25s before grid hour. However: (1) is_carried=false confirms this is a new observation at grid hour 2026-08-15T00:00:00Z, not carried from earlier; (2) source_timestamp 2026-08-14T23:58:35Z is within the same UTC hour and represents the actual on-chain observation time; (3) market_hourly grain is 'one asset per UTC hour' with hour as grid timestamp—source_timestamp variance within an hour is normal and does not invalidate the snapshot. The claim of inaccuracy lacks evidentiary support.; Numeric value 1,993,676,848.03 USD is correctly extracted from borrowed_usd_snapshot column, row 0, and properly cited to SQL1.",
  "system_claims": [
    {
      "text": "Dư nợ USDC được báo cáo tại grid hour 2026-08-15T00:00:00 UTC là 1,993,676,848.03 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1993676848.03,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "borrowed_usd_snapshot"
      }
    },
    {
      "text": "Giá trị này được mang từ quan sát nguồn tại 2026-08-14T23:58:35 UTC, không phải quan sát mới tại grid hour 2026-08-15T00:00:00Z",
      "citations": [
        "SQL1"
      ]
    },
    {
      "text": "Cờ is_carried = false cho biết quan sát này đã được sử dụng ở một grid hour trước đó",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 0,
        "unit": "other",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "is_carried"
      }
    }
  ],
  "documents": [],
  "sql": "SELECT asset, hour, borrowed_usd AS borrowed_usd_snapshot, source_timestamp, is_carried FROM market_hourly WHERE asset = 'USDC' AND hour >= '2026-08-15T00:00:00Z' AND hour < '2026-08-15T01:00:00Z' ORDER BY hour",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "borrowed_usd_snapshot",
      "source_timestamp",
      "is_carried"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "borrowed_usd_snapshot": 1993676848.0321777,
        "source_timestamp": "2026-08-14T23:58:35+00:00",
        "is_carried": false
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```

## A0023

```json
{
  "question": "Tài sản thế chấp có vai trò gì khi vay trên Aave V3?",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health"
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read"
    }
  ],
  "system_answer": "Tài sản thế chấp đóng vai trò then chốt trong vay trên Aave V3. Thứ nhất, người vay phải cung cấp đủ tài sản thế chấp để có thể vay được token. Thứ hai, giá trị của tài sản thế chấp được sử dụng để tính toán Health Factor, một chỉ số quan trọng đo lường độ an toàn của vị thế vay: Health Factor = (Tổng Giá Trị Tài Sản Thế Chấp × Trung Bình Gia Quyền Ngưỡng Thanh Lý) / Tổng Giá Trị Vay. Khi Health Factor giảm dưới 1, vị thế vay sẽ bị rủi ro thanh lý. Thứ ba, mỗi tài sản thế chấp có một Ngưỡng Thanh Lý (Liquidation Threshold) do Aave Governance xác định, quy định phần trăm tối đa của giá trị tài sản có thể được vay. Ví dụ, nếu cung cấp 10.000 USD ETH với ngưỡng thanh lý 80%, chỉ có thể vay tối đa 8.000 USD. Cuối cùng, nếu Health Factor rơi dưới 1, tài sản thế chấp sẽ bị thanh lý để trả nợ, và người thanh lý sẽ nhận được giá trị tương đương cộng với phí thanh lý từ tài sản thế chấp của người vay.",
  "system_claims": [
    {
      "text": "Health Factor được tính bằng công thức: (Tổng Giá Trị Tài Sản Thế Chấp × Trung Bình Gia Quyền Ngưỡng Thanh Lý) / Tổng Giá Trị Vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Health Factor dưới 1 báo hiệu rủi ro thanh lý",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Ngưỡng Thanh Lý được Aave Governance xác định cho mỗi tài sản thế chấp và quy định phần trăm tối đa của giá trị có thể được vay",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Ví dụ: cung cấp 10.000 USD ETH với ngưỡng thanh lý 80% và vay 6.000 USD GHO sẽ có Health Factor là 1.333",
      "citations": [
        "DOC_LIQ_000"
      ]
    },
    {
      "text": "Người vay phải duy trì tài sản thế chấp đủ để bao phủ số tiền vay, nếu không sẽ bị thanh lý",
      "citations": [
        "DOC_BORROW_000"
      ]
    },
    {
      "text": "Khi thanh lý xảy ra, người thanh lý trả nợ thay cho người vay và nhận giá trị tương đương cộng với phí thanh lý từ tài sản thế chấp",
      "citations": [
        "DOC_LIQ_001"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.8990474021112234
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.854258546537117
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.793707409879604
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.636978214687525
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.6683151106511598
    }
  ],
  "sql": "",
  "query_result": null
}
```

## A0024

```json
{
  "question": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Có thể coi đây là lợi nhuận người cung cấp đã thu được không? Vì sao?",
  "reference_answer": {
    "required_points": [
      "Giá trị cung cấp là số dư, không phải lợi nhuận thu được."
    ],
    "sql_result": [
      {
        "value": 1997694271.598428
      }
    ],
    "limitation": ""
  },
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1997694271.598428
        }
      ]
    },
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can"
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "system_answer": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC 2026-08-15 là $1,997,694,271.60 USD trong bộ dữ liệu hiện có [SQL1]. Tuy nhiên, không thể coi đây là lợi nhuận người cung cấp đã thu được vì lý do sau:\n\n1. Giá trị $1,997,694,271.60 là tổng giá trị USD của tất cả USDC được cung cấp tại thời điểm đó, không phải lợi nhuận.\n\n2. Theo tài liệu, lợi nhuận được tạo ra thông qua cơ chế tích lũy lãi suất động: 'Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time' [DOC_SUPPLY_000].\n\n3. Lợi nhuận là phần tăng thêm trên số tiền gốc được cung cấp, không phải toàn bộ giá trị cung cấp. Để xác định lợi nhuận thực tế, cần so sánh giá trị tại hai thời điểm khác nhau hoặc biết số tiền gốc ban đầu.\n\nChưa thể xác minh đầy đủ: Requested interval 2026-08-15T00:00:00Z to 2026-08-15T01:00:00Z is beyond observed data bounds. market_hourly USDC data ends at 2026-09-15T07:00:00Z, but the question requests a snapshot at 2026-08-15T00:00Z. The SQL result shows one row with source_timestamp 2026-08-14T23:58:35Z (2 minutes before the requested hour), which is within observed bounds. However, the question's date 2026-08-15 appears to be in the future relative to typical current dates. Verify whether this is an intentional historical query within the dataset or a data entry error.; The answer correctly interprets supplied_usd as a stock value (total USD value of USDC supplied at a point in time), not cumulative earnings. The SQL aggregation is appropriate: a single snapshot at hour 2026-08-15T00:00:00Z with value $1,997,694,271.60 USD.; The answer correctly refuses to characterize the supplied_usd snapshot as 'lợi nhuận người cung cấp đã thu được' (provider profit earned). The supplied_usd metric represents the total value of supplied tokens in USD at a moment, not accumulated interest or profit. The documents confirm that interest accrues dynamically over time (DOC_SUPPLY_000: 'Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate'), but no document provides a method to extract the interest component from the total supplied value or to calculate profit without a baseline comparison. The answer's reasoning is sound.; To answer whether the value represents profit, one would need either: (1) the initial principal supplied by each provider, (2) a time-series comparison (supplied_usd at an earlier date vs. 2026-08-15), or (3) a separate interest accrual metric. None of these are provided in the SQL result or documents. The answer acknowledges this limitation appropriately.; Retrieved documents (DOC_SUPPLY_000, DOC_SUPPLY_001) directly support the explanation of how interest accrual works in Aave. DOC_BORROW_000, DOC_BORROW_001, and DOC_LIQ_001 are not directly relevant to the supplied USDC value or profit calculation but do not contradict the answer.",
  "system_claims": [
    {
      "text": "Giá trị tài sản cung cấp USDC lúc 00:00 UTC 2026-08-15 là $1,997,694,271.60 USD",
      "citations": [
        "SQL1"
      ],
      "numeric": {
        "value": 1997694271.6,
        "unit": "USD",
        "evidence_id": "SQL1",
        "row": 0,
        "column": "supplied_usd_snapshot"
      }
    },
    {
      "text": "Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate, with interest accrual happening dynamically as the balance increases linearly over time",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    },
    {
      "text": "Giá trị cung cấp toàn bộ không phải là lợi nhuận; lợi nhuận là phần tăng thêm trên số tiền gốc được cung cấp",
      "citations": [
        "DOC_SUPPLY_000"
      ]
    }
  ],
  "documents": [
    {
      "id": "DOC_SUPPLY_000",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "Back to Supplying Supply Tokens beginner Introduction Supplying tokens to the Aave Protocol allows you to earn interest on your digital assets and utilize supplied tokens as collateral. When tokens are supplied, they are transferred to the Aave liquidity pool, a system of smart contracts that facilitates overcollateralized borrowing of tokens. Supplied tokens automatically accumulate interest by updating in balance at the current market supply rate. This interest accrual happens dynamically as the balance of your supplied tokens increases linearly over time, reflecting the current rate allocated to suppliers. Interest rates for supplied tokens are determined by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool, and by governance parameters that can be adjusted through community decisions. These parameters, including collateralization requirements and interest rates for suppliers and borrowers, are influenced by on-chain inputs such as token balances, oracle prices, and the borrow utilization ratio. As liquidity is supplied, borrowed, repaid, or withdrawn from the pool, the interest rates are updated accordingly. Tokens can be supplied through protocol smart contracts or through a frontend such as the Aave Labs interface, by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding tokens intended to supply. Step 2: Select Token To Supply Once connected, navigate to the ‘Dashboard’ where you’ll find the ‘Assets To Supply’ table, which lists current token balances and asset parameters. More details on supply and borrow parameters can be found by selecting the individual token icon, which will navigate to the reserve details page. Step 3: Approve Token Transfer In order to transfer tokens on an Ethereum-based network, the Aave Pool smart contract must be granted an allowance to transfer tokens from the connected wallet address. Approvals can be performed through transaction (which will incur a network fee) or signature (which does not incur a network fee). After selecting a token to supply, a modal will appear which will prompt a transaction or message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can",
      "score": 5.373592960506341
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 0.9095472101567856
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-18T02:47:43.333680+00:00",
      "source_sha256": "071408472a646541670d782521e5864abeefd6baf637700c00af764942d133f2",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.8358998770917703
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-18T02:47:43.660415+00:00",
      "source_sha256": "d35e7b9f13d1f23e78eef0c061d97f5b4a66c68cd4a79f23a2a02a159c5453e2",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 0.7746203598719164
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 0.25461108308588615
    }
  ],
  "sql": "SELECT asset, hour, supplied_usd AS supplied_usd_snapshot, source_timestamp, source_age_hours FROM market_hourly WHERE asset = 'USDC' AND hour >= '2026-08-15T00:00:00Z' AND hour < '2026-08-15T01:00:00Z' ORDER BY hour",
  "query_result": {
    "columns": [
      "asset",
      "hour",
      "supplied_usd_snapshot",
      "source_timestamp",
      "source_age_hours"
    ],
    "rows": [
      {
        "asset": "USDC",
        "hour": "2026-08-15T00:00:00+00:00",
        "supplied_usd_snapshot": 1997694271.598428,
        "source_timestamp": "2026-08-14T23:58:35+00:00",
        "source_age_hours": 0.02361111111111111
      }
    ],
    "truncated": false,
    "total_rows": 1
  }
}
```
