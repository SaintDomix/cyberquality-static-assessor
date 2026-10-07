# Security and Ethical Use

CyberQuality Static Assessor is designed for non-destructive, observable checks against HTTP(S) endpoints.
It does not exploit vulnerabilities, brute-force credentials, modify server data, or attempt denial of service.

Use it only on systems you own or are explicitly authorized to assess. The local `demo/` target is included so
all demonstration and CI checks can run without touching external systems.

A failed rule is evidence that a control appears absent or weak from the observed response. It is not proof that
an exploit is possible. Findings should be validated in context before operational decisions are made.
