# Feature Specification: Genre-Based Movie Recommendations

**Feature Branch**: `001-movie-recommendations`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "Build a movie recommendation system. Users can define their preferred genres and like movies. The system recommends movies based on shared genres, excludes already liked movies, and returns ranked results. No machine learning is used. Recommendations must be deterministic."

**Feature artifacts** (`.specify/memory/constitution.md`): under `/specs/<feature-name>/` use `rules.md` (required when behavior exists), `examples.json`, and `checklist.md`. Keep requirements and scenarios here; put all business logic in `rules.md` — no algorithms in this file. HTTP-facing examples MUST use the standard JSON success and error envelopes and status-code rules from the constitution. Behavior changes MUST follow: update `spec.md`, then `rules.md`, then `examples.json`, then `checklist.md`, then code — in that order. Describe entity IDs as strings, uniqueness expectations, and reference validation; invalid references use **400** per the constitution. List request classes and required state explicitly; every supported valid request class MUST have a matching `examples.json` case; document missing/incomplete state as defined errors.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Get ranked recommendations (Priority: P1)

A user with saved preferences and likes asks for suggestions. The system returns an ordered list of movies that share at least one genre with the user’s preferences, excludes every movie the user has liked, and applies a fixed ranking so that the same inputs and catalog data always produce the same order. No machine learning or undeclared randomness is used.

**Why this priority**: Delivers the core “what to watch next” outcome using shared genres only, deterministically.

**Independent Test**: With a seeded or fixture profile (genres and likes), request recommendations twice and receive identical ordering; verify no liked movie appears in the list.

**Acceptance Scenarios**:

1. **Given** a user with preferred genres and a catalog where some movies share genres with those preferences, **When** they request recommendations, **Then** every returned movie shares at least one genre with the user’s preferences and no returned movie is in the user’s liked set.
2. **Given** the same user preferences, likes, and catalog content, **When** recommendations are requested multiple times, **Then** the ordered list is identical each time (deterministic ranking).
3. **Given** a user with no preferred genres defined, **When** they request recommendations, **Then** the system responds with a defined error or empty result per `rules.md` (no invented defaults).

---

### User Story 2 - Set preferred genres (Priority: P2)

A user opens their profile and selects one or more genres they enjoy. The system saves these preferences and uses them as the basis for future recommendations.

**Why this priority**: Shared-genre matching requires stored preferences; this story supplies that state independently of the recommendation read path.

**Independent Test**: Create or update a profile with a genre list and confirm the stored preferences match what was chosen.

**Acceptance Scenarios**:

1. **Given** a user with no genres yet, **When** they submit a non-empty list of genres, **Then** the system stores exactly those genres for that user.
2. **Given** a user with existing genres, **When** they replace their genre list, **Then** the system updates stored genres to the new list and uses it for subsequent recommendations.

---

### User Story 3 - Like movies (Priority: P3)

A user marks movies they have already seen and liked. The system records each like so those titles can be excluded from future recommendations.

**Why this priority**: Excluding liked movies is an explicit product rule; likes can be tested as their own slice once catalog and identifiers exist.

**Independent Test**: Like a movie and verify it appears in the user’s liked set and is excluded from a later recommendation response when applicable.

**Acceptance Scenarios**:

1. **Given** a valid movie in the catalog, **When** the user likes it, **Then** the system records the like and duplicate likes for the same movie do not create duplicate records.
2. **Given** a movie that is not in the catalog, **When** the user tries to like it, **Then** the system rejects the action with a defined client-visible error (per constitution: invalid reference / validation rules to be detailed in `rules.md` and examples).

---

### Edge Cases

- User has preferred genres but every genre-matching movie is already liked → expect empty recommendation list or defined behavior in `rules.md`.
- User has no liked movies → recommendations include only non-liked, genre-matching titles.
- Catalog contains no movies sharing any preferred genre → empty list or defined behavior in `rules.md`.
- Duplicate like requests for the same movie → idempotent stored state.
- Invalid movie identifier when liking → defined validation error (not success).
- Concurrent updates to genres or likes → last-write behavior or explicit rule in `rules.md` (document assumption if single-client MVP).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Users MUST be able to create and update a non-empty set of preferred genres for their profile when they choose to set preferences (exact minimum and maximum counts, if any, belong in `rules.md`).
- **FR-002**: Users MUST be able to record that they like a movie that exists in the catalog, in an idempotent way per movie.
- **FR-003**: The system MUST recommend only movies that share at least one genre with the user’s current preferred genres.
- **FR-004**: The system MUST exclude every movie the user has liked from the recommendation result set.
- **FR-005**: The system MUST return recommendations as a single ranked list whose order is fully determined by explicit rules (no machine learning, no undeclared randomness).
- **FR-006**: For the same user preferences, same set of likes, and the same catalog snapshot, the system MUST return the same recommendation ordering on every request.
- **FR-007**: The system MUST reject attempts to like a movie that does not exist or is not valid per catalog rules, using a defined error outcome documented in `rules.md` and `examples.json`.
- **FR-008**: Movie and user-facing identifiers MUST be unique strings; cross-entity references MUST be validated per the project constitution.

### Key Entities *(include if feature involves data)*

- **Movie**: A catalog title with a stable string identifier, display fields needed for presentation, and a set of genre labels.
- **User profile**: Preferred genres (set of genre labels) associated with an identified user or session identity as defined in `rules.md`.
- **Like**: Association between a user and a movie they liked, at most one logical like per user–movie pair.
- **Genre**: A normalized label drawn from a shared vocabulary used both on movies and in user preferences.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: For any fixed user preferences, fixed liked-movie set, and fixed catalog snapshot, repeated recommendation requests produce the same ordered list 100% of the time.
- **SC-002**: In tests covering catalog and profile fixtures, 100% of recommended movies share at least one genre with the user’s preferred genres.
- **SC-003**: In tests covering user likes, 0% of recommended movies appear in that user’s liked set.
- **SC-004**: At least one end-to-end user journey (set genres → like at least one movie → receive recommendations) completes without undefined behavior, with outcomes matching documented examples once `examples.json` is populated.

## Assumptions

- Users are associated with a stable identifier so preferences and likes can be stored and retrieved consistently.
- A movie catalog is available to the system; movies include genre metadata suitable for overlap checks.
- Genre labels are comparable as strings (same spelling/casing rules to be fixed in `rules.md` for determinism).
- Scope excludes collaborative filtering, popularity-only ranking, embeddings, and any learned or probabilistic models.
