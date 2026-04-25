# Data model — list liked movies

## Reuse (from 001)

- **User** (`UserProfile`): `user_id: str`, `preferred_genres: list[str]`
- **Likes**: per-user set of `movie_id` strings in `InMemoryRepository` (`_likes[user_id] -> set[str]`)

## New derived view (no new persisted entity)

- **Liked list response**: not stored; computed as `sorted(frozen_set_of_ids)` for API output.

## Validation rules

- **GET** has no request body. Path `userId` is non-empty string (FastAPI path param).
- If `get_user(user_id)` is `None` → **404** (do not return `movieIds` for unknown users).
- If user exists, `movieIds` = **sorted** unique liked ids from store.

## State transitions

Read-only; no state change from GET.
