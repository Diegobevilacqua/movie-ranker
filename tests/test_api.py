"""API behavior tests — determinism, ranking, likes, validation."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient


def _envelope(data=None, error=None) -> dict:
    return {"data": data, "error": error}


def test_create_and_set_genres_exact_storage(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    body = {"genres": [" Action ", "Drama"]}
    r = client.post("/users/u1/genres", json=body)
    assert r.status_code == 200
    j = r.json()
    assert j == _envelope(
        {"userId": "u1", "preferredGenres": [" Action ", "Drama"]},
    )


def test_set_genres_empty_400(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    r = client.post("/users/u1/genres", json={"genres": []})
    assert r.status_code == 400
    assert r.json() == _envelope(
        error={"code": "INVALID_INPUT", "message": "genres must be a non-empty array"},
    )


def test_set_genres_user_unknown_404(client: TestClient) -> None:
    r = client.post("/users/nobody/genres", json={"genres": ["x"]})
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "USER_NOT_FOUND"


def test_like_unknown_movie_400(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    r = client.post("/users/u1/likes", json={"movieId": "no-such-movie"})
    assert r.status_code == 400
    assert r.json() == _envelope(
        error={"code": "MOVIE_NOT_FOUND", "message": "movie not found"},
    )


def test_like_idempotent(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    r1 = client.post("/users/u1/likes", json={"movieId": "m1"})
    r2 = client.post("/users/u1/likes", json={"movieId": "m1"})
    assert r1.status_code == 200
    assert r2.status_code == 200


def test_recommendations_unknown_user_404(client: TestClient) -> None:
    r = client.get("/users/nobody/recommendations")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "USER_NOT_FOUND"


def test_recommendations_no_genres_empty_list(client: TestClient) -> None:
    """rules.md: no preferred genres → 200 with empty movies (justified in rules)."""
    client.post("/users", json={"userId": "u1"})
    r = client.get("/users/u1/recommendations")
    assert r.status_code == 200
    assert r.json() == _envelope({"movies": []})


def test_recommendations_genre_match_and_ordering(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    client.post("/users/u1/genres", json={"genres": ["action", "sci-fi"]})
    r = client.get("/users/u1/recommendations")
    assert r.status_code == 200
    movies = r.json()["data"]["movies"]
    ids = [m["id"] for m in movies]
    # m1 shares action+sci-fi (2), m3 shares action (1), m2 drama (0), m4 comedy (0)
    assert ids == ["m1", "m3"]


def test_recommendations_exclude_liked(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    client.post("/users/u1/genres", json={"genres": ["action"]})
    client.post("/users/u1/likes", json={"movieId": "m1"})
    r = client.get("/users/u1/recommendations")
    ids = [m["id"] for m in r.json()["data"]["movies"]]
    assert "m1" not in ids
    assert ids == ["m3"]


def test_determinism_repeat_calls(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    client.post("/users/u1/genres", json={"genres": ["action"]})
    a = client.get("/users/u1/recommendations").json()
    b = client.get("/users/u1/recommendations").json()
    assert a == b


def test_get_likes_unknown_user_404(client: TestClient) -> None:
    r = client.get("/users/nobody/likes")
    assert r.status_code == 404
    assert r.json()["error"]["code"] == "USER_NOT_FOUND"


def test_get_likes_empty(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    r = client.get("/users/u1/likes")
    assert r.status_code == 200
    assert r.json() == {
        "data": {"movieIds": []},
        "error": None,
    }


def test_get_likes_sorted_and_deterministic(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    client.post("/users/u1/likes", json={"movieId": "m2"})
    client.post("/users/u1/likes", json={"movieId": "m1"})
    a = client.get("/users/u1/likes").json()
    b = client.get("/users/u1/likes").json()
    assert a == b
    assert a["data"]["movieIds"] == ["m1", "m2"]


def test_response_envelope_shape(client: TestClient) -> None:
    client.post("/users", json={"userId": "u1"})
    r = client.get("/users/u1/recommendations")
    j = r.json()
    assert set(j.keys()) == {"data", "error"}
    assert j["error"] is None
