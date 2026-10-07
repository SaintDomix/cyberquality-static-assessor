from cyberquality.models import ResponseSnapshot, TLSInfo
from cyberquality.rules.headers import evaluate


def snapshot(headers: dict[str, str]) -> ResponseSnapshot:
    return ResponseSnapshot(
        target_url="https://example.test",
        final_url="https://example.test",
        status_code=200,
        headers={k.lower(): v for k, v in headers.items()},
        set_cookie_headers=[],
        elapsed_ms=10,
        collected_at="2026-10-07T00:00:00+00:00",
        tls=TLSInfo(enabled=True, days_until_expiry=90),
    )


def test_hardened_headers_pass_core_checks():
    result = evaluate(
        snapshot(
            {
                "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none'",
                "X-Content-Type-Options": "nosniff",
                "X-Frame-Options": "DENY",
                "Referrer-Policy": "strict-origin-when-cross-origin",
                "Permissions-Policy": "camera=()",
            }
        )
    )
    assert all(item.status.value == "pass" for item in result)


def test_missing_csp_fails():
    result = evaluate(snapshot({"X-Content-Type-Options": "nosniff"}))
    csp = next(item for item in result if item.rule_id == "HDR-001")
    assert csp.status.value == "fail"
