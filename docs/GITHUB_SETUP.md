# GitHub Setup and Commit Plan

Do not upload the ZIP through the GitHub website as one anonymous dump. Use Git locally so the repository visibly satisfies the version-control requirement.

## 1. Create the GitHub repository

On GitHub create a **public** repository named:

`cyberquality-static-assessor`

Create it empty: do not auto-add README, `.gitignore`, or license because they already exist locally.

## 2. Initialize Git locally

From the project folder:

```powershell
git init
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/cyberquality-static-assessor.git
```

## 3. Commit in meaningful stages

The project files are already complete, but stage them in groups so the history demonstrates a real development process.

### Commit 1 — project skeleton/documentation

```powershell
git add README.md LICENSE SECURITY.md .gitignore pyproject.toml requirements.txt requirements-dev.txt
git commit -m "chore: initialize project structure and documentation"
git push -u origin main
```

Then create the GitHub Issues listed below.

### Commit 2 — core assessment engine

```powershell
git add cyberquality/__init__.py cyberquality/models.py cyberquality/collector.py cyberquality/engine.py cyberquality/scoring.py cyberquality/rules
git commit -m "feat: implement static assessment engine and security rules"
git push
```

### Commit 3 — reporting and tests

```powershell
git add cyberquality/reporting.py tests
git commit -m "test: add automated tests and structured reporting"
git push
```

### Commit 4 — CLI, UI and deterministic demo

```powershell
git add main.py app.py demo scripts sample_reports
git commit -m "feat: add CLI dashboard and deterministic demo environment"
git push
```

### Commit 5 — CI/CD

```powershell
git add .github/workflows .github/ISSUE_TEMPLATE
git commit -m "ci: add automated CI and release delivery workflows"
git push
```

### Commit 6 — assignment/demo documentation

```powershell
git add docs CHANGELOG.md
git commit -m "docs: add assignment coverage and demonstration guide"
git push
```

## 4. Recommended GitHub Issues

Create these Issues in GitHub before/around the feature commits and close them after the relevant functionality is pushed:

1. `Implement HTTP security header rules`
2. `Add session cookie security checks`
3. `Generate JSON and PDF assessment reports`
4. `Add automated tests and coverage`
5. `Create demonstration dashboard`
6. `Configure GitHub Actions CI`
7. `Add tag-based release delivery`

The easiest method is GitHub → Issues → New issue. Add labels such as `enhancement`, `testing`, and `documentation` if desired.

## 5. Verify CI

After Commit 5, open:

GitHub repository → **Actions** → **CI**

The job should complete green and contain:

- dependency installation;
- Ruff linting;
- pytest + coverage;
- local demo server;
- insecure/secure report generation;
- uploaded `cyberquality-demo-reports` artifact.

## 6. Create a release to demonstrate CD

When CI is green:

```powershell
git tag v0.1.0
git push origin v0.1.0
```

Then open GitHub → **Actions** → **Release** and wait for it to complete.

Finally open GitHub → **Releases**. Version `v0.1.0` should contain a downloadable project ZIP generated automatically by the workflow.

## 7. Useful Git evidence for presentation

```powershell
git status
git log --oneline --graph --decorate --all
```
