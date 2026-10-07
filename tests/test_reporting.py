from pathlib import Path

from cyberquality.engine import assess_snapshot
from cyberquality.models import ResponseSnapshot, TLSInfo
from cyberquality.reporting import write_json, write_pdf


def test_reports_are_created(tmp_path: Path):
    snap = ResponseSnapshot(
        target_url="https://example.test",
        final_url="https://example.test",
        status_code=200,
        headers={
            "content-security-policy": "default-src 'self'; frame-ancestors 'none'",
            "x-content-type-options": "nosniff",
            "x-frame-options": "DENY",
            "referrer-policy": "same-origin",
            "permissions-policy": "camera=()",
            "strict-transport-security": "max-age=31536000",
        },
        set_cookie_headers=["MoodleSession=abc; Secure; HttpOnly; SameSite=Lax"],
        elapsed_ms=9,
        collected_at="2026-10-07T00:00:00+00:00",
        tls=TLSInfo(enabled=True, protocol="TLSv1.3", days_until_expiry=90),
    )
    result = assess_snapshot(snap)
    json_path = write_json(result, tmp_path / "result.json")
    pdf_path = write_pdf(result, tmp_path / "result.pdf")
    assert json_path.exists() and json_path.stat().st_size > 100
    assert pdf_path.exists() and pdf_path.stat().st_size > 1000
