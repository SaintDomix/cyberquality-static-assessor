from __future__ import annotations

from cyberquality.models import ResponseSnapshot, Severity

from .common import finding, header


def evaluate(snapshot: ResponseSnapshot):
    findings = []

    csp = header(snapshot, "content-security-policy")
    findings.append(
        finding(
            rule_id="HDR-001",
            category="Web Security Headers",
            title="Content-Security-Policy",
            severity=Severity.HIGH,
            passed=bool(csp),
            description="CSP reduces the impact of script injection by restricting allowed content sources.",
            evidence=(f"Content-Security-Policy: {csp}" if csp else "Header not present"),
            recommendation="Define and test a restrictive Content-Security-Policy appropriate for the application.",
        )
    )

    xcto = header(snapshot, "x-content-type-options")
    findings.append(
        finding(
            rule_id="HDR-002",
            category="Web Security Headers",
            title="X-Content-Type-Options",
            severity=Severity.MEDIUM,
            passed=(xcto or "").lower() == "nosniff",
            description="The nosniff directive prevents browsers from MIME-sniffing responses.",
            evidence=(f"X-Content-Type-Options: {xcto}" if xcto else "Header not present"),
            recommendation="Set X-Content-Type-Options: nosniff.",
        )
    )

    xfo = (header(snapshot, "x-frame-options") or "").lower()
    csp_lower = (csp or "").lower()
    frame_protected = xfo in {"deny", "sameorigin"} or "frame-ancestors" in csp_lower
    evidence_parts = []
    if xfo:
        evidence_parts.append(f"X-Frame-Options: {xfo}")
    if csp and "frame-ancestors" in csp_lower:
        evidence_parts.append("CSP contains frame-ancestors")
    findings.append(
        finding(
            rule_id="HDR-003",
            category="Web Security Headers",
            title="Clickjacking protection",
            severity=Severity.MEDIUM,
            passed=frame_protected,
            description="Frame restrictions reduce clickjacking risk.",
            evidence="; ".join(evidence_parts) if evidence_parts else "No effective frame restriction detected",
            recommendation="Use CSP frame-ancestors and/or X-Frame-Options where appropriate.",
        )
    )

    referrer = header(snapshot, "referrer-policy")
    findings.append(
        finding(
            rule_id="HDR-004",
            category="Web Security Headers",
            title="Referrer-Policy",
            severity=Severity.LOW,
            passed=bool(referrer),
            description="Referrer-Policy limits information disclosed in outbound Referer headers.",
            evidence=(f"Referrer-Policy: {referrer}" if referrer else "Header not present"),
            recommendation="Set a Referrer-Policy such as strict-origin-when-cross-origin or stricter where suitable.",
        )
    )

    permissions = header(snapshot, "permissions-policy")
    findings.append(
        finding(
            rule_id="HDR-005",
            category="Web Security Headers",
            title="Permissions-Policy",
            severity=Severity.LOW,
            passed=bool(permissions),
            description="Permissions-Policy restricts access to selected browser capabilities.",
            evidence=(f"Permissions-Policy: {permissions}" if permissions else "Header not present"),
            recommendation="Define a Permissions-Policy that disables unused browser features.",
        )
    )

    return findings
