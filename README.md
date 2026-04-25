# movie-ranker

Rule-based movie recommendation API (FastAPI). See `specs/001-movie-recommendations/` for specifications. **Web UI (Vite + React):** run the API and the frontend per [specs/003-web-frontend/quickstart.md](specs/003-web-frontend/quickstart.md).

```bash
pip install -e ".[dev]"
uvicorn movie_ranker.main:app --reload
pytest -q
```
