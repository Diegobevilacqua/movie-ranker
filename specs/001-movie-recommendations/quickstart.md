# Quickstart: Movie Ranker (dev)

## Prereqs

- Python 3.12+
- Virtualenv (recommended)

## Run API

```bash
cd <repo-root>
python -m venv .venv
.venv\Scripts\activate
pip install -e ".[dev]"
uvicorn movie_ranker.main:app --reload --host 0.0.0.0 --port 8000
```

(OpenAPI UI: `http://localhost:8000/docs` once implemented.)

## Tests

```bash
pytest -q
```

Contract tests should load `specs/001-movie-recommendations/features/*/examples.json`.
