from __future__ import annotations

from collections import defaultdict

from .models import Finding, Severity, Status


def _score(findings: list[Finding]) -> int:
    applicable = [f for f in findings if f.status not in {Status.NOT_APPLICABLE, Status.INFO} and (f.weight or 0) > 0]
    if not applicable:
        return 100
    total = sum(f.weight or 0 for f in applicable)
    passed = sum((f.weight or 0) for f in applicable if f.status == Status.PASS)
    return round((passed / total) * 100) if total else 100


def calculate_scores(findings: list[Finding]) -> tuple[int, dict[str, int]]:
    dimensions: dict[str, list[Finding]] = defaultdict(list)
    for finding in findings:
        dimensions[finding.category].append(finding)
    return _score(findings), {category: _score(items) for category, items in sorted(dimensions.items())}


def grade_for(score: int) -> str:
    if score >= 90:
        return "A"
    if score >= 80:
        return "B"
    if score >= 70:
        return "C"
    if score >= 60:
        return "D"
    return "F"


def count_findings(findings: list[Finding]) -> dict[str, int]:
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0, "passed": 0, "not_applicable": 0}
    for finding in findings:
        if finding.status == Status.FAIL:
            if finding.severity in {Severity.CRITICAL, Severity.HIGH, Severity.MEDIUM, Severity.LOW}:
                counts[finding.severity.value] += 1
        elif finding.status == Status.PASS:
            counts["passed"] += 1
        elif finding.status == Status.NOT_APPLICABLE:
            counts["not_applicable"] += 1
    return counts
