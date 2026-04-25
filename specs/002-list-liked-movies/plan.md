# Implementation Plan: View my liked movies

**Branch**: `002-list-liked-movies` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/002-list-liked-movies/spec.md`

## Summary

Add a **read-only** HTTP endpoint **GET `/users/{userId}/likes`** that returns the current user’s liked `movieId` values in **ascending lexicographic order** inside the standard JSON envelope (`data`, `error`). **404** if the user does not exist; **200** with `data: { "movieIds": [] }` if the user exists but has no likes. Reuses the existing in-memory user/like store from [001-movie-recommendations](../001-movie-recommendations/plan.md); no new persistence technology.

## Technical Context

| Field | Value |
|-------|--------|
| **Language/Version** | Python 3.12+ (same as repo) |
| **Primary dependencies** | FastAPI, Pydantic v2, Uvicorn |
| **Storage** | Existing `InMemoryRepository` — extend with `list_liked_movie_ids(user_id) -> list[str] \| None` (None = unknown user) or equivalent |
| **Testing** | pytest + `TestClient`; contract tests from `examples.json` |
| **Target platform** | Same as 001 (local HTTP API) |
| **Project type** | JSON REST API (incremental feature) |
| **Performance** | O(n log n) sort on like count per user; acceptable for MVP |
| **Constraints** | Strict envelope; **404** vs empty list per `rules.md`; no extra `data` fields |
| **Scale/scope** | Single new route + service method + (optional) DTO + repository read |

## Constitution Check

*GATE: Passed — re-check after implementation.*

- **Artifacts**: `spec.md`, `rules.md`, `examples.json`, `checklist.md` present for 002; evolution order respected before code.
- **This feature** does not change recommendation or genre logic; no ML/randomness; list order fully specified in `rules.md` (lexicographic sort).
- **Stack**: Python, FastAPI, Pydantic; router delegates to `UserService`; sorting in service or domain helper (not in router as business rules).
- **API contracts**: Envelope and **404** for missing user; **200** for success; messages match `examples.json` for contract tests.
- **Strict outputs**: `data` contains only `movieIds` (array of strings) — no additional keys.
- **Entities**: `userId` is string; unknown user is **404**, not **400** (path resource).

## Project Structure

### Documentation (this feature)

```text
specs/002-list-liked-movies/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
└── examples.json
```

### Source code (extends existing package)

```text
src/movie_ranker/
├── api/routers/users.py          # add GET /users/{user_id}/likes
├── models/dto.py                 # e.g. LikedMoviesData { movieIds }
├── services/user_service.py      # get_liked_movie_ids → sorted list; 404 if no user
├── repositories/memory.py      # return sorted list from user's like set; None if no user
tests/
├── test_api.py                   # add cases
└── test_contract_examples.py     # load 002 examples or new test module for 002
```

**Structure decision**: No new top-level package; one vertical slice in existing `movie_ranker` layout.

## Implementation steps (for `/speckit.tasks` or ad hoc)

1. **DTO** — `LikedMoviesData` with `movieIds: list[str]` (field name matches `rules.md` / `examples.json`).
2. **Repository** — `get_user` already exists; add `get_sorted_liked_movie_ids(user_id: str) -> list[str] | None` where `None` means user missing, `[]` means user exists with no likes.
3. **Service** — `list_likes(user_id)` → `LikedMoviesData`; raise `AppError(404, USER_NOT_FOUND, ...)` if user missing; else return sorted set.
4. **Router** — `GET` route above POST likes; return `JSONResponse` + `ok(...)`.
5. **Tests** — Determinism (two GETs), empty vs unknown user, order `m1` before `m2`, match `examples.json` cases; integrate with 001 app factory + seed.

## Complexity Tracking

None.
