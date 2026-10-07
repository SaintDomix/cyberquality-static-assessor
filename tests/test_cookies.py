from cyberquality.models import ResponseSnapshot, TLSInfo
from cyberquality.rules.cookies import evaluate


def make(cookie: str) -> ResponseSnapshot:
    return ResponseSnapshot(
        target_url="https://example.test",
        final_url="https://example.test",
        status_code=200,
        headers={},
        set_cookie_headers=[cookie],
        elapsed_ms=5,
        collected_at="2026-10-07T00:00:00+00:00",
        tls=TLSInfo(enabled=True, days_until_expiry=90),
    )


def test_secure_session_cookie_passes_all_cookie_rules():
    findings = evaluate(make("MoodleSession=abc; Path=/; Secure; HttpOnly; SameSite=Lax"))
    assert all(item.status.value == "pass" for item in findings)


def test_weak_session_cookie_fails_all_cookie_rules():
    findings = evaluate(make("MoodleSession=abc; Path=/"))
    assert all(item.status.value == "fail" for item in findings)
