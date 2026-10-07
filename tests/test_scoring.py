from cyberquality.models import Finding, Severity, Status
from cyberquality.scoring import calculate_scores, grade_for


def f(rule_id: str, status: Status, severity: Severity = Severity.HIGH) -> Finding:
    return Finding(
        rule_id=rule_id,
        category="Test",
        title="test",
        severity=severity,
        status=status,
        description="",
        evidence="",
        recommendation="",
    )


def test_weighted_score_rewards_passed_controls():
    score, dimensions = calculate_scores(
        [f("A", Status.PASS), f("B", Status.FAIL), f("C", Status.PASS, Severity.LOW)]
    )
    assert score == 53
    assert dimensions["Test"] == 53


def test_not_applicable_is_excluded():
    score, _ = calculate_scores([f("A", Status.PASS), f("B", Status.NOT_APPLICABLE)])
    assert score == 100


def test_grade_boundaries():
    assert grade_for(90) == "A"
    assert grade_for(80) == "B"
    assert grade_for(70) == "C"
    assert grade_for(60) == "D"
    assert grade_for(59) == "F"
