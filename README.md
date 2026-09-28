# Notes Sharing System

A small dynamic web app where students share study notes, search them by keyword or subject, and mark notes as helpful.
Built with Python Flask and delivered through Git + GitHub Actions CI/CD to Render.

## Features
- Home page rendered by the server (Jinja2) from data
- Form to share a note (POST /add) with validation
- Search and subject filter (GET /?q=...&subject=...)
- "Helpful" counter (POST /like/<id>)
- JSON API: GET /api/notes
- Health check: GET /health
- Footer shows running commit ID

## Run locally
```
python -m venv venv
venv\Scripts\activate        # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
flake8
pytest -v
python app.py                # http://localhost:5000
```

## Pipeline
```
git push -> Lint (flake8) -> Test (pytest) -> Deploy hook -> Render -> Live site
```
Deploy runs only on push to `main` and only if lint and tests pass (`needs: test`).

## Render settings
Language: Python 3 | Build: `pip install -r requirements.txt` | Start: `gunicorn app:app` | Auto-Deploy: Off | Health check: `/health`
Secret in GitHub: `RENDER_DEPLOY_HOOK`

Live URL: (add here)
