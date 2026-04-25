"""Domain entities aligned with spec Key Entities — no HTTP shapes."""

from __future__ import annotations

from pydantic import BaseModel, Field, field_validator


def _normalize_genre(value: str) -> str:
    return value.strip().lower()


class Genre(BaseModel):
    """Normalized genre label for comparisons (shared vocabulary)."""

    value: str = Field(..., min_length=1)

    @field_validator("value", mode="before")
    @classmethod
    def normalize(cls, v: str) -> str:
        if not isinstance(v, str):
            raise TypeError("genre must be a string")
        s = v.strip()
        if not s:
            raise ValueError("genre must be non-blank")
        return _normalize_genre(s)

    model_config = {"frozen": True}


class Movie(BaseModel):
    """Catalog movie: stable id, presentation fields, genre labels."""

    id: str = Field(..., min_length=1)
    title: str = Field(..., min_length=1)
    genres: list[str] = Field(default_factory=list)

    @field_validator("id", mode="before")
    @classmethod
    def strip_id(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("movie id must be a non-empty string")
        return v.strip()


class UserProfile(BaseModel):
    """User profile: stable string id and preferred genres (stored order preserved)."""

    user_id: str = Field(..., min_length=1)
    preferred_genres: list[str] = Field(default_factory=list)

    @field_validator("user_id", mode="before")
    @classmethod
    def strip_user(cls, v: str) -> str:
        if not isinstance(v, str) or not v.strip():
            raise ValueError("user_id must be a non-empty string")
        return v.strip()


class Like(BaseModel):
    """At most one logical like per user–movie pair (enforced by repository)."""

    user_id: str = Field(..., min_length=1)
    movie_id: str = Field(..., min_length=1)

    model_config = {"frozen": True}
