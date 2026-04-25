# Feature checklist: 003 — Web frontend

- [X] User can set or register `userId` and see it used for all subsequent API calls.
- [X] User can set non-empty preferred genres and see success or API error envelope.
- [X] User can load recommendations and see `data.movies` in server order (or empty list).
- [X] User can like a movie by id (from recommendations) and see success or API error envelope.
- [X] User can list liked movie ids via GET likes; order matches API (lexicographic on server).
- [X] Any API error response displays `error.code` and `error.message` when present.
- [X] Network failure shows a dedicated message (not a fake success).
- [X] `VITE_API_BASE_URL` (or documented default) is used for all requests.
- [X] No client-side re-ranking of recommendations; no duplicate business rules vs 001/002.
- [X] `examples.json` cases covered by automated tests (or manual sign-off documented in PR).
