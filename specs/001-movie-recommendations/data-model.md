# Data Model: Genre-Based Movie Recommendations

## User

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | string | Unique in user store; server-generated |
| `genres` | set of string | Normalized labels; semantics (min count) in `features/create-user/rules.md` |
| `liked_movies` | set of string | Movie IDs; subset of catalog IDs; idempotent adds |

## Movie

| Field | Type | Constraints |
|-------|------|-------------|
| `id` | string | Unique in catalog |
| `genres` | list of string | Non-empty unless rules say otherwise; order may affect tie-breaks if documented |

## Invariants

- Every `liked_movies` entry MUST exist in the movie catalog at time of like (else **400**).
- Recommendation input: user must exist (**404** on missing `user_id` path); catalog is global for MVP.

## Store (MVP)

- `users: dict[str, User]`
- `movies: dict[str, Movie]`
- Single process; optional `asyncio.Lock` around mutations if tests hit concurrency.
