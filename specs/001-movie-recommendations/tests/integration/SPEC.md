# Integration tests — specification

**Feature**: `001-movie-recommendations`  
**Location (runtime)**: Repository `tests/integration/` (when implemented), aligned with this spec.

## Scope

- **In scope**: Full app wiring: `TestClient` against FastAPI app, in-memory store populated per test, real routers and services.
- **Exercises**: End-to-end HTTP semantics short of freezing full `examples.json` byte-for-byte (that is contract tests).

## Requirements

- Use the same **JSON envelope** expectations as production (`data` / `error`).
- Status codes MUST match API plan: **200** success, **400** validation/invalid refs, **404** missing user on path, **500** only for simulated internal faults if tested.
- Store state MUST be reset or isolated per test to avoid order-dependent failures.

## Definition of done

- Happy paths for POST `/users`, GET `/movies`, POST `/users/{id}/like`, GET `/users/{id}/recommendations` each have at least one integration test with a seeded catalog.
- Invalid user on recommendation/like paths returns **404** / **400** per plan.
