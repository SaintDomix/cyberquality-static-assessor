from __future__ import annotations

from . import __version__
from .collector import collect
from .models import AssessmentResult, ResponseSnapshot
from .rules import evaluate_all
from .scoring import calculate_scores, count_findings, grade_for


def assess_snapshot(snapshot: ResponseSnapshot) -> AssessmentResult:
    findings = evaluate_all(snapshot)
    overall_score, dimension_scores = calculate_scores(findings)
    return AssessmentResult(
        scanner_version=__version__,
        target_url=snapshot.target_url,
        final_url=snapshot.final_url,
        collected_at=snapshot.collected_at,
        http_status=snapshot.status_code,
        response_time_ms=snapshot.elapsed_ms,
        overall_score=overall_score,
        grade=grade_for(overall_score),
        dimension_scores=dimension_scores,
        counts=count_findings(findings),
        findings=findings,
        tls=snapshot.tls,
    )


def scan(url: str, *, timeout: float = 10.0, verify_tls: bool = True) -> AssessmentResult:
    return assess_snapshot(collect(url, timeout=timeout, verify_tls=verify_tls))
