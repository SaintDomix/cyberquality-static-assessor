# 3–4 Minute Practical Demonstration Script

## Before class

- Make sure the repository is public.
- Make sure the latest GitHub Actions CI run is green.
- Create at least one GitHub Release (for example `v0.1.0`).
- Start the local demo server and Streamlit dashboard.

## Demo

### 1. Repository (30–40 sec)

“This repository contains the first working module of my dissertation architecture: the static rule-based cybersecurity assessment branch. The code is organized as a modular monolith, with separate evidence collection, rule evaluation, scoring and reporting components.”

Show `README.md`, `cyberquality/`, `tests/`, `.github/workflows/`.

### 2. CI/CD (30–40 sec)

“Every push and pull request runs linting and automated tests. The pipeline also starts a deterministic local target, executes two assessments and uploads the generated reports. A version tag triggers a delivery workflow that publishes a release ZIP.”

Open Actions and show the green job and artifact.

### 3. Live insecure assessment (60 sec)

Use `http://127.0.0.1:8765/insecure` in the Streamlit interface.

Point out:
- low overall score;
- missing CSP/security headers;
- weak session-cookie attributes;
- product/version disclosure;
- wildcard CORS;
- evidence and recommendation fields.

### 4. Hardened comparison (40 sec)

Scan `http://127.0.0.1:8765/secure`.

Explain that the same deterministic rules now pass for most web/session controls. HTTP remains visible as a transport limitation, which demonstrates that the scoring does not hide unresolved controls.

### 5. PDF and research context (30 sec)

Download/open the PDF report.

“This structured output is designed to become one input stream to the later cybersecurity-quality integration layer. The second dissertation branch will perform behavioral anomaly analysis, but this assignment intentionally delivers one small, independently testable, reproducible software module.”
