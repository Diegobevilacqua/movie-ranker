"""Contract tests: specs/002-list-liked-movies/examples.json"""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def examples_002_path() -> Path:
    return Path(__file__).resolve().parents[1] / "specs" / "002-list-liked-movies" / "examples.json"


@pytest.fixture
def cases_002(examples_002_path: Path) -> list[dict]:
    return list(json.loads(examples_002_path.read_text(encoding="utf-8"))["cases"])


@pytest.mark.parametrize("name", ["list_likes_user_missing", "list_likes_empty", "list_likes_two_ids_sorted"])
def test_002_examples(name: str, client: TestClient, cases_002: list[dict]) -> None:
    by_name = {c["name"]: c for c in cases_002}
    ex = by_name[name]

    if name == "list_likes_empty":
        client.post("/users", json={"userId": "u1"})
    if name == "list_likes_two_ids_sorted":
        client.post("/users", json={"userId": "u1"})
        client.post("/users/u1/likes", json={"movieId": "m2"})
        client.post("/users/u1/likes", json={"movieId": "m1"})

    r = client.request(ex["method"], ex["path"])
    assert r.status_code == ex["expect_status"]
    assert r.json() == ex["expect_body"]
