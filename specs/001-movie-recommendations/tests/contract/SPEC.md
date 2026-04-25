# Contract tests — specification

**Feature**: `001-movie-recommendations`  
**Location (runtime)**: Repository `tests/contract/` (when implemented), aligned with this spec.

## Scope

- **Primary source of truth**: `specs/001-movie-recommendations/features/*/examples.json` (and parent `examples.json` if consolidated later).
- Each case MUST specify: HTTP method, path, optional body, expected **status**, expected **full JSON body** (including envelope and key order where the example defines it).

## Requirements

- Assertions MUST use **exact** equality for response JSON vs expected fixture (strict output matching per constitution).
- Tests MUST fail if a new request class is implemented without a matching example (scenario coverage).
- Load paths MUST stay stable relative to repo root (use fixtures that resolve `examples.json` by feature name).

## Definition of done

- Every example object in each feature’s `examples.json` has a parametrized test (or equivalent) that passes against the running app.
- Error cases include `error.code` values agreed in `plan.md` / `rules.md` (e.g. `INVALID_INPUT`, `MOVIE_NOT_FOUND`).
