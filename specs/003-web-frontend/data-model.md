# Data model (client): 003 — Web frontend

> Server-side entity definitions remain in 001/002. This file describes **client-recognized shapes** for UI state and API DTOs as consumed from JSON.

## UI session

| Field | Type | Description |
|-------|------|-------------|
| `userId` | `string \| null` | Current actor for `/users/{userId}/...` routes. Trimmed, non-empty when set. |
| `lastError` | `{ code: string; message: string } \| null` | Last API error for optional banner/dismissible alert. |
| `loading` | `boolean` or per-section flags | In-flight request indicators. |

## API envelope (all endpoints)

| Shape | Type | Description |
|-------|------|-------------|
| Success | `{ data: T, error: null }` | `T` depends on route. |
| Error | `{ data: null, error: { code, message } }` | Shown to user. |

## Route payloads (read models)

### `CreateUser` response (POST `/users`)

- `data.userId`: `string`
- `data.preferredGenres`: `string[]` (may be empty at creation)

### `SetGenres` response (POST `/users/{userId}/genres`)

- `data.userId`, `data.preferredGenres[]`

### `MovieOut` (elements of recommendations)

- `id`: `string`
- `title`: `string`
- `genres`: `string[]`

### `RecommendationsData`

- `data.movies`: `MovieOut[]` — order is **authoritative** for ranking.

### `LikedMoviesData`

- `data.movieIds`: `string[]` — order per server (lexicographic for current backend).

## Validation (client)

- The client does **not** re-validate catalog references beyond UX (non-empty strings). The server is authoritative for 400/404 and “movie not found”.
