"""Contract tests aligned with specs/001-movie-recommendations/examples.json."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize(
    "case",
    [
        "set_genres_empty",
        "set_genres_user_missing",
        "like_movie_missing",
        "recommendations_user_missing",
    ],
)
def test_examples_json_cases(case: str, client: TestClient, examples_cases: list[dict]) -> None:
    by_name = {c["name"]: c for c in examples_cases}
    ex = by_name[case]

    if case == "like_movie_missing":
        client.post("/users", json={"userId": "u1"})

    method = ex["method"]
    path = ex["path"]
    kwargs: dict = {}
    if "body" in ex:
        kwargs["json"] = ex["body"]

    r = client.request(method, path, **kwargs)
    assert r.status_code == ex["expect_status"]
    assert r.json() == ex["expect_body"]
