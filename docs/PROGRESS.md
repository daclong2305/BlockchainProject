# Execution ledger — docs/IMPLEMENTATION.md

- Ruling: work directly in the user-requested empty F:/Code/BlockchainProject, initialized on branch implementation. No existing checkout needs isolation.
- Ruling: preserve this ledger and test evidence rather than skill-specific shell scripts: Windows and a new repository have no base commit or existing plan workspace.
- Ruling: use Python venv with project-local TEMP/TMP; bundled Python lacks ensurepip. Dependencies are installed only in .venv.
- Ruling: use the same Haiku model for separate generation, verifier and judge prompts; disclose correlated-judge limitation and require independent human checks.
- Ruling: machine-generated benchmark references are provisional until two humans approve; do not silently run final research evaluation on unapproved gold.
- Complete: restore release and verify 146,914 market rows / 25,121 events / 20,159 distinct transactions. Five assets each have 14,592 benchmark hours, no grid gaps in that interval.
- Complete: three official Aave pages snapshotted; six BM25 chunks, URL/date/hash provenance.
- Complete: 60 unique provisional questions, correct 20/40 split, disjoint families and normalized templates; 20 separate provisional stress cases.
- Complete: B0/B1/P and three ablations; code+LLM SQL review, numeric/citation support checks, global two-repair limit, stale evidence replacement, timeouts/errors and actual tool/token logging.
- Complete: immutable paired experiment outputs, factual scorer, independent judge input, category/pair summaries, human sample and Cohen kappa reporting; Streamlit and CLI.
- Review: independent read-only reviewer found duplicated/leaked benchmark questions, lost error costs, deadline bypasses, refusal metric and missing lock file. Regression tests reproduced failures; fixes passed. Also corrected stress blank-answer setup and unit checks.
- Verification: offline scripted-model test on real source data repaired event COUNT(*)=158 to COUNT(DISTINCT tx_hash)=107 for August 2026 in one round. This is engineering verification, not a Bedrock research result.
- Verification: Streamlit initial render and missing-credential error handling passed AppTest; pip check passed. See final verification.json for final test count.
- External prerequisite: AWS us-east-1/default profile not present in this execution environment (ProfileNotFound); no paid inference calls or effectiveness results claimed.
- External prerequisite: two independent human approvals for gold and stress remain required. Freeze correctly rejects unreviewed Q001. No final test questions have been sent to an LLM.
- Ruling: keep this new standalone repository and files at the exact user-requested path; there is no base branch to merge or remote PR to create.
- Deferred: none of the independent review's substantive issues remain knowingly unfixed. Live Bedrock validation and research/human gold validation remain explicit external prerequisites, not passing checks.
