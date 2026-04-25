"""Shared fixtures."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from movie_ranker.main import create_app
from movie_ranker.models.domain import Movie


@pytest.fixture
def seed_movies() -> list[Movie]:
    return [
        Movie(id="m1", title="Action One", genres=["action", "sci-fi"]),
        Movie(id="m2", title="Drama One", genres=["drama"]),
        Movie(id="m3", title="Action Two", genres=["action"]),
        Movie(id="m4", title="Comedy", genres=["comedy"]),
    ]


@pytest.fixture
def app(seed_movies: list[Movie]):
    return create_app(seed_movies=seed_movies)


@pytest.fixture
def client(app):
    with TestClient(app) as c:
        yield c


@pytest.fixture
def examples_path() -> Path:
    return Path(__file__).resolve().parents[1] / "specs" / "001-movie-recommendations" / "examples.json"


@pytest.fixture
def examples_cases(examples_path: Path) -> list[dict]:
    data = json.loads(examples_path.read_text(encoding="utf-8"))
    return list(data.get("cases", []))
