"""FastAPI application entry."""

from __future__ import annotations

from fastapi import FastAPI
from fastapi.responses import JSONResponse

from movie_ranker.api.responses import err
from movie_ranker.api.routers import users
from movie_ranker.errors import AppError
from movie_ranker.models.domain import Movie
from movie_ranker.repositories.memory import InMemoryRepository


def default_catalog() -> list[Movie]:
    """Deterministic seed catalog for MVP (rules.md: catalog available)."""
    return [
        Movie(id="m1", title="Action One", genres=["action", "sci-fi"]),
        Movie(id="m2", title="Drama One", genres=["drama"]),
        Movie(id="m3", title="Action Two", genres=["action"]),
        Movie(id="m4", title="No overlap", genres=["comedy"]),
    ]


def create_app(*, seed_movies: list[Movie] | None = None) -> FastAPI:
    repo = InMemoryRepository(seed_movies=seed_movies if seed_movies is not None else default_catalog())
    app = FastAPI(title="Movie Ranker", version="0.1.0")
    app.state.repo = repo
    app.include_router(users.router)

    @app.exception_handler(AppError)
    async def _app_error(_request, exc: AppError) -> JSONResponse:
        status, payload = err(exc.status_code, exc.code, exc.message)
        return JSONResponse(status_code=status, content=payload)

    return app


app = create_app()
