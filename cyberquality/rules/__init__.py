from __future__ import annotations

from cyberquality.models import Finding, ResponseSnapshot

from . import cookies, exposure, headers, transport

RULE_MODULES = (transport, headers, cookies, exposure)


def evaluate_all(snapshot: ResponseSnapshot) -> list[Finding]:
    findings: list[Finding] = []
    for module in RULE_MODULES:
        findings.extend(module.evaluate(snapshot))
    return findings
