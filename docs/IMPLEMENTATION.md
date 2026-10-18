# Aave V3 implementation and experiment plan

Approved scope: Vietnamese QA, five V3 Ethereum assets (DAI, USDC, USDT, USDe, WETH), historical data, evidence, SQL semantic checks and at most two repairs. Benchmark interval [2025-01-01, 2026-09-01) UTC. No profitUSD, gas or APR in the main benchmark.

1. Restore release data-2026-09-15; normalize, audit, build DuckDB and data dictionary.
2. Snapshot Aave supply/borrow/liquidations help, chunk, index BM25.
3. Build 60 draft benchmark records (20 dev, 40 test), independently review gold and freeze test. Counts exact, USD equal after decimal half-up rounding to requested precision (default 2).
4. Implement shared draft and B0/B1.
5. Implement semantic SQL verification, per-claim evidence verification, bounded repair; P and three ablations.
6. Run paired experiments (40 questions x 6 modes x 3 repeats), factual scorer, independent judge prompt, human audit, summaries; Streamlit demo and reproducibility instructions.

Acceptance: offline integration tests cover event/transaction distinction, stocks vs flows, UTC boundaries, missing coverage, invalid evidence, stale repaired evidence, exhausted budgets, regressions, timeout and API errors. Live results require verified source data and human-approved benchmark. Never label fixtures or auto-generated references as validated research results.
