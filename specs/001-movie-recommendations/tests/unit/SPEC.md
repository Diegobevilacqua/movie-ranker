# Unit tests — specification

**Feature**: `001-movie-recommendations`  
**Location (runtime)**: Repository `tests/unit/` (when implemented), aligned with this spec.

## Scope

- **In scope**: `domain/rules/*.py` — normalization, overlap scoring steps, tie-break ordering, idempotent-like logic **as pure functions** with explicit inputs/outputs.
- **Out of scope**: FastAPI routers, HTTP envelopes, `TestClient` (those belong in integration/contract).

## Requirements

- Tests MUST be deterministic (no wall-clock or randomness unless a rule explicitly fixes a seed; default: none).
- Tests MUST cover edge cases named in `features/*/rules.md` (empty sets, no overlap, all liked, duplicate like).
- Mocks MAY stub `InMemoryStore` only when testing a function that accepts store-like data as plain dicts.

## Definition of done

- Each exported rule function has at least one unit test per distinct branch in `rules.md`.
- Coverage gaps are tracked only when `rules.md` is updated—update tests in the same change set.
