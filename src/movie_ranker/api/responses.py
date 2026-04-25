"""JSON envelope helpers per `.specify/memory/constitution.md`."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel

from movie_ranker.models.dto import Envelope, ErrorBody


def ok(data: Any) -> dict[str, Any]:
    if isinstance(data, BaseModel):
        dumped = data.model_dump()
    elif data is None:
        dumped = None
    else:
        dumped = data
    return Envelope(data=dumped, error=None).model_dump()


def err(status_code: int, code: str, message: str) -> tuple[int, dict[str, Any]]:
    body = Envelope(data=None, error=ErrorBody(code=code, message=message)).model_dump()
    return status_code, body
