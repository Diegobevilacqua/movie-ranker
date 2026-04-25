"""Application errors mapped to HTTP status and envelope codes."""

from __future__ import annotations


class AppError(Exception):
    __slots__ = ("status_code", "code", "message")

    def __init__(self, status_code: int, code: str, message: str) -> None:
        self.status_code = status_code
        self.code = code
        self.message = message
        super().__init__(message)
