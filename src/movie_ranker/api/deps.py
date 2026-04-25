from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Request

from movie_ranker.repositories.memory import InMemoryRepository
from movie_ranker.services.user_service import UserService


def get_repo(request: Request) -> InMemoryRepository:
    return request.app.state.repo


def get_service(
    repo: Annotated[InMemoryRepository, Depends(get_repo)],
) -> UserService:
    return UserService(repo)
