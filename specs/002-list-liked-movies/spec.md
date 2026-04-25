# Feature Specification: View my liked movies

**Feature Branch**: `002-list-liked-movies`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "Let a user see the list of movies they have already liked, in a stable, reviewable order. Complements the existing like and recommendation features; no new scoring or ML."

**Feature artifacts** (`.specify/memory/constitution.md`): under `/specs/<feature-name>/` use `rules.md` (required when behavior exists), `examples.json`, and `checklist.md`. Keep requirements and scenarios here; put all business logic in `rules.md` — no algorithms in this file. HTTP-facing examples MUST use the standard JSON success and error envelopes and status-code rules from the constitution. Behavior changes MUST follow: update `spec.md`, then `rules.md`, then `examples.json`, then `checklist.md`, then code — in that order. Describe entity IDs as strings, uniqueness expectations, and reference validation; invalid references use **400** per the constitution. List request classes and required state explicitly; every supported valid request class MUST have a matching `examples.json` case; document missing/incomplete state as defined errors.

**Dependency**: This feature assumes users and the like model exist as defined in [specs/001-movie-recommendations/spec.md](../001-movie-recommendations/spec.md) (users can like movies; likes are idempotent per user–movie pair).

## User Scenarios & Testing *(mandatory)*

### User Story 1 - List liked movies (Priority: P1)

A signed-in or identified user opens “My likes” and sees every movie they have liked, in a predictable order, so they can review choices and understand why recommendations may be empty (e.g. all candidates already liked).

**Why this priority**: Read-only visibility into stored state; low risk, high trust; independent of changing recommendation rules.

**Independent Test**: With a user who has zero, one, or many likes, call the list-likes API and assert the response matches the stored set and documented ordering.

**Acceptance Scenarios**:

1. **Given** a user with no likes, **When** they request their liked list, **Then** the system returns a success response with an empty list (no error solely for “no likes”).
2. **Given** a user with one or more likes for movies that exist in the catalog, **When** they request their liked list, **Then** the system returns a success response listing each liked movie exactly once, with a stable, repeatable order across repeated calls.
3. **Given** a user id that does not exist, **When** they request the liked list, **Then** the system returns a not-found error as defined in `rules.md` and `examples.json` (not a success with an empty list).

---

### Edge Cases

- Likes may reference only valid catalog movies at the time of like; list returns identifiers (and optional display fields per contract) for movies still considered valid in catalog — if a movie is later removed from the catalog, behavior is defined in `rules.md` (e.g. return id only, or filter removed titles).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The system MUST expose a read operation for a user to retrieve all movies that user has liked, as a single list.
- **FR-002**: The list MUST be deterministic: repeated calls with the same user and same server state MUST return the same order of entries.
- **FR-003**: The system MUST not introduce machine learning, randomness, or popularity-based ordering for this list; ordering rules belong in `rules.md`.
- **FR-004**: If the user does not exist, the system MUST return an error (not a success with an empty list) per `rules.md` and `examples.json`.
- **FR-005**: The HTTP response MUST use the project JSON success and error envelope and status codes from `.specify/memory/constitution.md`.

### Key Entities

- **User**: Same notion as the parent feature — identified by a stable string `userId` (or equivalent path parameter name in `examples.json`).
- **Like / liked movie set**: The set of `movieId` values recorded for the user; list output is a derived view of that set.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For a fixed user and fixed like set, 100% of repeat list requests return byte-identical ordered payloads (per strict output rules).
- **SC-002**: 100% of list responses for unknown users are errors, not success with an empty list.
- **SC-003**: 100% of `movieId` values in a non-empty list correspond to movies the user had liked in tests (no extras, no missing).

## Assumptions

- The client passes the same `userId` as used for likes and other user-scoped routes in [001-movie-recommendations](../001-movie-recommendations/spec.md).
- For MVP, catalog movies used in likes are still present; if `rules.md` later defines “removed from catalog” behavior, tests will follow.
- No pagination in v1 unless added explicitly in a future spec revision.
