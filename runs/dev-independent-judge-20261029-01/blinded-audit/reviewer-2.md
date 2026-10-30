# Independent audit

Assess each answer against the supplied reference and sources. Do not inspect machine labels or the other reviewer’s decisions.
Record 0 or 1 for correctness, faithfulness and citation quality; give reasons. Do not infer correctness from a runtime passed status. Gold must already have independent review for a final experiment.

## A0001

```json
{
  "question": "Health factor thể hiện điều gì và khi nào vị thế có nguy cơ thanh lý?",
  "reference_answer": {
    "required_points": [
      "Health factor phản ánh mức an toàn của vị thế; dưới 1 có thể bị thanh lý, không đồng nghĩa chắc chắn bị thanh lý ngay lập tức."
    ],
    "sql_result": null,
    "limitation": ""
  },
  "sources": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-28T14:16:07.023365+00:00",
      "source_sha256": "29031b86b53d3b90c456e0eb91dafc75cdacb68928b4f776eb590eff301f3b25",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent"
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-28T14:16:07.023365+00:00",
      "source_sha256": "29031b86b53d3b90c456e0eb91dafc75cdacb68928b4f776eb590eff301f3b25",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read"
    }
  ],
  "system_answer": "Health factor thể hiện mức độ an toàn của một vị thế vay. Vị thế có nguy cơ thanh lý khi health factor thấp hơn 1.",
  "system_claims": [],
  "documents": [
    {
      "id": "DOC_LIQ_000",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-28T14:16:07.023365+00:00",
      "source_sha256": "29031b86b53d3b90c456e0eb91dafc75cdacb68928b4f776eb590eff301f3b25",
      "text": "Back to Borrowing Health Factor & Liquidations advanced Health Factor The health factor is a critical metric within the Aave Protocol that measures the safety of a borrow position. It is calculated as: Health Factor = (Total Collateral Value * Weighted Average Liquidation Threshold) / Total Borrow Value This metric indicates the stability of a borrow position, with a health factor below 1 signaling the risk of liquidation. The liquidation threshold, set by Aave Governance for each collateral asset, determines the maximum percentage of value that can be borrowed against it. For example, if you supply $10,000 in ETH with an 80% liquidation threshold and borrow $6,000 in GHO, your health factor would be 1.333. Managing Health Factor Maintaining a health factor above 1 is crucial to avoid liquidation. Regular monitoring of this metric is essential, as it fluctuates with the value of both collateral and borrowed assets. To improve your health factor, you can either supply more collateral or repay part of your borrow position. The health factor is sensitive to market changes—if your collateral's value increases, so does your health factor; conversely, if it decreases, your health factor drops, heightening the risk of liquidation. There is no universally \"safe\" health factor, as this depends on the volatility and correlation of your assets. Generally, lower health factors may be acceptable for correlated assets, such as stablecoins or assets closely tied to ETH. Tools for Managing Health Factor (Use at your own risk): Simulate health factor changes: DeFi Simulator Auto-repay borrow position: DeFi Saver Liquidation Process A liquidation in the Aave Protocol occurs when a borrower's health factor falls below 1, indicating that their collateral no longer sufficiently covers the borrowed amount. This situation can happen when the value of the collateral decreases or the borrowed amount increases, pushing the position past the liquidation threshold. The amount that can be liquidated depends on the health factor and position size: Up to 50% of total debt can be liquidated when the health factor is above 0.95 AND both the collateral and debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent",
      "score": 1.2606761995083786
    },
    {
      "id": "DOC_BORROW_001",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-28T14:16:05.100252+00:00",
      "source_sha256": "3d05a42e5f1beb0ea05cb067c4ed673135313157efe4f2fb57d83975445e2d32",
      "text": "interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health factor is a critical indicator of the safety of your borrow position, and maintaining it above the liquidation threshold is essential to prevent your collateral from being liquidated. Related Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read Health Factor & Liquidations advanced Mechanics of Aave Protocol liquidations. 5 min read",
      "score": 1.2350568060210767
    },
    {
      "id": "DOC_BORROW_000",
      "title": "Borrow Tokens | Aave",
      "url": "https://aave.com/help/borrowing/borrow-tokens",
      "collected_at": "2026-10-28T14:16:05.100252+00:00",
      "source_sha256": "3d05a42e5f1beb0ea05cb067c4ed673135313157efe4f2fb57d83975445e2d32",
      "text": "Back to Borrowing Borrow Tokens beginner Introduction Borrowing tokens from the Aave Protocol enables participants to access liquidity against supplied collateral tokens. This process requires maintaining sufficient collateral and understanding the associated risks, such as liquidation. Borrowers must maintain that their collateral remains adequate to cover the borrowed amount, as falling below the required collateralization level could lead to liquidation. The interest rates for borrowed tokens are dynamically determined by the protocol based on factors like the borrow utilization rate and governance parameters, which can change through community decisions. Borrowing can be performed through protocol smart contracts or through a frontend such as the Aave Labs interface by performing the following steps: Step 1: Connect Wallet To begin, press ‘Connect Wallet’ and select the Ethereum wallet provider corresponding to the wallet holding the collateralized tokens. Step 2: Select Token to Borrow Once connected, navigate to the ‘Dashboard’ and locate the ‘Assets to Borrow’ table. This table lists the available tokens for borrowing, along with key parameters such as available amount, interest rates, and your health factor. The interest rates displayed here are influenced by the borrow utilization rate, which measures the proportion of assets currently borrowed against the total supplied in the pool. As liquidity is borrowed or repaid, these rates are dynamically adjusted to reflect current market conditions. Select the token you wish to borrow. Step 3: Review Borrow Parameters Before proceeding, review the borrow parameters including the Loan-to-Value (LTV) ratio, Liquidation Threshold (LT) ratio, and your current health factor. These parameters are crucial for maintaining sufficient collateral and avoiding liquidation. If you are borrowing a network base asset (e.g., ETH), you will first need to approve the WrappedTokenGateway contract. This approval enables the contract to perform a credit delegation, which performs a borrow and unwraps to the base asset in a single transaction. Step 4: Confirm Borrow Transaction Enter the amount you wish to borrow and confirm the transaction in your wallet. Upon confirmation, the borrowed tokens will be transferred to your wallet. It's important to note that interest on the borrowed tokens begins to accrue immediately and is dynamically adjusted based on the borrow utilization rate. Step 5: Monitor Health Factor Regularly monitor your health factor from the ‘Dashboard’ to verify that your collateral remains sufficient. If your health factor drops, consider supplying more collateral or repaying part of your borrow position to avoid liquidation. The health",
      "score": 1.1264413832677036
    },
    {
      "id": "DOC_LIQ_001",
      "title": "Health Factor & Liquidations | Aave",
      "url": "https://aave.com/help/borrowing/liquidations",
      "collected_at": "2026-10-28T14:16:07.023365+00:00",
      "source_sha256": "29031b86b53d3b90c456e0eb91dafc75cdacb68928b4f776eb590eff301f3b25",
      "text": "debt values are at least $2,000 each. Up to 100% of debt can be liquidated when the health factor is 0.95 or below, OR when either the collateral or debt value is below $2,000. During liquidation, the liquidator repays debt on behalf of the borrower and receives an equivalent value plus a liquidation bonus from the borrower's collateral. To prevent dust accumulation, partial liquidations must leave at least $1,000 worth of both collateral and debt remaining—otherwise, the position must be fully cleared. Liquidations are permissionless, meaning any network participant can initiate the process when a borrow position is eligible for liquidation. Liquidations within Aave are highly competitive, requiring a deep understanding of the protocol and technical proficiency. Liquidators must actively monitor borrow positions, quickly react to changes in oracle prices, collateral balances, and protocol parameters, and submit transactions with high priority in the attempt to be first to execute the liquidation. Due to the competitive nature, successful liquidations often necessitate custom-coded bots or scripts that automate monitoring and execution. Developers interested in building liquidation bots or learning more about the process can find guidance and resources in the Aave Developer Documentation. Related Borrow Tokens beginner Maintain overcollateralised borrow positions. 4 min read Repay Tokens beginner Repay active borrow positions. 3 min read Efficiency Mode (E-mode) intermediate Borrowing in Efficiency Mode (E-mode). 3 min read",
      "score": 1.0573187923167777
    },
    {
      "id": "DOC_SUPPLY_001",
      "title": "Supply Tokens | Aave",
      "url": "https://aave.com/help/supplying/supply-tokens",
      "collected_at": "2026-10-28T14:16:02.570990+00:00",
      "source_sha256": "b59a3f775e241e2e9d829abc9fbd529afe72cc0d31bf94f8dd6a46a05d7b084c",
      "text": "message signature request in the connected wallet. Step 4: Perform Supply Transaction After approval, enter the amount you wish to supply and confirm, which will prompt a transaction in the connected wallet. Your supplied tokens are then added to the Aave liquidity pool, where they are made available for borrowers. The supplied tokens will start earning interest immediately, which can be monitored from the ‘Dashboard’ tab. Related Withdraw Tokens beginner Withdraw tokens from the Aave Protocol. 4 min read Toggle Collateral Status intermediate Toggle collateral status of supply positions. 4 min read Isolation Mode beginner Supply isolated collateral assets. 3 min read",
      "score": 0.5697788296853195
    }
  ],
  "sql": "",
  "query_result": null
}
```
