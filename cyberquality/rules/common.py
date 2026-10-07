from __future__ import annotations

from cyberquality.models import Finding, ResponseSnapshot, Severity, Status


def finding(
    *,
    rule_id: str,
    category: str,
    title: str,
    severity: Severity,
    passed: bool | None,
    description: str,
    evidence: str,
    recommendation: str,
    source: str = "HTTP response",
) -> Finding:
    if passed is None:
        status = Status.NOT_APPLICABLE
    else:
        status = Status.PASS if passed else Status.FAIL
    return Finding(
        rule_id=rule_id,
        category=category,
        title=title,
        severity=severity,
        status=status,
        description=description,
        evidence=evidence,
        recommendation=recommendation,
        source=source,
    )


def header(snapshot: ResponseSnapshot, name: str) -> str | None:
    return snapshot.headers.get(name.lower())
