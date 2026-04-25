# Quickstart: 003 — Web frontend (with API)

## Prerequisites

- **Python 3.12+** and project virtualenv (see repo root `README` if present; otherwise `uv pip` / `pip install -e ".[dev]"` as in CI).
- **Node.js 20+** and **npm**.

## 1. API (FastAPI)

From the repository root:

```bash
# Install backend deps (example; adjust to project’s documented command)
uv sync
# or: pip install -e ".[dev]"

uvicorn movie_ranker.main:app --reload --host 127.0.0.1 --port 8000
```

### CORS (required for browser)

The FastAPI app must allow the Vite dev origin. If not already configured, add `CORSMiddleware` allowing `http://127.0.0.1:5173` and `http://localhost:5173` (implementation task). Until then, some browsers may block cross-origin `fetch` from the dev server to port 8000.

## 2. Frontend (Vite)

In a second terminal, after `frontend/` is scaffolded by implementation tasks:

```bash
cd frontend
npm install
# Optional override (defaults in rules.md if unset)
set VITE_API_BASE_URL=http://127.0.0.1:8000
npm run dev
```

Open the URL printed by Vite (usually `http://127.0.0.1:5173`).

## 3. Happy path (manual)

1. Register a user id (e.g. `demo`) or type an existing id.
2. Set preferred genres (non-empty list).
3. Open recommendations — confirm order matches server.
4. Like a movie from the list, then open “Liked” — confirm ids list.

## 4. Run tests (once scaffolded)

```bash
cd frontend
npm test
```
