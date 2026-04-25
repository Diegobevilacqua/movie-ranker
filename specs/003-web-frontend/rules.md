# Feature rules: 003 — Web frontend

## Scope

- The browser app **only** displays data and issues requests supported by the Movie Ranker API implemented under `src/movie_ranker/`. It MUST NOT reimplement recommendation ordering, genre overlap scoring, or like semantics.
- Business rules for ranking and validation remain in **001** / **002** server specs and code.

## API base URL

- The client reads the base URL from **`import.meta.env.VITE_API_BASE_URL`** (Vite) at build/runtime.
- If unset, the app MUST use **`http://127.0.0.1:8000`** as the default for local development (documented in `quickstart.md`).
- All requests MUST be `fetch` to `{baseURL}{path}` with `Content-Type: application/json` on bodies.

## Endpoints the UI must use (MVP)

| Action | Method | Path | Notes |
|--------|--------|------|--------|
| Register user | POST | `/users` | Body `{ "userId": "<string>" }` |
| Set genres | POST | `/users/{userId}/genres` | Body `{ "genres": ["...", ...] }` — must be non-empty per server |
| Like movie | POST | `/users/{userId}/likes` | Body `{ "movieId": "<string>" }` |
| List likes | GET | `/users/{userId}/likes` | Success: `data.movieIds` array, sorted on server |
| Recommendations (primary browse for movie titles in v1) | GET | `/users/{userId}/recommendations` | Success: `data.movies` — `MovieOut[]` in server order; no separate `GET /movies` in current API |

Paths use **exact** server strings (e.g. `likes` not `like`).

## Error handling (client)

- **2xx** with `error: null` — treat as success; render `data` per endpoint shape.
- **4xx/5xx** with JSON error envelope — display `error.code` and `error.message` to the user; do not show raw stack traces.
- **Network failure** (no response) — show a non-technical “cannot reach server” message and suggest checking base URL and that the API is running.
- The client MUST NOT map `404` to a different business meaning than the API (e.g. missing user → show not found, not “invalid id format” unless message says so).

## User id handling

- `userId` is trimmed of leading/trailing whitespace before being placed in path segments or request bodies.
- When no current user is set, genre/like/recommendation actions that require a user MUST be disabled or show an explicit “select or create user” prompt—no request with an empty id.

## Presentation

- Reordering of lists for display (e.g. alphabetical by title) is allowed if **business order** (e.g. recommendations) is shown in a **dedicated** section that preserves API order, or the screen’s sole purpose is recommendations (then order MUST match API).

## Out of scope (v1)

- OAuth, sessions, cookies, JWT.
- Service workers and offline mode.
- Server-side rendering of the React app (SPA only unless plan changes).
