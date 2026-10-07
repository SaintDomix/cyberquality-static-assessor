from __future__ import annotations

from urllib.parse import urlparse

from cyberquality.models import ResponseSnapshot, Severity

from .common import finding, header


def evaluate(snapshot: ResponseSnapshot):
    findings = []
    is_https = urlparse(snapshot.final_url).scheme.lower() == "https"

    findings.append(
        finding(
            rule_id="TRN-001",
            category="Transport Security",
            title="HTTPS transport",
            severity=Severity.HIGH,
            passed=is_https,
            description="Sensitive educational-platform traffic should be protected with HTTPS.",
            evidence=f"Final URL: {snapshot.final_url}",
            recommendation="Serve the platform over HTTPS and redirect HTTP requests to HTTPS.",
            source="Final request URL",
        )
    )

    hsts = header(snapshot, "strict-transport-security")
    findings.append(
        finding(
            rule_id="TRN-002",
            category="Transport Security",
            title="HTTP Strict Transport Security (HSTS)",
            severity=Severity.MEDIUM,
            passed=(bool(hsts) if is_https else None),
            description="HSTS instructs browsers to use HTTPS for future requests.",
            evidence=(f"Strict-Transport-Security: {hsts}" if hsts else "Header not present"),
            recommendation="Configure Strict-Transport-Security with an appropriate max-age after HTTPS is stable.",
        )
    )

    tls = snapshot.tls
    if not is_https:
        expiry_passed = None
        expiry_evidence = "TLS certificate not applicable to an HTTP target"
    elif tls.error:
        expiry_passed = False
        expiry_evidence = f"TLS inspection error: {tls.error}"
    elif tls.days_until_expiry is None:
        expiry_passed = False
        expiry_evidence = "Certificate expiry could not be determined"
    else:
        expiry_passed = tls.days_until_expiry >= 30
        expiry_evidence = f"Certificate expires in {tls.days_until_expiry} days ({tls.expires_at})"

    findings.append(
        finding(
            rule_id="TRN-003",
            category="Transport Security",
            title="TLS certificate validity window",
            severity=Severity.MEDIUM,
            passed=expiry_passed,
            description="Certificates close to expiry can interrupt secure access and create operational risk.",
            evidence=expiry_evidence,
            recommendation="Renew certificates before expiry and automate renewal where possible.",
            source="TLS handshake",
        )
    )
    return findings
