# Feature rules — genre-based movie recommendations

## Genre normalization

- For **matching** (overlap counts): trim whitespace; compare case-insensitively by applying `strip()` then `lower()` to each genre label.
- **User preferred genres** (POST `/users/{userId}/genres`): store the **exact** list order and strings provided in the request body (after JSON parse). Validation only requires non-empty list and non-blank strings per DTO.
- **Movie** genres in catalog: stored as provided at seed time; matching uses normalized equality against normalized user genres.

## POST `/users` (registration — supports tests and flows)

- Body: `{ "userId": string }` (required).
- Creates a user with empty `preferred_genres` and no likes if `userId` is new.
- If user exists: **200** and return current profile (idempotent create).

## POST `/users/{userId}/genres`

- Replaces the user’s preferred genres with the request list **exactly** (order preserved).
- Request body MUST have non-empty `genres` array; each element non-blank after strip → else **400** `INVALID_INPUT`.
- User MUST exist → else **404** `USER_NOT_FOUND`.

## POST `/users/{userId}/likes`

- Body: `{ "movieId": string }`.
- Movie MUST exist in catalog → else **400** `MOVIE_NOT_FOUND`.
- User MUST exist → else **404** `USER_NOT_FOUND`.
- Idempotent: at most one like per `(userId, movieId)`; duplicate POST returns **200** with same logical state.

## GET `/users/{userId}/recommendations`

- User MUST exist → else **404** `USER_NOT_FOUND`.
- If user has **no** preferred genres (empty list): return **200** with `data.movies == []` (empty list, not an error).
- Candidate movies: catalog movies where **normalized** genre overlap with user preferred genres is **≥ 1**.
- Exclude any movie ID in the user’s liked set.
- **Ranking**:
  1. **Primary**: `shared_genre_count` descending (count distinct normalized overlaps).
  2. **Secondary**: `movie.id` ascending (lexicographic string order).
- Deterministic: no randomness; stable sort only.

## Error codes (HTTP + envelope)

| Code | Typical HTTP |
|------|----------------|
| `INVALID_INPUT` | 400 |
| `MOVIE_NOT_FOUND` | 400 |
| `USER_NOT_FOUND` | 404 |
