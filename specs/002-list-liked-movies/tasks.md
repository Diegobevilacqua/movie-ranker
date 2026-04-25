# Tasks: List liked movies (002)

**Input**: [plan.md](./plan.md), [spec.md](./spec.md), [rules.md](./rules.md), [examples.json](./examples.json)

## Phase 1: Core

- [X] T001 Add `LikedMoviesData` DTO in [src/movie_ranker/models/dto.py](../../src/movie_ranker/models/dto.py) and export from `models/__init__.py`
- [X] T002 Add `UserService.list_likes` using `get_user` + sorted `get_likes` → `LikedMoviesData`
- [X] T003 Add `GET /users/{user_id}/likes` in [src/movie_ranker/api/routers/users.py](../../src/movie_ranker/api/routers/users.py)

## Phase 2: Tests

- [X] T004 API tests: 404 unknown user, 200 empty, sorted order, determinism
- [X] T005 Contract tests for [examples.json](./examples.json) (with per-case setup)

## Phase 3: Checklist

- [X] T006 Mark [checklist.md](./checklist.md) complete after verification

## Format: `[ID] Description`

- Execute in order T001 → T006.
