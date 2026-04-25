"""User, genres, likes, recommendations routes."""

from __future__ import annotations

from typing import Annotated, Any

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse

from movie_ranker.api.deps import get_service
from movie_ranker.api.responses import err, ok
from movie_ranker.errors import AppError
from movie_ranker.models.dto import CreateUserRequest, LikeMovieRequest, RecommendationsData
from movie_ranker.services.user_service import UserService

router = APIRouter()


@router.post("/users")
def create_user(
    req: CreateUserRequest,
    svc: Annotated[UserService, Depends(get_service)],
) -> dict[str, Any]:
    u = svc.create_user(req)
    return ok({"userId": u.user_id, "preferredGenres": list(u.preferred_genres)})


@router.post("/users/{user_id}/genres")
async def set_preferred_genres(
    user_id: str,
    request: Request,
    svc: Annotated[UserService, Depends(get_service)],
) -> JSONResponse:
    try:
        body = await request.json()
    except Exception:
        status, payload = err(400, "INVALID_INPUT", "genres must be a non-empty array")
        return JSONResponse(status_code=status, content=payload)

    if not isinstance(body, dict):
        status, payload = err(400, "INVALID_INPUT", "genres must be a non-empty array")
        return JSONResponse(status_code=status, content=payload)

    raw = body.get("genres")
    if not isinstance(raw, list) or len(raw) == 0:
        status, payload = err(400, "INVALID_INPUT", "genres must be a non-empty array")
        return JSONResponse(status_code=status, content=payload)

    genres: list[str] = []
    for g in raw:
        if not isinstance(g, str) or not g.strip():
            status, payload = err(400, "INVALID_INPUT", "genres must be a non-empty array")
            return JSONResponse(status_code=status, content=payload)
        genres.append(g)

    try:
        u = svc.set_preferred_genres(user_id.strip(), genres)
    except AppError as e:
        status, payload = err(e.status_code, e.code, e.message)
        return JSONResponse(status_code=status, content=payload)

    return JSONResponse(status_code=200, content=ok({"userId": u.user_id, "preferredGenres": list(u.preferred_genres)}))


@router.post("/users/{user_id}/likes")
def add_like(
    user_id: str,
    req: LikeMovieRequest,
    svc: Annotated[UserService, Depends(get_service)],
) -> JSONResponse:
    try:
        svc.add_like(user_id.strip(), req.movieId)
    except AppError as e:
        status, payload = err(e.status_code, e.code, e.message)
        return JSONResponse(status_code=status, content=payload)
    return JSONResponse(status_code=200, content=ok({"movieId": req.movieId}))


@router.get("/users/{user_id}/recommendations")
def recommendations(
    user_id: str,
    svc: Annotated[UserService, Depends(get_service)],
) -> JSONResponse:
    try:
        data: RecommendationsData = svc.get_recommendations(user_id.strip())
    except AppError as e:
        status, payload = err(e.status_code, e.code, e.message)
        return JSONResponse(status_code=status, content=payload)
    return JSONResponse(status_code=200, content=ok(data))
