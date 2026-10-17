# Security in DevOps: SAST, SCA, and DAST

A small project that builds an intentionally vulnerable Flask app and scans it with three kinds of security testing, automated through GitHub Actions.

| Type | Tool | What it checks |
|------|------|----------------|
| SAST | SonarQube / SonarQube Cloud | Source code (flaws such as hardcoded secrets, injection) |
| SCA | pip-audit | Third-party dependencies with known CVEs |
| DAST | OWASP ZAP | The running application, by sending real requests |

## Structure

```
.
├── .github/workflows/
│   ├── sast_sca_scan.yml     # SonarQube + pip-audit
│   └── dast_scan.yml         # OWASP ZAP full scan
├── vulnerable_flask_app/     # Intentionally vulnerable app (scan target)
└── fixed_flask_app/          # Remediated version of the same app
```

## Intentional vulnerabilities (vulnerable_flask_app)

- Command injection at `/execute` (`subprocess.run(shell=True)` on user input)
- Reflected XSS at `/hello` (user input placed in HTML unescaped)
- Hardcoded secret key, displayed on `/admin`
- Flask debug mode enabled, bound to `0.0.0.0`
- Outdated dependencies (`Flask==2.0.0`, `Werkzeug==2.0.3`)

## Run locally

```bash
cd vulnerable_flask_app
docker build -t my-vulnerable-flask-app .
docker run -dp 5000:5000 my-vulnerable-flask-app
```

Open http://localhost:5000. Only run this on a machine you control, and stop it when you are done: the app lets anyone run commands on the host container.

## Fixed version

```bash
cd fixed_flask_app
docker build -t my-fixed-flask-app .
docker run -dp 5001:5000 -e SECRET_KEY=change-me my-fixed-flask-app
```

## CI setup

1. Create a SonarQube Cloud project for this repo and disable Automatic Analysis.
2. Add your token as the repository secret `SONAR_TOKEN`.
3. In `.github/workflows/sast_sca_scan.yml`, replace `sonar.organization` and `sonar.projectKey` with your own values.
4. Push to `main` (or run the workflows manually from the Actions tab).

## Credits

Based on the tutorial series by Pantelis Deligiannidis (pandelig.com). Licensed under MIT.
