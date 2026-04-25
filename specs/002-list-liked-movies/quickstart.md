# Quickstart: verify list-likes (002)

Prerequisites: [001 quickstart](../001-movie-recommendations/quickstart.md) — same app; branch `002-list-liked-movies` after implementation.

## Example session

1. `POST /users` `{ "userId": "u1" }`
2. `POST /users/u1/likes` `{ "movieId": "m2" }` then `{ "movieId": "m1" }` (order of POSTs should not affect list order)
3. `GET /users/u1/likes` → `200` with `data.movieIds` == `["m1", "m2"]` (sorted)
4. `GET /users/nobody/likes` → `404` with `USER_NOT_FOUND`

## Tests

```bash
pytest -q
```

Add or extend contract coverage for `specs/002-list-liked-movies/examples.json` once implemented.
