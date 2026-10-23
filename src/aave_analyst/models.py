from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class QuerySpec:
    kind: str = "mixed"
    metric: str = ""
    assets: list[str] = field(default_factory=list)
    start: str | None = None
    end: str | None = None
    unit: str = ""
    aggregation: str = ""
    grain: str = ""
    retrieval_query: str = ""
    clarification: str = ""


@dataclass
class QueryResult:
    columns: list[str] = field(default_factory=list)
    rows: list[dict] = field(default_factory=list)
    truncated: bool = False
    total_rows: int = 0


@dataclass
class Issue:
    code: str
    message: str
    action: str = "answer"


@dataclass
class Draft:
    question: str
    spec: QuerySpec
    sql: str = ""
    query_result: QueryResult | None = None
    documents: list[dict] = field(default_factory=list)
    answer: str = ""
    claims: list[dict] = field(default_factory=list)
    refused: bool = False
    issues: list[Issue] = field(default_factory=list)
    elapsed: float = 0.
    usage: list[dict] = field(default_factory=list)
    error: str = ""
    tools: list[dict] = field(default_factory=list)
    planning: dict = field(default_factory=dict)


@dataclass
class RunResult:
    mode: str
    draft: Draft
    status: str
    repairs: int = 0
    issues: list[Issue] = field(default_factory=list)
    trace: list[dict] = field(default_factory=list)
    elapsed: float = 0.
    usage: list[dict] = field(default_factory=list)
    error: str = ""
    tools: list[dict] = field(default_factory=list)


def serializable(obj: Any):
    if hasattr(obj,"__dataclass_fields__"):
        return asdict(obj)
    raise TypeError(type(obj).__name__)
