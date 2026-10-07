from __future__ import annotations

import re

from cyberquality.models import ResponseSnapshot, Severity

from .common import finding, header


def evaluate(snapshot: ResponseSnapshot):
    findings = []

    server = header(snapshot, "server")
    version_disclosed = bool(server and (re.search(r"\d", server) or "/" in server))
    findings.append(
        finding(
            rule_id="EXP-001",
            category="Information Exposure",
            title="Server version disclosure",
            severity=Severity.LOW,
            passed=not version_disclosed,
            description="Detailed server banners can expose implementation and version information.",
            evidence=(f"Server: {server}" if server else "Server header not present"),
            recommendation="Suppress detailed product/version banners where operationally feasible.",
        )
    )

    powered_by = header(snapshot, "x-powered-by")
    findings.append(
        finding(
            rule_id="EXP-002",
            category="Information Exposure",
            title="X-Powered-By disclosure",
            severity=Severity.MEDIUM,
            passed=not bool(powered_by),
            description="X-Powered-By may disclose framework or runtime information.",
            evidence=(f"X-Powered-By: {powered_by}" if powered_by else "Header not present"),
            recommendation="Remove X-Powered-By headers unless there is a clear operational need.",
        )
    )

    acao = header(snapshot, "access-control-allow-origin")
    credentials = (header(snapshot, "access-control-allow-credentials") or "").lower() == "true"
    wildcard = acao == "*"
    severity = Severity.HIGH if wildcard and credentials else Severity.MEDIUM
    findings.append(
        finding(
            rule_id="EXP-003",
            category="Information Exposure",
            title="CORS wildcard exposure",
            severity=severity,
            passed=not wildcard,
            description="An unrestricted Access-Control-Allow-Origin can expose resources to cross-origin reads.",
            evidence=(
                f"Access-Control-Allow-Origin: {acao}; credentials={credentials}"
                if acao
                else "No Access-Control-Allow-Origin header observed for the assessment Origin"
            ),
            recommendation="Allow only trusted origins for resources that require cross-origin access.",
        )
    )

    return findings
