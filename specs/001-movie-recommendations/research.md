# Research: Genre-Based Movie Recommendations MVP

## Decisions

| Topic | Decision | Rationale | Alternatives |
|-------|-----------|-----------|----------------|
| Persistence | In-memory dict stores keyed by string ID | Fastest path to deterministic MVP; matches “no DB” constraint. | SQLite — deferred (adds migration scope). |
| API framework | FastAPI + Pydantic v2 | Required by project constitution; native validation and OpenAPI. | Flask — rejected (more manual validation). |
| ID generation | Server-generated opaque strings (e.g. `uuid4` hex or `usr_` prefix) | Unique string IDs per constitution; stable in examples. | Client-supplied IDs — rejected (collision + validation burden). |
| Genre normalization | Lowercase + strip whitespace; dedupe | Deterministic matching across user and movie genres. | Locale-aware collation — out of scope for MVP. |
| Ranking tie-break | Document explicitly in `get-recommendations/rules.md` (e.g. `movie.id` ascending after overlap count) | Guarantees reproducible ordering without ML. | Random tie-break — forbidden. |

## Open items (none blocking plan)

All items above are resolved; unknowns become explicit `rules.md` + `examples.json` entries.
