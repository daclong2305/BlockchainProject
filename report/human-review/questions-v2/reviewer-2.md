# Independent human review

Do not read the other reviewer’s decisions. Verify the question, answer/SQL, source support, UTC scope and units independently.
The references below are MACHINE-GENERATED DRAFTS, not approved gold. If anything is wrong, use changes_requested and explain it; do not approve until corrected and reviewed again.
Fill your name and decisions in the companion JSON. This tool does not prove human identity and never supplies human labels.

## Q001 · dev · mechanism

Cung cấp tài sản trên Aave V3 là gì?

Family: `supply_mechanism`

```json
{
  "id": "Q001",
  "category": "mechanism",
  "family": "supply_mechanism",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Cung cấp token vào pool; phân biệt cung cấp với vay, không bảo đảm mức lãi cố định."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q002 · dev · mechanism

Cung cấp tài sản trên Aave V3 là gì? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `supply_mechanism`

```json
{
  "id": "Q002",
  "category": "mechanism",
  "family": "supply_mechanism",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Cung cấp token vào pool; phân biệt cung cấp với vay, không bảo đảm mức lãi cố định."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q003 · dev · mechanism

Tài sản thế chấp có vai trò gì khi vay trên Aave V3?

Family: `collateral_mechanism`

```json
{
  "id": "Q003",
  "category": "mechanism",
  "family": "collateral_mechanism",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q004 · dev · mechanism

Tài sản thế chấp có vai trò gì khi vay trên Aave V3? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `collateral_mechanism`

```json
{
  "id": "Q004",
  "category": "mechanism",
  "family": "collateral_mechanism",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Khả năng vay phụ thuộc tài sản thế chấp và các tham số rủi ro; không phải cứ cung cấp bao nhiêu sẽ vay được bấy nhiêu."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q005 · test · mechanism

Health factor thể hiện điều gì và khi nào vị thế có nguy cơ thanh lý?

Family: `health_factor`

```json
{
  "id": "Q005",
  "category": "mechanism",
  "family": "health_factor",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Health factor phản ánh mức an toàn của vị thế; dưới 1 có thể bị thanh lý, không đồng nghĩa chắc chắn bị thanh lý ngay lập tức."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q006 · test · mechanism

Health factor thể hiện điều gì và khi nào vị thế có nguy cơ thanh lý? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `health_factor`

```json
{
  "id": "Q006",
  "category": "mechanism",
  "family": "health_factor",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Health factor phản ánh mức an toàn của vị thế; dưới 1 có thể bị thanh lý, không đồng nghĩa chắc chắn bị thanh lý ngay lập tức."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q007 · test · mechanism

Cơ chế thanh lý trên Aave V3 hoạt động như thế nào?

Family: `liquidation_process`

```json
{
  "id": "Q007",
  "category": "mechanism",
  "family": "liquidation_process",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Health factor dưới 1 khiến vị thế đủ điều kiện thanh lý. Điều kiện này không xác định thời điểm thanh lý thực tế.",
      "Người thanh lý hoàn trả một phần nợ và nhận tài sản thế chấp kèm phần thưởng thanh lý. Tùy điều kiện của vị thế, khoản nợ được hoàn trả có thể lên tới toàn bộ."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q008 · test · mechanism

Cơ chế thanh lý trên Aave V3 hoạt động như thế nào? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `liquidation_process`

```json
{
  "id": "Q008",
  "category": "mechanism",
  "family": "liquidation_process",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Health factor dưới 1 khiến vị thế đủ điều kiện thanh lý. Điều kiện này không xác định thời điểm thanh lý thực tế.",
      "Người thanh lý hoàn trả một phần nợ và nhận tài sản thế chấp kèm phần thưởng thanh lý. Tùy điều kiện của vị thế, khoản nợ được hoàn trả có thể lên tới toàn bộ."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q009 · test · mechanism

Người vay trên Aave V3 phải lưu ý gì về lãi vay?

Family: `borrow_interest`

```json
{
  "id": "Q009",
  "category": "mechanism",
  "family": "borrow_interest",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Lãi bắt đầu tích lũy ngay khi người dùng vay token.",
      "Lãi suất vay có thể thay đổi theo mức sử dụng vốn và tham số của giao thức."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q010 · test · mechanism

Người vay trên Aave V3 phải lưu ý gì về lãi vay? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `borrow_interest`

```json
{
  "id": "Q010",
  "category": "mechanism",
  "family": "borrow_interest",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Lãi bắt đầu tích lũy ngay khi người dùng vay token.",
      "Lãi suất vay có thể thay đổi theo mức sử dụng vốn và tham số của giao thức."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q011 · test · mechanism

Việc rút tài sản đã cung cấp phụ thuộc vào điều kiện nào?

Family: `withdraw_supply`

```json
{
  "id": "Q011",
  "category": "mechanism",
  "family": "withdraw_supply",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Số tiền rút được phụ thuộc vào phần thanh khoản chưa được vay còn sẵn trong pool.",
      "Nếu tài sản đang được dùng làm thế chấp cho khoản vay, vị thế phải còn đủ thế chấp sau khi rút. Người dùng có thể cần trả bớt nợ hoặc thêm tài sản thế chấp."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
      "id": "DOC_WITHDRAW_000",
      "title": "Withdraw Tokens | Aave",
      "url": "https://aave.com/help/supplying/withdraw-tokens",
      "collected_at": "2026-11-22T09:12:17.587025+00:00",
      "source_sha256": "03e8aa2323f7b856e267363066a975fa7615c71e4abfa639a4abf71eaf59d460",
      "text": "Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q012 · test · mechanism

Việc rút tài sản đã cung cấp phụ thuộc vào điều kiện nào? Hãy trả lời ngắn gọn và dẫn nguồn.

Family: `withdraw_supply`

```json
{
  "id": "Q012",
  "category": "mechanism",
  "family": "withdraw_supply",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Số tiền rút được phụ thuộc vào phần thanh khoản chưa được vay còn sẵn trong pool.",
      "Nếu tài sản đang được dùng làm thế chấp cho khoản vay, vị thế phải còn đủ thế chấp sau khi rút. Người dùng có thể cần trả bớt nợ hoặc thêm tài sản thế chấp."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "expected_numeric": [],
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
      "id": "DOC_WITHDRAW_000",
      "title": "Withdraw Tokens | Aave",
      "url": "https://aave.com/help/supplying/withdraw-tokens",
      "collected_at": "2026-11-22T09:12:17.587025+00:00",
      "source_sha256": "03e8aa2323f7b856e267363066a975fa7615c71e4abfa639a4abf71eaf59d460",
      "text": "Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q013 · dev · lookup

Giá trị tài sản cung cấp USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?

Family: `supply_snapshot`

```json
{
  "id": "Q013",
  "category": "lookup",
  "family": "supply_snapshot",
  "split": "dev",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1997694271.598428
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1997694271.598428,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q014 · dev · lookup

Giá trị tài sản cung cấp WETH lúc 00:00 UTC ngày 2025-08-15 là bao nhiêu USD?

Family: `supply_snapshot`

```json
{
  "id": "Q014",
  "category": "lookup",
  "family": "supply_snapshot",
  "split": "dev",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2025-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 11041542615.29097
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 11041542615.29097,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2025-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 11041542615.29097
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q015 · dev · lookup

Dư nợ USDC lúc 00:00 UTC ngày 2026-08-15 là bao nhiêu USD?

Family: `debt_snapshot`

```json
{
  "id": "Q015",
  "category": "lookup",
  "family": "debt_snapshot",
  "split": "dev",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1993676848.0321777,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q016 · dev · lookup

Dư nợ WETH lúc 00:00 UTC ngày 2025-08-15 là bao nhiêu USD?

Family: `debt_snapshot`

```json
{
  "id": "Q016",
  "category": "lookup",
  "family": "debt_snapshot",
  "split": "dev",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2025-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 10023005896.239573
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 10023005896.239573,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q017 · test · lookup

Trong tháng 2026-08 UTC có bao nhiêu giao dịch thanh lý trên Aave V3 Ethereum?

Family: `transaction_count`

```json
{
  "id": "Q017",
  "category": "lookup",
  "family": "transaction_count",
  "split": "test",
  "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 107
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 107,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 107
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q018 · test · lookup

Trong tháng 2025-08 UTC có bao nhiêu giao dịch thanh lý trên Aave V3 Ethereum?

Family: `transaction_count`

```json
{
  "id": "Q018",
  "category": "lookup",
  "family": "transaction_count",
  "split": "test",
  "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 307
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 307,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
      "rows": [
        {
          "value": 307
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q019 · test · lookup

Trong tháng 2026-08 UTC có bao nhiêu sự kiện thanh lý trên Aave V3 Ethereum?

Family: `event_count`

```json
{
  "id": "Q019",
  "category": "lookup",
  "family": "event_count",
  "split": "test",
  "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 158
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 158,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 158
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q020 · test · lookup

Trong tháng 2025-08 UTC có bao nhiêu sự kiện thanh lý trên Aave V3 Ethereum?

Family: `event_count`

```json
{
  "id": "Q020",
  "category": "lookup",
  "family": "event_count",
  "split": "test",
  "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 307
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 307,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
      "rows": [
        {
          "value": 307
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q021 · test · lookup

Tổng giá trị thanh lý trên Aave V3 Ethereum trong tháng 2026-08 (UTC) là bao nhiêu USD?

Family: `liquidation_value`

```json
{
  "id": "Q021",
  "category": "lookup",
  "family": "liquidation_value",
  "split": "test",
  "sql": "SELECT sum(amount_usd) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 6604733.083234468
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 6604733.083234468,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT sum(amount_usd) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 6604733.083234468
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q022 · test · lookup

Tổng giá trị thanh lý trên Aave V3 Ethereum trong tháng 2025-08 (UTC) là bao nhiêu USD?

Family: `liquidation_value`

```json
{
  "id": "Q022",
  "category": "lookup",
  "family": "liquidation_value",
  "split": "test",
  "sql": "SELECT sum(amount_usd) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 28132234.04010158
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 28132234.04010158,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT sum(amount_usd) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-08-01' AND time < TIMESTAMPTZ '2025-09-01'",
      "rows": [
        {
          "value": 28132234.04010158
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q023 · test · lookup

Dư nợ USDC lớn nhất theo quan sát giờ trong tháng 2026-08 là bao nhiêu USD?

Family: `debt_peak`

```json
{
  "id": "Q023",
  "category": "lookup",
  "family": "debt_peak",
  "split": "test",
  "sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 2073673650.805748
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2073673650.805748,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='USDC' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 2073673650.805748
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q024 · test · lookup

Dư nợ WETH lớn nhất theo quan sát giờ trong tháng 2025-08 là bao nhiêu USD?

Family: `debt_peak`

```json
{
  "id": "Q024",
  "category": "lookup",
  "family": "debt_peak",
  "split": "test",
  "sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour >= TIMESTAMPTZ '2025-08-01' AND hour < TIMESTAMPTZ '2025-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 10836798387.491997
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 10836798387.491997,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT max(borrowed_usd) AS value FROM market_hourly WHERE asset='WETH' AND hour >= TIMESTAMPTZ '2025-08-01' AND hour < TIMESTAMPTZ '2025-09-01'",
      "rows": [
        {
          "value": 10836798387.491997
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q025 · dev · analysis

Giá trị dư nợ trung bình theo giờ của DAI trong tháng 2026-06 là bao nhiêu USD?

Family: `avg_debt`

```json
{
  "id": "Q025",
  "category": "analysis",
  "family": "avg_debt",
  "split": "dev",
  "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-06-01' AND hour < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 98282885.63031632
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 98282885.63031632,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q026 · dev · analysis

Giá trị dư nợ trung bình theo giờ của USDT trong tháng 2026-07 là bao nhiêu USD?

Family: `avg_debt`

```json
{
  "id": "Q026",
  "category": "analysis",
  "family": "avg_debt",
  "split": "dev",
  "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-07-01' AND hour < TIMESTAMPTZ '2026-08-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 2337819599.9938083
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2337819599.9938083,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q027 · dev · analysis

Giá trị dư nợ trung bình theo giờ của USDe trong tháng 2026-08 là bao nhiêu USD?

Family: `avg_debt`

```json
{
  "id": "Q027",
  "category": "analysis",
  "family": "avg_debt",
  "split": "dev",
  "sql": "SELECT avg(borrowed_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 521264061.9902388
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 521264061.9902388,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q028 · dev · analysis

Giá trị tài sản cung cấp trung bình theo giờ của DAI trong tháng 2026-06 là bao nhiêu USD?

Family: `avg_supply`

```json
{
  "id": "Q028",
  "category": "analysis",
  "family": "avg_supply",
  "split": "dev",
  "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-06-01' AND hour < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 118343676.63059068
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 118343676.63059068,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q029 · dev · analysis

Giá trị tài sản cung cấp trung bình theo giờ của USDT trong tháng 2026-07 là bao nhiêu USD?

Family: `avg_supply`

```json
{
  "id": "Q029",
  "category": "analysis",
  "family": "avg_supply",
  "split": "dev",
  "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-07-01' AND hour < TIMESTAMPTZ '2026-08-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 2831780087.9296083
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2831780087.9296083,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q030 · dev · analysis

Giá trị tài sản cung cấp trung bình theo giờ của USDe trong tháng 2026-08 là bao nhiêu USD?

Family: `avg_supply`

```json
{
  "id": "Q030",
  "category": "analysis",
  "family": "avg_supply",
  "split": "dev",
  "sql": "SELECT avg(supplied_usd) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-08-01' AND hour < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 749295298.141774
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 749295298.141774,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q031 · test · analysis

Lúc 00:00 UTC ngày 2026-06-15, dư nợ USDC trừ dư nợ DAI bằng bao nhiêu USD?

Family: `asset_gap`

```json
{
  "id": "Q031",
  "category": "analysis",
  "family": "asset_gap",
  "split": "test",
  "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='DAI' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','DAI') AND hour=TIMESTAMPTZ '2026-06-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1692127461.001217
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1692127461.001217,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='DAI' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','DAI') AND hour=TIMESTAMPTZ '2026-06-15 00:00:00+00'",
      "rows": [
        {
          "value": 1692127461.001217
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q032 · test · analysis

Lúc 00:00 UTC ngày 2026-07-15, dư nợ USDC trừ dư nợ USDT bằng bao nhiêu USD?

Family: `asset_gap`

```json
{
  "id": "Q032",
  "category": "analysis",
  "family": "asset_gap",
  "split": "test",
  "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='USDT' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','USDT') AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -437232310.61343
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -437232310.61343,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='USDT' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','USDT') AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
      "rows": [
        {
          "value": -437232310.61343
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q033 · test · analysis

Lúc 00:00 UTC ngày 2026-08-15, dư nợ USDC trừ dư nợ USDe bằng bao nhiêu USD?

Family: `asset_gap`

```json
{
  "id": "Q033",
  "category": "analysis",
  "family": "asset_gap",
  "split": "test",
  "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='USDe' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','USDe') AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 1417403487.0444803
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1417403487.0444803,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT max(CASE WHEN asset='USDC' THEN borrowed_usd END)-max(CASE WHEN asset='USDe' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset IN ('USDC','USDe') AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
      "rows": [
        {
          "value": 1417403487.0444803
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q034 · test · analysis

Dư nợ DAI trung bình theo giờ quý II trừ quý I năm 2026 là bao nhiêu USD?

Family: `quarter_change`

```json
{
  "id": "Q034",
  "category": "analysis",
  "family": "quarter_change",
  "split": "test",
  "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -12133324.429995105
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -12133324.429995105,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='DAI' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": -12133324.429995105
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q035 · test · analysis

Dư nợ USDT trung bình theo giờ quý II trừ quý I năm 2026 là bao nhiêu USD?

Family: `quarter_change`

```json
{
  "id": "Q035",
  "category": "analysis",
  "family": "quarter_change",
  "split": "test",
  "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -1725488668.2893205
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -1725488668.2893205,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='USDT' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": -1725488668.2893205
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q036 · test · analysis

Dư nợ USDe trung bình theo giờ quý II trừ quý I năm 2026 là bao nhiêu USD?

Family: `quarter_change`

```json
{
  "id": "Q036",
  "category": "analysis",
  "family": "quarter_change",
  "split": "test",
  "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -240373085.12855375
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -240373085.12855375,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT avg(CASE WHEN hour>=TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END)-avg(CASE WHEN hour<TIMESTAMPTZ '2026-04-01' THEN borrowed_usd END) AS value FROM market_hourly WHERE asset='USDe' AND hour >= TIMESTAMPTZ '2026-01-01' AND hour < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": -240373085.12855375
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q037 · test · analysis

Từ 2025-01-01 đến trước 2026-01-01 UTC, tháng nào có nhiều giao dịch thanh lý nhất và có bao nhiêu giao dịch? Nếu bằng nhau chọn tháng sớm nhất.

Family: `peak_month_tx`

```json
{
  "id": "Q037",
  "category": "analysis",
  "family": "peak_month_tx",
  "split": "test",
  "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-01-01' AND time < TIMESTAMPTZ '2026-01-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "month": "2025-02",
        "value": 2188
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2188,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-01-01' AND time < TIMESTAMPTZ '2026-01-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
      "rows": [
        {
          "month": "2025-02",
          "value": 2188
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q038 · test · analysis

Từ 2026-01-01 đến trước 2026-09-01 UTC, tháng nào có nhiều giao dịch thanh lý nhất và có bao nhiêu giao dịch? Nếu bằng nhau chọn tháng sớm nhất.

Family: `peak_month_tx`

```json
{
  "id": "Q038",
  "category": "analysis",
  "family": "peak_month_tx",
  "split": "test",
  "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-01-01' AND time < TIMESTAMPTZ '2026-09-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "month": "2026-02",
        "value": 2647
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2647,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-01-01' AND time < TIMESTAMPTZ '2026-09-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
      "rows": [
        {
          "month": "2026-02",
          "value": 2647
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q039 · test · analysis

Từ 2025-07-01 đến trước 2026-07-01 UTC, tháng nào có nhiều giao dịch thanh lý nhất và có bao nhiêu giao dịch? Nếu bằng nhau chọn tháng sớm nhất.

Family: `peak_month_tx`

```json
{
  "id": "Q039",
  "category": "analysis",
  "family": "peak_month_tx",
  "split": "test",
  "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-07-01' AND time < TIMESTAMPTZ '2026-07-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "month": "2026-02",
        "value": 2647
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 2647,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT strftime(date_trunc('month',time),'%Y-%m') AS month, count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2025-07-01' AND time < TIMESTAMPTZ '2026-07-01' GROUP BY 1 ORDER BY value DESC, month ASC LIMIT 1",
      "rows": [
        {
          "month": "2026-02",
          "value": 2647
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q040 · test · analysis

Tổng USD thanh lý tháng 2026-06 trừ tổng USD từ 2026-05-01 đến trước 2026-06-01 UTC bằng bao nhiêu?

Family: `liquidation_change`

```json
{
  "id": "Q040",
  "category": "analysis",
  "family": "liquidation_change",
  "split": "test",
  "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-06-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-06-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-07-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": 51931723.65202591
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 51931723.65202591,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-06-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-06-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-07-01'",
      "rows": [
        {
          "value": 51931723.65202591
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q041 · test · analysis

Tổng USD thanh lý tháng 2026-07 trừ tổng USD từ 2026-05-01 đến trước 2026-07-01 UTC bằng bao nhiêu?

Family: `liquidation_change`

```json
{
  "id": "Q041",
  "category": "analysis",
  "family": "liquidation_change",
  "split": "test",
  "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-07-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-07-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-08-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -325072291.77384555
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -325072291.77384555,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-07-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-07-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-08-01'",
      "rows": [
        {
          "value": -325072291.77384555
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q042 · test · analysis

Tổng USD thanh lý tháng 2026-08 trừ tổng USD từ 2026-05-01 đến trước 2026-08-01 UTC bằng bao nhiêu?

Family: `liquidation_change`

```json
{
  "id": "Q042",
  "category": "analysis",
  "family": "liquidation_change",
  "split": "test",
  "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-08-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-08-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [],
    "sql_result": [
      {
        "value": -324263050.30990607
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": -324263050.30990607,
      "unit": "USD",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT sum(CASE WHEN time>=TIMESTAMPTZ '2026-08-01' THEN amount_usd ELSE 0 END)-sum(CASE WHEN time<TIMESTAMPTZ '2026-08-01' THEN amount_usd ELSE 0 END) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-05-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": -324263050.30990607
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": false,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q043 · dev · mixed

Dư nợ USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?

Family: `debt_explanation`

```json
{
  "id": "Q043",
  "category": "mixed",
  "family": "debt_explanation",
  "split": "dev",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
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
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1993676848.0321777,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q044 · dev · mixed

Dư nợ WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Có thể coi đây là tổng tiền vay mới trong tháng không? Vì sao?

Family: `debt_explanation`

```json
{
  "id": "Q044",
  "category": "mixed",
  "family": "debt_explanation",
  "split": "dev",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
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
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 3042883324.3152447,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q045 · dev · mixed

Giá trị tài sản cung cấp USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Có thể coi đây là lợi nhuận người cung cấp đã thu được không? Vì sao?

Family: `supply_explanation`

```json
{
  "id": "Q045",
  "category": "mixed",
  "family": "supply_explanation",
  "split": "dev",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
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
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1997694271.598428,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q046 · dev · mixed

Giá trị tài sản cung cấp WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Có thể coi đây là lợi nhuận người cung cấp đã thu được không? Vì sao?

Family: `supply_explanation`

```json
{
  "id": "Q046",
  "category": "mixed",
  "family": "supply_explanation",
  "split": "dev",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
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
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 3897799627.0425687,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q047 · test · mixed

Tháng 2026-08 có bao nhiêu sự kiện thanh lý? Giải thích: Số sự kiện không chứng minh mọi vị thế có health factor dưới 1 đều đã được thanh lý.

Family: `liquidation_explanation`

```json
{
  "id": "Q047",
  "category": "mixed",
  "family": "liquidation_explanation",
  "split": "test",
  "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [
      "Số sự kiện không chứng minh mọi vị thế có health factor dưới 1 đều đã được thanh lý."
    ],
    "sql_result": [
      {
        "value": 158
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 158,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 158
        }
      ]
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q048 · test · mixed

Tháng 2026-07 có bao nhiêu sự kiện thanh lý? Giải thích: Số sự kiện không chứng minh mọi vị thế có health factor dưới 1 đều đã được thanh lý.

Family: `liquidation_explanation`

```json
{
  "id": "Q048",
  "category": "mixed",
  "family": "liquidation_explanation",
  "split": "test",
  "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-07-01' AND time < TIMESTAMPTZ '2026-08-01'",
  "reference_answer": {
    "required_points": [
      "Số sự kiện không chứng minh mọi vị thế có health factor dưới 1 đều đã được thanh lý."
    ],
    "sql_result": [
      {
        "value": 63
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 63,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(*) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-07-01' AND time < TIMESTAMPTZ '2026-08-01'",
      "rows": [
        {
          "value": 63
        }
      ]
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q049 · test · mixed

Trong tháng 2026-08 (UTC) có bao nhiêu giao dịch thanh lý trên Aave V3 Ethereum? Số sự kiện thanh lý và số giao dịch thanh lý có nhất thiết bằng nhau không? Giải thích.

Family: `transactions_explanation`

```json
{
  "id": "Q049",
  "category": "mixed",
  "family": "transactions_explanation",
  "split": "test",
  "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
  "reference_answer": {
    "required_points": [
      "Một giao dịch có thể chứa nhiều sự kiện thanh lý. Đếm giao dịch phân biệt theo tx_hash và đếm từng sự kiện là hai phép đếm khác nhau.",
      "Kết quả nhóm các sự kiện theo tx_hash trong tháng được hỏi có giao dịch chứa nhiều sự kiện, nên hai số đếm không nhất thiết bằng nhau."
    ],
    "sql_result": [
      {
        "value": 107
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 107,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01'",
      "rows": [
        {
          "value": 107
        }
      ]
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    },
    {
      "id": "SQL2",
      "sql": "SELECT count(*) AS transaction_count, sum(event_count) AS event_total, count(*) FILTER (WHERE event_count > 1) AS transactions_with_multiple_events FROM (SELECT tx_hash, count(*) AS event_count FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-08-01' AND time < TIMESTAMPTZ '2026-09-01' GROUP BY tx_hash) AS events_per_transaction",
      "rows": [
        {
          "transaction_count": 107,
          "event_total": 158,
          "transactions_with_multiple_events": 18
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q050 · test · mixed

Trong tháng 2026-07 (UTC) có bao nhiêu giao dịch thanh lý trên Aave V3 Ethereum? Số sự kiện thanh lý và số giao dịch thanh lý có nhất thiết bằng nhau không? Giải thích.

Family: `transactions_explanation`

```json
{
  "id": "Q050",
  "category": "mixed",
  "family": "transactions_explanation",
  "split": "test",
  "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-07-01' AND time < TIMESTAMPTZ '2026-08-01'",
  "reference_answer": {
    "required_points": [
      "Một giao dịch có thể chứa nhiều sự kiện thanh lý. Đếm giao dịch phân biệt theo tx_hash và đếm từng sự kiện là hai phép đếm khác nhau.",
      "Kết quả nhóm các sự kiện theo tx_hash trong tháng được hỏi có giao dịch chứa nhiều sự kiện, nên hai số đếm không nhất thiết bằng nhau."
    ],
    "sql_result": [
      {
        "value": 52
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 52,
      "unit": "count",
      "decimals": 2
    }
  ],
  "sources": [
    {
      "id": "SQL1",
      "sql": "SELECT count(DISTINCT tx_hash) AS value FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-07-01' AND time < TIMESTAMPTZ '2026-08-01'",
      "rows": [
        {
          "value": 52
        }
      ]
    },
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-18T02:47:43.950779+00:00",
      "source_sha256": "0a38b5c040f315f20d829ffdbfa5e73df3e175876fd6eb6a7519220404314057",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    },
    {
      "id": "SQL2",
      "sql": "SELECT count(*) AS transaction_count, sum(event_count) AS event_total, count(*) FILTER (WHERE event_count > 1) AS transactions_with_multiple_events FROM (SELECT tx_hash, count(*) AS event_count FROM liquidation_events WHERE time >= TIMESTAMPTZ '2026-07-01' AND time < TIMESTAMPTZ '2026-08-01' GROUP BY tx_hash) AS events_per_transaction",
      "rows": [
        {
          "transaction_count": 52,
          "event_total": 63,
          "transactions_with_multiple_events": 5
        }
      ]
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q051 · test · mixed

Dư nợ USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Số liệu này có đủ chứng minh lãi vay là nguyên nhân làm tăng dư nợ không? Giải thích căn cứ.

Family: `debt_change_explanation`

```json
{
  "id": "Q051",
  "category": "mixed",
  "family": "debt_change_explanation",
  "split": "test",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [
      "Biến động dư nợ USD không đủ kết luận nguyên nhân từ lãi vay hoặc hành vi người dùng."
    ],
    "sql_result": [
      {
        "value": 1993676848.0321777
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1993676848.0321777,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q052 · test · mixed

Dư nợ WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Số liệu này có đủ chứng minh lãi vay là nguyên nhân làm tăng dư nợ không? Giải thích căn cứ.

Family: `debt_change_explanation`

```json
{
  "id": "Q052",
  "category": "mixed",
  "family": "debt_change_explanation",
  "split": "test",
  "sql": "SELECT borrowed_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [
      "Biến động dư nợ USD không đủ kết luận nguyên nhân từ lãi vay hoặc hành vi người dùng."
    ],
    "sql_result": [
      {
        "value": 3042883324.3152447
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 3042883324.3152447,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q053 · test · mixed

Giá trị tài sản cung cấp USDC lúc 00:00 UTC 2026-08-15 là bao nhiêu USD? Số liệu này có chứng minh tài sản không có rủi ro và luôn rút ngay được không? Giải thích điều kiện.

Family: `supply_risk_explanation`

```json
{
  "id": "Q053",
  "category": "mixed",
  "family": "supply_risk_explanation",
  "split": "test",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='USDC' AND hour=TIMESTAMPTZ '2026-08-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [
      "Giá trị tài sản cung cấp chỉ mô tả số dư theo bộ dữ liệu tại thời điểm được hỏi. Nó không chứng minh tài sản không có rủi ro hoặc luôn có thể rút ngay.",
      "Số tiền rút được phụ thuộc vào phần thanh khoản chưa được vay còn sẵn trong pool.",
      "Nếu tài sản đang được dùng làm thế chấp cho khoản vay, vị thế phải còn đủ thế chấp sau khi rút. Người dùng có thể cần trả bớt nợ hoặc thêm tài sản thế chấp."
    ],
    "sql_result": [
      {
        "value": 1997694271.598428
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 1997694271.598428,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
    },
    {
      "id": "DOC_WITHDRAW_000",
      "title": "Withdraw Tokens | Aave",
      "url": "https://aave.com/help/supplying/withdraw-tokens",
      "collected_at": "2026-11-22T09:12:17.587025+00:00",
      "source_sha256": "03e8aa2323f7b856e267363066a975fa7615c71e4abfa639a4abf71eaf59d460",
      "text": "Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q054 · test · mixed

Giá trị tài sản cung cấp WETH lúc 00:00 UTC 2026-07-15 là bao nhiêu USD? Số liệu này có chứng minh tài sản không có rủi ro và luôn rút ngay được không? Giải thích điều kiện.

Family: `supply_risk_explanation`

```json
{
  "id": "Q054",
  "category": "mixed",
  "family": "supply_risk_explanation",
  "split": "test",
  "sql": "SELECT supplied_usd AS value FROM market_hourly WHERE asset='WETH' AND hour=TIMESTAMPTZ '2026-07-15 00:00:00+00'",
  "reference_answer": {
    "required_points": [
      "Giá trị tài sản cung cấp chỉ mô tả số dư theo bộ dữ liệu tại thời điểm được hỏi. Nó không chứng minh tài sản không có rủi ro hoặc luôn có thể rút ngay.",
      "Số tiền rút được phụ thuộc vào phần thanh khoản chưa được vay còn sẵn trong pool.",
      "Nếu tài sản đang được dùng làm thế chấp cho khoản vay, vị thế phải còn đủ thế chấp sau khi rút. Người dùng có thể cần trả bớt nợ hoặc thêm tài sản thế chấp."
    ],
    "sql_result": [
      {
        "value": 3897799627.0425687
      }
    ],
    "limitation": ""
  },
  "expected_numeric": [
    {
      "row": 0,
      "column": "value",
      "value": 3897799627.0425687,
      "unit": "USD",
      "decimals": 2
    }
  ],
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
    },
    {
      "id": "DOC_WITHDRAW_000",
      "title": "Withdraw Tokens | Aave",
      "url": "https://aave.com/help/supplying/withdraw-tokens",
      "collected_at": "2026-11-22T09:12:17.587025+00:00",
      "source_sha256": "03e8aa2323f7b856e267363066a975fa7615c71e4abfa639a4abf71eaf59d460",
      "text": "Back to Supplying Withdraw Tokens beginner Introduction Withdrawing tokens from the Aave Protocol transfers underlying supplied assets along with any accrued interest, provided there is sufficient liquidity in the pool. This means suppliers can withdraw up to the amount available in the pool that is not currently borrowed. The process varies slightly depending on the type of token and the withdrawal method, and can be performed through protocl smart contracts or a frontend such as the Aave Labs interface . Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet where the tokens are supplied. Step 2: Navigate to 'Your Supplies' Once connected, navigate to the ‘Dashboard’ and locate the ‘Your Supplies’ section. This table displays all tokens you have supplied to the Aave Protocol. Step 3: Select Token to Withdraw Choose the token you wish to withdraw from the list. Verify that there is enough available liquidity in the pool to support your withdrawal. If the token is not being used as collateral for an active borrow position, you can proceed to withdraw the desired amount. Step 4: Confirm Withdrawal Enter the amount you want to withdraw and confirm the transaction in your wallet. If you are withdrawing the same underlying token that you supplied (e.g., WETH to WETH), no additional approval transaction is needed. However, if you’re withdrawing to a network base token, such as ETH, the Aave Protocol stores these as wrapped tokens (e.g., WETH). In this case, the withdrawal process involves the WrappedTokenGateway contract, where the WETH is unwrapped and withdrawn in a single transaction. Step 5: Handling Collateralised Tokens If your supplied tokens are used as collateral, you may need to repay part of your borrow position or supply additional collateral to maintain a healthy balance before you can withdraw. Regularly monitoring your health factor will help you manage this effectively. Step 6: Withdrawing and Switching Tokens The Aave Labs interface also offers a feature to withdraw and switch to a different token in one action. This requires token approval for both the withdrawal and the switch. Ensure you review the necessary approvals in your wallet before proceeding. Related Supply Tokens beginner Supply tokens to the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read"
    }
  ],
  "expected_refusal": false,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q055 · dev · unanswerable

Phí gas tổng cộng của các giao dịch thanh lý tháng 8/2026 là bao nhiêu USD?

Family: `unavailable_fields`

```json
{
  "id": "Q055",
  "category": "unanswerable",
  "family": "unavailable_fields",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Gas/profit chưa được xác minh và bị loại khỏi dữ liệu thực nghiệm."
    ],
    "sql_result": null,
    "limitation": "Gas/profit chưa được xác minh và bị loại khỏi dữ liệu thực nghiệm."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q056 · dev · unanswerable

Lợi nhuận USD thực của người thanh lý tháng 8/2026 là bao nhiêu?

Family: `unavailable_fields`

```json
{
  "id": "Q056",
  "category": "unanswerable",
  "family": "unavailable_fields",
  "split": "dev",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Gas/profit chưa được xác minh và bị loại khỏi dữ liệu thực nghiệm."
    ],
    "sql_result": null,
    "limitation": "Gas/profit chưa được xác minh và bị loại khỏi dữ liệu thực nghiệm."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q057 · test · unanswerable

Có bao nhiêu giao dịch thanh lý riêng USDC tháng 8/2026?

Family: `unverified_liquidation_asset`

```json
{
  "id": "Q057",
  "category": "unanswerable",
  "family": "unverified_liquidation_asset",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Chưa xác minh ánh xạ market sang tài sản thanh lý; không thể kết luận theo token."
    ],
    "sql_result": null,
    "limitation": "Chưa xác minh ánh xạ market sang tài sản thanh lý; không thể kết luận theo token."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q058 · test · unanswerable

Tổng USD thanh lý riêng WETH tháng 7/2026 là bao nhiêu?

Family: `unverified_liquidation_asset`

```json
{
  "id": "Q058",
  "category": "unanswerable",
  "family": "unverified_liquidation_asset",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Chưa xác minh ánh xạ market sang tài sản thanh lý; không thể kết luận theo token."
    ],
    "sql_result": null,
    "limitation": "Chưa xác minh ánh xạ market sang tài sản thanh lý; không thể kết luận theo token."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q059 · test · unanswerable

Dư nợ USDC ngay bây giờ là bao nhiêu USD?

Family: `unavailable_live_or_forecast`

```json
{
  "id": "Q059",
  "category": "unanswerable",
  "family": "unavailable_live_or_forecast",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Bộ dữ liệu lịch sử cố định không cung cấp dữ liệu trực tiếp hoặc kết quả dự báo tương lai."
    ],
    "sql_result": null,
    "limitation": "Bộ dữ liệu lịch sử cố định không cung cấp dữ liệu trực tiếp hoặc kết quả dự báo tương lai."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```

## Q060 · test · unanswerable

Dư nợ WETH tháng 12/2027 chắc chắn sẽ là bao nhiêu USD?

Family: `unavailable_live_or_forecast`

```json
{
  "id": "Q060",
  "category": "unanswerable",
  "family": "unavailable_live_or_forecast",
  "split": "test",
  "sql": "",
  "reference_answer": {
    "required_points": [
      "Bộ dữ liệu lịch sử cố định không cung cấp dữ liệu trực tiếp hoặc kết quả dự báo tương lai."
    ],
    "sql_result": null,
    "limitation": "Bộ dữ liệu lịch sử cố định không cung cấp dữ liệu trực tiếp hoặc kết quả dự báo tương lai."
  },
  "expected_numeric": [],
  "sources": [
    {
      "id": "POLICY",
      "text": "Available fields: hourly supplied_usd/borrowed_usd and liquidation events. No gas, profit, verified token mapping, live data, forecasts or wallet health factors."
    }
  ],
  "expected_refusal": true,
  "requires_judge": true,
  "scope": {
    "chain": "Ethereum",
    "protocol": "Aave V3",
    "start": "2025-01-01",
    "end_exclusive": "2026-09-01"
  }
}
```
