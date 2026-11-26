"""Register human-reviewed fixed drafts and evaluate a frozen checker."""

import argparse
from collections import Counter, defaultdict
from dataclasses import asdict
from hashlib import file_digest, sha256
import json
from pathlib import Path
import unicodedata

from .benchmark import load_benchmark, save_benchmark
from .database import Database
from .models import Draft, Issue, QueryResult, QuerySpec
from .review import content_hash
from .verifier_replay import ALIASES, verify_candidate


FINAL_DIR = Path("data/benchmark/checker-final")
LEGACY_REPLAY = Path("runs/claude-full-20261110-retry-v1/replay_candidates.jsonl")
DATABASE = Path("data/processed/aave.duckdb")
CHUNKS = Path("data/documents/chunks.json")
STRESS = Path("data/benchmark/stress.jsonl")
REPLAY_DEADLINE = 120.
EVIDENCE_ROOTS = 6
SQL_PAIRS = 10
TARGET_CODES = {
    **ALIASES,
    "missing_citation": {"citation_id", "missing_citation", "missing_claims"},
    "irrelevant_source": {"irrelevant_source", "citation_id", "unsupported_claim", "numeric_link"},
    "contradiction": {"contradiction", "unsupported_claim", "numeric_mismatch"},
    "scope": {"scope", "coverage", "time_range", "time_filter", "asset_filter"},
    "causation": {"causation", "unsupported_claim"},
    "numeric_link": {"numeric_link", "numeric_mismatch", "citation_id"},
    "numeric_mismatch": {"numeric_mismatch"},
    "asset_attribution": {"asset_attribution", "asset_mismatch", "answer_asset_error", "wrong_asset_attribution"},
    "other": set(),
}


def _file_hash(path):
    with path.open("rb") as stream:
        return file_digest(stream, "sha256").hexdigest()


def _read_json(path):
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _write_new(path, value):
    with path.open("x", encoding="utf-8") as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write("\n")


def _unique_index(rows, field, kind):
    index = {row[field]: row for row in rows}
    if len(index) != len(rows):
        raise ValueError(f"Duplicate {kind} IDs")
    return index


def _normalized(value):
    return unicodedata.normalize("NFC", " ".join(value.casefold().split()))


def draft_hash(draft):
    # This serialization matches verify_candidate's digest of the exact Draft.
    return sha256(json.dumps(draft, sort_keys=True, default=str).encode()).hexdigest()


def _restore(value):
    fields = dict(value)
    fields["spec"] = QuerySpec(**fields["spec"])
    if fields["query_result"] is not None:
        fields["query_result"] = QueryResult(**fields["query_result"])
    fields["issues"] = [Issue(**item) for item in fields["issues"]]
    return Draft(**fields)


def export_case_reviews(rows, destination):
    destination.mkdir(parents=True, exist_ok=False)
    items = [
        {"id": row["id"], "content_sha256": content_hash(row), "has_error": None,
         "target_error": None, "notes": ""}
        for row in rows
    ]
    booklet = [
        "# Phiếu kiểm tra bản nháp Aave",
        "",
        "Kiểm tra câu hỏi, câu trả lời, nguồn được trích, phạm vi và kết quả SQL.",
        "Tự chấm từng bản trước khi trao đổi với người duyệt còn lại. "
        "Không tra cảnh báo hoặc điểm của checker.",
        "Trong JSON, điền tên và xác nhận tự chấm ở independent_confirmation. "
        "Ghi has_error là true nếu có lỗi và false nếu bản nháp đúng. "
        "Ghi target_error cho bản sai và null cho bản đúng. "
        "Mỗi mục cần notes nêu lỗi hoặc lý do bản đúng, kèm bằng chứng đã đối chiếu.",
        "",
        "Mã lỗi: " + ", ".join(TARGET_CODES) + ". Nếu không có mã phù hợp, dùng other và mô tả cụ thể.",
        "",
    ]
    for row in rows:
        draft = row["draft"]
        visible = {key: draft[key] for key in ("question", "answer", "claims", "sql", "query_result", "documents")}
        booklet += [f"## {row['id']}", "", "```json",
                     json.dumps(visible, ensure_ascii=False, indent=2), "```", ""]
    for slot in (1, 2):
        _write_new(destination / f"reviewer-{slot}.json",
                   {"schema_version": 1, "reviewer_name": "", "independent_confirmation": False, "items": items})
        (destination / f"reviewer-{slot}.md").write_text("\n".join(booklet), encoding="utf-8")


def review_labels(rows, first, second, require_pairs=False):
    cases = _unique_index(rows, "id", "case")
    names = [_normalized(packet.get("reviewer_name", "")) for packet in (first, second)]
    if (not all(names) or names[0] == names[1] or
            any(packet.get("independent_confirmation") is not True or packet.get("original_reviewer_label")
                for packet in (first, second))):
        raise ValueError("Two distinct named independent human reviewers must confirm their assessments")

    outcomes = []
    for packet in (first, second):
        items = _unique_index(packet["items"], "id", "review item")
        if items.keys() != cases.keys():
            raise ValueError("Review items must cover the exact case set")
        decisions = {}
        for case_id, row in cases.items():
            item = items[case_id]
            if item.get("content_sha256") != content_hash(row):
                raise ValueError(f"Reviewed case content changed: {case_id}")
            has_error, target = item.get("has_error"), item.get("target_error")
            if (type(has_error) is not bool or not item.get("notes", "").strip() or
                    (has_error and (not isinstance(target, str) or target not in TARGET_CODES)) or
                    (not has_error and target is not None)):
                raise ValueError(f"Review needs a decision, target when applicable and evidence note: {case_id}")
            decisions[case_id] = {"has_error": has_error, "target_error": target}
        outcomes.append(decisions)
    disagreements = [key for key in cases if outcomes[0][key] != outcomes[1][key]]
    if disagreements:
        raise ValueError("Reviewers disagree on " + ", ".join(disagreements))
    if require_pairs:
        groups = defaultdict(list)
        for row in rows:
            pair_id = row.get("pair_id", row["root_id"])
            groups[(row["group"], pair_id)].append(outcomes[0][row["id"]]["has_error"])
        if any(sorted(group) != [False, True] for group in groups.values()):
            raise ValueError("Each reviewed pair must have one verified correct and one verified incorrect draft")
    return outcomes[0]


def _source_hashes(root):
    return {str(path.as_posix()): _file_hash(root / path)
            for path in (DATABASE, CHUNKS, STRESS, LEGACY_REPLAY)}


def _validate_holdout_shape(rows):
    _unique_index(rows, "id", "case")
    if Counter(row["group"] for row in rows) != {"sql": 2 * SQL_PAIRS, "evidence": 2 * EVIDENCE_ROOTS}:
        raise ValueError(f"Held-out checker requires {SQL_PAIRS} SQL pairs and {EVIDENCE_ROOTS} evidence pairs")
    evidence = Counter(row["root_id"] for row in rows if row["group"] == "evidence")
    if len(evidence) != EVIDENCE_ROOTS or any(count != 2 for count in evidence.values()):
        raise ValueError(f"Held-out checker requires {EVIDENCE_ROOTS} evidence roots with two drafts each")
    if any(row["split"] != "test" for row in rows):
        raise ValueError("Held-out checker cases must all belong to the test split")


def _checked_cases(root):
    directory = root / FINAL_DIR
    rows = load_benchmark(directory / "cases.jsonl")
    _validate_holdout_shape(rows)
    manifest = _read_json(directory / "preparation.json")
    if (manifest["cases_sha256"] != _file_hash(directory / "cases.jsonl") or
            manifest["source_hashes"] != _source_hashes(root)):
        raise ValueError("Held-out case preparation or source changed; prepare and review a fresh version")
    return rows, manifest


def approve_cases(root, first, second):
    rows, manifest = _checked_cases(root)
    reviewers = [_read_json(path) for path in (first, second)]
    labels = review_labels(rows, *reviewers, require_pairs=True)
    _write_new(root / FINAL_DIR / "approved.json",
               {"cases_sha256": manifest["cases_sha256"], "reviewers": reviewers, "labels": labels})
    return len(labels)


def checker_lock_inputs(root):
    """Validate the approved exact corpus and return artifacts to pin at freeze."""
    root = Path(root)
    rows, manifest = _checked_cases(root)
    path = root / FINAL_DIR / "approved.json"
    if not path.is_file():
        raise FileNotFoundError("Held-out checker approval is missing; collect both independent case reviews first")
    approval = _read_json(path)
    labels = review_labels(rows, *approval["reviewers"], require_pairs=True)
    if approval["cases_sha256"] != manifest["cases_sha256"] or approval["labels"] != labels:
        raise ValueError("Held-out checker approvals no longer match the reviewed corpus")
    return {**manifest["source_hashes"],
            **{(FINAL_DIR / name).as_posix(): _file_hash(root / FINAL_DIR / name)
               for name in ("cases.jsonl", "preparation.json", "approved.json")}}


def summarize_replay(cases, labels, replay):
    by_id = _unique_index(replay, "case_id", "replay coverage")
    if by_id.keys() != {row["id"] for row in cases} or by_id.keys() != labels.keys():
        raise ValueError("Replay coverage differs from the labeled case set")
    summary = {}
    for group in sorted({row["group"] for row in cases}):
        group_cases = [row for row in cases if row["group"] == group]
        result = {"question_roots": len({row["root_id"] for row in group_cases}),
                  "scheduled": len(group_cases), "target_code_hits": 0, "target_code_candidates": []}
        for label in ("correct", "incorrect"):
            result[label] = dict.fromkeys(("total", "fail", "pass", "insufficient", "timeout", "error"), 0)
        for case in group_cases:
            row, label = by_id[case["id"]], labels[case["id"]]
            if row["candidate_sha256"] != draft_hash(case["draft"]):
                raise ValueError(f"Checker replay used another draft: {case['id']}")
            bucket = result["incorrect" if label["has_error"] else "correct"]
            state = row["execution_status"]
            outcome = row["verdict"] if state == "completed" else state
            if outcome not in {"fail", "pass", "insufficient", "timeout", "error"}:
                raise ValueError(f"Unknown checker outcome: {outcome}")
            bucket["total"] += 1
            bucket[outcome] += 1
            if label["has_error"] and outcome == "fail":
                target = label["target_error"]
                hit = any(issue["code"] in TARGET_CODES[target] for issue in row["issues"])
                result["target_code_hits"] += hit
                result["target_code_candidates"].append(
                    {"id": case["id"], "expected": target, "code_matched": hit, "issues": row["issues"]}
                )
        result["target_code_total"] = result["incorrect"]["total"]
        summary[group] = result
    return summary


def _report(summary):
    rows = [
        "# Hiệu quả checker trên các bản nháp độc lập",
        "",
        "| Nhóm | Câu gốc | Nhãn đã xác minh | Số bản | Báo lỗi | Cho qua | Chưa đủ căn cứ | Timeout | Lỗi chạy |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for group, result in summary.items():
        for key, label in (("correct", "Đúng"), ("incorrect", "Sai")):
            counts = result[key]
            total = counts["total"]
            fractions = " | ".join(f"{counts[k]}/{total}" for k in ("fail", "pass", "insufficient", "timeout", "error"))
            name = "SQL" if group == "sql" else "Dẫn chứng"
            rows.append(f"| {name} | {result['question_roots']} | {label} | {total} | {fractions} |")
    rows += ["", "Báo lỗi trên bản sai được tính là phát hiện. Báo lỗi trên bản đúng được tính là báo nhầm.",
             "", "| Nhóm | Mã cảnh báo khớp lỗi mục tiêu / tổng bản sai |",
             "|---|---:|"]
    for group, result in summary.items():
        name = "SQL" if group == "sql" else "Dẫn chứng"
        rows.append(f"| {name} | {result['target_code_hits']}/{result['target_code_total']} |")
    rows += ["", "Đối chiếu nội dung từng cảnh báo trong summary.json trước khi kết luận checker đã chỉ ra đúng lỗi mục tiêu.", ""]
    return "\n".join(rows)


def _numeric_claim(text, result, column="value", row=0):
    return {
        "text": text, "citations": ["SQL1"],
        "numeric": {"value": result.rows[row][column], "unit": "USD",
                    "evidence_id": "SQL1", "row": row, "column": column},
    }


def _answer(claims):
    return " ".join(
        claim["text"] + "".join(f" [{source}]" for source in claim["citations"])
        for claim in claims
    )


def _case(case_id, root_id, pair_id, group, draft, split="test"):
    return {"id": case_id, "root_id": root_id, "pair_id": pair_id, "group": group,
            "split": split, "draft": asdict(draft)}


def _stress_cases(rows, db, availability):
    output = []
    for row in rows:
        question = row["question"]
        root_id = sha256(_normalized(question).encode()).hexdigest()[:16]
        # The scope is determined independently from the variant query.
        asset, = [asset for asset in ("USDT", "DAI") if asset in question]
        aggregation = "range" if "nhỏ nhất" in question else "max"
        spec = QuerySpec(kind="data", metric="supplied_usd", assets=[asset], aggregation=aggregation,
                         start="2025-01-01T00:00:00Z", end="2026-01-01T00:00:00Z", unit="USD")
        results = [db.query(row[key]) for key in ("correct_sql", "wrong_sql")]
        if results[0].rows != row["reference_rows"] or results[1].rows == results[0].rows:
            raise ValueError(f"SQL fixture is invalid or no longer reproduces: {row['id']}")
        for index, sql_key in enumerate(("correct_sql", "wrong_sql")):
            result = results[index]
            claim = _numeric_claim(f"{result.rows[0]['value']:,.2f} USD", result)
            draft = Draft(question=question, spec=spec, sql=row[sql_key], query_result=result,
                          claims=[claim], answer=_answer([claim]), planning={"availability": availability})
            # Alternate variant order without embedding a label in the case identifier.
            slot = "AB"[(int(row["id"][1:]) + index) % 2]
            output.append(_case(f"{row['id']}-{slot}", root_id, row["id"], "sql", draft))
    return output


def _evidence_cases(designs, db, docs, availability):
    cases = []
    for index, row in enumerate(designs, 1):
        question = row["question"]
        spec = QuerySpec(**row["spec"])
        sql = row.get("sql", "")
        result = db.query(sql) if sql else None
        documents = [docs[doc_id] for doc_id in row.get("documents", [])]
        case_id = f"EC{index:02}"
        for side, variant in enumerate(row["variants"]):
            claims = []
            for item in variant:
                if "column" in item:
                    result_row = item.get("row", 0)
                    text = item["text"].format(**result.rows[result_row])
                    claim = _numeric_claim(text, result, item["column"], result_row)
                    claim["citations"] = item["citations"]
                else:
                    claim = {"text": item["text"], "citations": item["citations"]}
                claims.append(claim)
            draft = Draft(question=question, spec=spec, sql=sql, query_result=result, documents=documents,
                          answer=_answer(claims), claims=claims, planning={"availability": availability})
            cases.append(_case(f"{case_id}-{'AB'[(side + index) % 2]}", case_id, case_id, "evidence", draft))
    return cases


def prepare_cases(root, designs_path):
    root = Path(root)
    directory = root / FINAL_DIR
    if directory.exists():
        raise FileExistsError("Preserve existing review files and version the replacement intentionally")
    sources = _source_hashes(root)
    db = Database(root / DATABASE)
    chunks = {chunk["id"]: chunk for chunk in _read_json(root / CHUNKS)}
    availability = {
        "market_hourly": db.query("SELECT * FROM coverage ORDER BY asset").rows,
        "liquidation_events": db.query("SELECT MIN(time) AS first_event_utc, MAX(time) AS last_event_utc "
                                       "FROM liquidation_events").rows[0],
    }
    stress = [row for row in load_benchmark(root / STRESS) if row["split"] == "test"]
    designs = _read_json(designs_path)
    if len(designs) != EVIDENCE_ROOTS or any(len(row["variants"]) != 2 for row in designs):
        raise ValueError(f"Provide {EVIDENCE_ROOTS} distinct evidence questions with two variants each")
    legacy = load_benchmark(root / LEGACY_REPLAY)
    used_questions = {_normalized(row["draft"]["question"]) for row in legacy}
    used_ids = {row["id"].rsplit("-", maxsplit=1)[0] for row in legacy}
    if (len({_normalized(row["question"]) for row in designs}) != EVIDENCE_ROOTS or
            any(_normalized(row["question"]) in used_questions for row in stress + designs) or
            any(row["id"] in used_ids for row in stress)):
        raise ValueError("A test root or SQL pair overlaps known dev replay")
    cases = _stress_cases(stress, db, availability) + _evidence_cases(designs, db, chunks, availability)
    cases.sort(key=lambda row: row["id"])
    _validate_holdout_shape(cases)
    if _source_hashes(root) != sources:
        raise ValueError("Local sources changed while preparing the case set")
    directory.mkdir(parents=True, exist_ok=False)
    save_benchmark(cases, directory / "cases.jsonl")
    _write_new(directory / "preparation.json",
               {"source_hashes": sources, "cases_sha256": _file_hash(directory / "cases.jsonl"),
                "prior_replay_check": "No exact question or SQL pair ID from historical dev replay",
                "sql_source": "Rows tagged test in stress.jsonl; previous offline SQL audit is not checker exposure"})
    export_case_reviews(cases, directory / "review")
    return Counter(row["group"] for row in cases)


def export_legacy_reviews(root, destination):
    usable = [row for row in load_benchmark(root / LEGACY_REPLAY)
              if row["group"] in {"evidence_stress", "sql_stress"}]
    next_number = Counter()
    cases = []
    for row in usable:
        group = "sql" if row["group"] == "sql_stress" else "evidence"
        next_number[group] += 1
        root_id = sha256(_normalized(row["draft"]["question"]).encode()).hexdigest()[:16]
        cases.append(_case(f"DEV-{group}-{next_number[group]:02}", root_id, row["id"].rsplit("-", maxsplit=1)[0],
                           group, _restore(row["draft"]), split="dev"))
    export_case_reviews(cases, destination)
    save_benchmark(cases, destination / "cases.jsonl")
    return len(cases)


def run_replay(root, out, resume=False):
    from .cli import analyst_at, verify_final_lock

    lock = verify_final_lock(root)
    # Validate both the full experimental freeze and the exact labeled drafts before any model call.
    expected_files = checker_lock_inputs(root)
    if lock["checker_inputs"] != expected_files:
        raise ValueError("Checker data or approvals changed since freeze")
    cases, _ = _checked_cases(root)
    labels = _read_json(root / FINAL_DIR / "approved.json")["labels"]
    rows_path = out / "replay.jsonl"
    run_manifest = {"lock": lock, "candidate_ids": [row["id"] for row in cases], "deadline": REPLAY_DEADLINE}
    if resume:
        if _read_json(out / "config.json") != run_manifest:
            raise ValueError("Checker replay configuration changed")
    else:
        out.mkdir(parents=True, exist_ok=False)
        _write_new(out / "config.json", run_manifest)
    if (out / "summary.json").exists():
        raise FileExistsError("Checker replay already summarized")
    results = load_benchmark(rows_path) if rows_path.exists() else []
    completed = _unique_index(results, "case_id", "replay checkpoint")
    case_hashes = {row["id"]: draft_hash(row["draft"]) for row in cases}
    if any(case_hashes.get(case_id) != row["candidate_sha256"] for case_id, row in completed.items()):
        raise ValueError("Checker replay checkpoint contains changed or unexpected drafts")
    analyst = analyst_at(root, deadline=REPLAY_DEADLINE)
    if analyst.llm.config() != lock["llm_config"]:
        raise ValueError("Checker model differs from freeze")
    with rows_path.open("a", encoding="utf-8") as stream:
        for row in cases:
            if row["id"] in completed:
                continue
            verdict = verify_candidate(_restore(row["draft"]), analyst, variant="full", deadline=REPLAY_DEADLINE)
            verdict["case_id"] = row["id"]
            stream.write(json.dumps(verdict, ensure_ascii=False) + "\n")
            stream.flush()
            results.append(verdict)
    if verify_final_lock(root) != lock:
        raise ValueError("Frozen inputs changed during checker replay")
    summary = summarize_replay(cases, labels, results)
    report_path = out / "checker-report.md"
    report_path.write_text(_report(summary), encoding="utf-8")
    _write_new(out / "summary.json", summary)
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=Path("."), type=Path)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("prepare").add_argument("designs", type=Path)
    commands.add_parser("export-dev").add_argument("destination", type=Path)
    approval = commands.add_parser("approve")
    approval.add_argument("reviewer_1", type=Path)
    approval.add_argument("reviewer_2", type=Path)
    dev_review = commands.add_parser("resolve-dev")
    dev_review.add_argument("destination", type=Path)
    replay = commands.add_parser("replay")
    replay.add_argument("out", type=Path)
    replay.add_argument("--resume", action="store_true")
    args = parser.parse_args()
    if args.command == "prepare":
        result = prepare_cases(args.root, args.designs)
    elif args.command == "export-dev":
        result = export_legacy_reviews(args.root, args.destination)
    elif args.command == "approve":
        result = approve_cases(args.root, args.reviewer_1, args.reviewer_2)
    elif args.command == "resolve-dev":
        rows = load_benchmark(args.destination / "cases.jsonl")
        packets = [_read_json(args.destination / f"reviewer-{slot}.json") for slot in (1, 2)]
        labels = review_labels(rows, *packets)
        _write_new(args.destination / "labels.json", {"reviewers": packets, "labels": labels})
        result = len(labels)
    else:
        result = run_replay(args.root, args.out, resume=args.resume)
    print(json.dumps(result, ensure_ascii=False))


if __name__ == "__main__":
    main()
