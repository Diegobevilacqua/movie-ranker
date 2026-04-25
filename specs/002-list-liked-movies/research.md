# Research: List liked movies (002)

## Decisions

| Topic | Decision | Rationale | Alternatives |
|-------|------------|-----------|----------------|
| User missing vs empty likes | **404** for unknown `userId`; **200** + `movieIds: []` for real user with no likes | Matches `rules.md` and `examples.json`; avoids conflating “no account” with “no data”. | 200+empty for unknown — rejected (violates FR-004). |
| Sorting | `sorted(movie_ids)` lexicographic ASCII/Unicode code points | Stated in `rules.md`; matches Python default for string sort; deterministic. | Sort by like time — rejected (no timestamp stored in 001). |
| Response shape | `data: { "movieIds": string[] }` only | No extra fields per constitution + spec. | Include full `Movie` objects — deferred; can be a follow-up spec. |
| Where to sort | Service layer | Repository may return set; service sorts before response for single place of truth. | Sort in repository — acceptable; plan prefers service for testability. |

## Open items

None — all behavior bounded by 002 `spec.md` and `rules.md`.
