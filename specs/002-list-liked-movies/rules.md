# Feature rules — list liked movies

## Operation

- **GET** `/users/{userId}/likes` (path parameter name in code may be `user_id`; contract uses the same path shape as in `examples.json`).

## Success (HTTP **200**)

- Response body uses the standard **API contracts** success envelope: `data` is an object, `error` is JSON `null`.
- **`data` shape**: `{ "movieIds": string[] }` — each string is a catalog `movieId` the user has liked, **no duplicates** (at most one like per user–movie pair, consistent with 001).
- **Ordering (determinism)**: `movieIds` MUST be sorted in **ascending lexicographic order** (Unicode code point order of the string, same as simple Python `sorted(ids)` for ASCII ids used in tests).
- Empty like set: **200** with `{ "movieIds": [] }` (not an error).

## Not found (HTTP **404**)

- If no user exists for `userId`, return **404** with error envelope, `code` e.g. `USER_NOT_FOUND`, message per `examples.json` (not **200** with empty list).

## Out of scope for this feature

- **POST/DELETE** likes (covered by 001 and future work).
- **Pagination** (full list in one response for MVP).
- Hiding or filtering movies removed from catalog: **MVP** returns all stored liked `movieId` values in sorted order; if an id is not in the catalog, list still includes that id (client may resolve titles separately) unless a future spec tightens this.

## Error codes

| Code            | HTTP | When           |
|-----------------|------|----------------|
| `USER_NOT_FOUND` | 404  | Unknown `userId` |
