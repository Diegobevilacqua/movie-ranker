# movie-ranker

Rule-based movie recommendation API (FastAPI). See `specs/001-movie-recommendations/` for specifications.

```bash
pip install -e ".[dev]"
uvicorn movie_ranker.main:app --reload
pytest -q
```
