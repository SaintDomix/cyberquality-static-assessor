from __future__ import annotations

from cyberquality.models import ResponseSnapshot, Severity

from .common import finding

SESSION_MARKERS = ("session", "moodle", "auth", "token", "sid", "jwt")


def _candidate_cookies(snapshot: ResponseSnapshot) -> list[str]:
    if not snapshot.set_cookie_headers:
        return []
    session_like = [
        cookie
        for cookie in snapshot.set_cookie_headers
        if any(marker in cookie.split("=", 1)[0].lower() for marker in SESSION_MARKERS)
    ]
    return session_like or snapshot.set_cookie_headers


def evaluate(snapshot: ResponseSnapshot):
    cookies = _candidate_cookies(snapshot)
    if not cookies:
        common = dict(
            category="Session Security",
            passed=None,
            evidence="No session-like Set-Cookie header observed in the assessed response",
            source="Set-Cookie headers",
        )
        return [
            finding(
                rule_id="SES-001",
                title="Secure cookie attribute",
                severity=Severity.HIGH,
                description="Secure prevents cookies from being sent over unencrypted HTTP.",
                recommendation="Mark authentication/session cookies as Secure when HTTPS is used.",
                **common,
            ),
            finding(
                rule_id="SES-002",
                title="HttpOnly cookie attribute",
                severity=Severity.HIGH,
                description="HttpOnly reduces access to session cookies from client-side scripts.",
                recommendation="Mark authentication/session cookies as HttpOnly.",
                **common,
            ),
            finding(
                rule_id="SES-003",
                title="SameSite cookie attribute",
                severity=Severity.MEDIUM,
                description="SameSite can reduce cross-site request risks for session cookies.",
                recommendation="Set an appropriate SameSite value (Lax or Strict unless cross-site use is required).",
                **common,
            ),
        ]

    secure_ok = all("; secure" in cookie.lower() or cookie.lower().endswith(";secure") for cookie in cookies)
    httponly_ok = all("httponly" in cookie.lower() for cookie in cookies)
    samesite_ok = all("samesite=" in cookie.lower() for cookie in cookies)
    names = ", ".join(cookie.split("=", 1)[0] for cookie in cookies)

    return [
        finding(
            rule_id="SES-001",
            category="Session Security",
            title="Secure cookie attribute",
            severity=Severity.HIGH,
            passed=secure_ok,
            description="Secure prevents cookies from being sent over unencrypted HTTP.",
            evidence=f"Assessed cookies: {names}; Secure present on all: {secure_ok}",
            recommendation="Mark authentication/session cookies as Secure when HTTPS is used.",
            source="Set-Cookie headers",
        ),
        finding(
            rule_id="SES-002",
            category="Session Security",
            title="HttpOnly cookie attribute",
            severity=Severity.HIGH,
            passed=httponly_ok,
            description="HttpOnly reduces access to session cookies from client-side scripts.",
            evidence=f"Assessed cookies: {names}; HttpOnly present on all: {httponly_ok}",
            recommendation="Mark authentication/session cookies as HttpOnly.",
            source="Set-Cookie headers",
        ),
        finding(
            rule_id="SES-003",
            category="Session Security",
            title="SameSite cookie attribute",
            severity=Severity.MEDIUM,
            passed=samesite_ok,
            description="SameSite can reduce cross-site request risks for session cookies.",
            evidence=f"Assessed cookies: {names}; SameSite present on all: {samesite_ok}",
            recommendation="Set an appropriate SameSite value (Lax or Strict unless cross-site use is required).",
            source="Set-Cookie headers",
        ),
    ]
