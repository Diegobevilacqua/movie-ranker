"""HTTP DTOs — envelope and request/response bodies per API contract."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field, field_validator


class ErrorBody(BaseModel):
    code: str = Field(..., min_length=1)
    message: str = Field(..., min_length=1)


class Envelope(BaseModel):
    data: Any | None = None
    error: ErrorBody | None = None


class CreateUserRequest(BaseModel):
    """Register a user by stable string id (needed before genres/likes)."""

    userId: str = Field(..., min_length=1)

    @field_validator("userId", mode="before")
    @classmethod
    def strip_uid(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("userId must be non-empty")
        return v.strip()


class SetPreferredGenresRequest(BaseModel):
    """Replace preferred genres — must be non-empty per spec / rules."""

    genres: list[str]

    @field_validator("genres")
    @classmethod
    def non_empty_strings(cls, v: list[str]) -> list[str]:
        if not v:
            raise ValueError("genres must be a non-empty array")
        out: list[str] = []
        for g in v:
            if not isinstance(g, str) or not g.strip():
                raise ValueError("each genre must be a non-blank string")
            out.append(g)
        return out


class LikeMovieRequest(BaseModel):
    movieId: str = Field(..., min_length=1)

    @field_validator("movieId", mode="before")
    @classmethod
    def strip_mid(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("movieId must be non-empty")
        return v.strip()


class MovieOut(BaseModel):
    """Response movie payload — id, title, genres only (no extra fields)."""

    id: str
    title: str
    genres: list[str]


class RecommendationsData(BaseModel):
    movies: list[MovieOut]
