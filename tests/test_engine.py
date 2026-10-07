from cyberquality.engine import assess_snapshot
from cyberquality.models import ResponseSnapshot, TLSInfo


def test_engine_returns_traceable_result():
    snap = ResponseSnapshot(
        target_url="http://example.test",
        final_url="http://example.test",
        status_code=200,
        headers={
            "server": "Apache/2.4.58",
            "x-powered-by": "PHP/8.2",
            "access-control-allow-origin": "*",
        },
        set_cookie_headers=["MoodleSession=abc; Path=/"],
        elapsed_ms=12.5,
        collected_at="2026-10-07T00:00:00+00:00",
        tls=TLSInfo(enabled=False),
    )
    result = assess_snapshot(snap)
    assert result.overall_score < 50
    assert result.counts["high"] >= 1
    assert any(item.rule_id == "TRN-001" for item in result.findings)
    assert result.target_url == "http://example.test"
