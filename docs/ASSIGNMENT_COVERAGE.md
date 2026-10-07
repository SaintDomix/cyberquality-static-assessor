# Assignment 3 Practical-Part Coverage

This file maps the practical requirements directly to repository evidence.

| Assignment requirement | Repository evidence | Demonstration evidence |
|---|---|---|
| Use Git version control | Local Git repository + structured commit history | `git log --oneline --graph` |
| Host project on GitHub | Public GitHub repository | Repository URL |
| README | `README.md` | Open repository home page |
| License | `LICENSE` | GitHub license indicator |
| Issues | `.github/ISSUE_TEMPLATE/` + real GitHub Issues | Open/closed issues in repository |
| Basic CI/CD pipeline | `.github/workflows/ci.yml` and `release.yml` | GitHub Actions green run + Release |
| Justify technologies | README Technology choices + later theoretical report | Explain Python/httpx/pytest/ReportLab/Streamlit/GitHub Actions |
| Automated testing | `tests/` + pytest coverage | CI test log |
| Code quality/documentation | modular package, Ruff, docstrings/readable names, README/docs | CI lint pass + repository structure |

## Strong presentation sequence

1. Open repository and show README/architecture.
2. Open Issues and show development tasks.
3. Open Actions and show a green CI run.
4. Start local demo server.
5. Open Streamlit UI and scan `/insecure`.
6. Show low score, failed rules, evidence and recommendations.
7. Download/open the generated PDF.
8. Scan `/secure` and show improved dimension scores.
9. Open a GitHub Release created from tag `v0.1.0`.
10. Explain that this is the independently validated static branch; the behavioral AI branch is a later dissertation module.
