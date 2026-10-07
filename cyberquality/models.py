from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class Severity(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class Status(str, Enum):
    PASS = "pass"
    FAIL = "fail"
    INFO = "info"
    NOT_APPLICABLE = "not_applicable"


SEVERITY_WEIGHTS: dict[Severity, int] = {
    Severity.CRITICAL: 10,
    Severity.HIGH: 7,
    Severity.MEDIUM: 4,
    Severity.LOW: 1,
    Severity.INFO: 0,
}


@dataclass(slots=True)
class TLSInfo:
    enabled: bool
    protocol: str | None = None
    cipher: str | None = None
    expires_at: str | None = None
    days_until_expiry: int | None = None
    error: str | None = None


@dataclass(slots=True)
class ResponseSnapshot:
    target_url: str
    final_url: str
    status_code: int
    headers: dict[str, str]
    set_cookie_headers: list[str]
    elapsed_ms: float
    collected_at: str
    tls: TLSInfo


@dataclass(slots=True)
class Finding:
    rule_id: str
    category: str
    title: str
    severity: Severity
    status: Status
    description: str
    evidence: str
    recommendation: str
    source: str = "HTTP response"
    weight: int | None = None
    observed_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def __post_init__(self) -> None:
        if self.weight is None:
            self.weight = SEVERITY_WEIGHTS[self.severity]

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["severity"] = self.severity.value
        data["status"] = self.status.value
        return data


@dataclass(slots=True)
class AssessmentResult:
    scanner_version: str
    target_url: str
    final_url: str
    collected_at: str
    http_status: int
    response_time_ms: float
    overall_score: int
    grade: str
    dimension_scores: dict[str, int]
    counts: dict[str, int]
    findings: list[Finding]
    tls: TLSInfo

    def to_dict(self) -> dict[str, Any]:
        return {
            "scanner_version": self.scanner_version,
            "target_url": self.target_url,
            "final_url": self.final_url,
            "collected_at": self.collected_at,
            "http_status": self.http_status,
            "response_time_ms": round(self.response_time_ms, 2),
            "overall_score": self.overall_score,
            "grade": self.grade,
            "dimension_scores": self.dimension_scores,
            "counts": self.counts,
            "tls": asdict(self.tls),
            "findings": [finding.to_dict() for finding in self.findings],
        }
