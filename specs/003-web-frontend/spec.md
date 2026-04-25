# Feature Specification: Web frontend for Movie Ranker

**Feature Branch**: `003-web-frontend`  
**Created**: 2026-04-19  
**Status**: Draft  
**Input**: User description: "Build a frontend for the app."

**Feature artifacts** (`.specify/memory/constitution.md`): under `/specs/003-web-frontend/` use `rules.md`, `examples.json`, and `checklist.md`. The frontend **consumes** the existing Movie Ranker HTTP API; it does not change recommendation, genre, or like **business** rules (those stay on the server). The UI must surface API error envelopes to users in a legible way and must not claim behavior that the API does not provide.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Work with a known user (Priority: P1)

A user opens the app, enters or selects a **user id** that already exists on the server, and can view movies, set preferred genres, see recommendations, like movies, and see their list of liked movies. All data comes from the API; the UI clearly shows loading and error states.

**Why this priority**: Delivers the end-to-end value of the product without requiring account systems beyond a string id.

**Independent Test**: With API running and a user seeded, complete browse → set genres → recommendations → like → list likes without a blank screen on errors.

**Acceptance Scenarios**:

1. **Given** the API is reachable and a user `u1` exists, **When** the user enters `u1` and confirms, **Then** subsequent actions use that user id until changed.
2. **Given** a current user, **When** the user requests recommendations, **Then** the UI shows each returned movie (id, title, genres) in the **same order** as the API (see `data.movies`); this is the primary way to **browse** candidate titles in v1 (there is no separate catalog list endpoint today).
3. **Given** a current user, **When** the user sets non-empty preferred genres, **Then** the UI reflects success and later recommendation requests use that state via the API.
4. **Given** a current user with preferences, **When** a recommendation response is empty, **Then** the UI shows an explicit empty state (not an error) unless the API returned an error envelope.
5. **Given** a current user, **When** the user likes a valid movie, **Then** the UI updates or allows refresh to show that like and excludes silent failure when the API returns an error envelope.
6. **Given** a current user, **When** the user views liked movies, **Then** the UI lists `movieIds` from `GET /users/{id}/likes` in the order returned by the API.

---

### User Story 2 - Register a new user from the UI (Priority: P2)

A new visitor creates a user id through the app so they can set genres and get recommendations.

**Why this priority**: Reduces dependency on out-of-band API tools for onboarding.

**Independent Test**: Create user with a fresh id, then run Story 1 flows for that id.

**Acceptance Scenarios**:

1. **Given** a new non-empty `userId` not already present, **When** the user registers, **Then** the app treats that id as the current user and the API returns success per server rules.
2. **Given** a duplicate or invalid id, **When** the user attempts registration, **Then** the UI shows the API error `code` and `message` (no generic “something went wrong” without detail).

---

### User Story 3 - Recover from API and network problems (Priority: P3)

When the API is down, returns 4xx/5xx, or the network fails, the user sees a clear message and can retry when appropriate.

**Why this priority**: Prevents false confidence in stale data and sets expectations for a thin client over HTTP.

**Independent Test**: Stop the API or use invalid base URL; confirm messages and no silent success.

**Acceptance Scenarios**:

1. **Given** a network error, **When** any request is made, **Then** the UI indicates connection failure and does not show a success state for that action.
2. **Given** an API error envelope (`data: null`, `error: { code, message }`), **When** the response is received, **Then** the user can read the error and continue using the app where possible.

---

### Edge Cases

- User id field empty or whitespace — block submit with a clear inline message before calling the API where feasible.
- **404** for missing user on routes that require an existing user — show not-found messaging aligned with `error.message` and `error.code` from the API.
- **400** for invalid body or bad references — show validation-style messaging from the error envelope; do not invent a second source of truth for codes.
- Large lists (many movies) — list remains scrollable; no requirement for virtual scrolling in v1.
- CORS or wrong API base URL — user-visible configuration or documented default in `rules.md` for local dev.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The app MUST call the existing Movie Ranker JSON API (same request and response contracts as the server) for user creation, genre updates, likes, list-likes, and recommendations—no parallel ranking or genre logic in the client.
- **FR-002**: The app MUST let the user designate a **current user id** for actions that require `/users/{userId}/...` paths.
- **FR-003**: The app MUST display lists returned by the API (recommendation movies, liked ids) without reordering for business purposes unless `rules.md` allows presentational sort only; recommendation order is authoritative.
- **FR-004**: The app MUST display API error envelopes to the user: at minimum `error.code` and `error.message` when present.
- **FR-005**: The app MUST show an explicit loading state for in-flight requests that replace prior results.
- **FR-006**: The app MUST be usable on a **desktop-class browser** (keyboard/mouse; responsive layout to common widths is required; native mobile apps are out of scope for v1 per Assumptions).
- **FR-007**: The app MUST read the API base URL from configuration specified in `rules.md` (e.g. environment for dev) so the same build can point at different hosts.

### Key Entities (client- and API-facing)

- **Current session context**: A string `userId` (and optional display metadata) chosen by the user for subsequent calls.
- **Movie (catalog view)**: Data as returned by `GET /movies` (id, title, genres, etc. per API).
- **Error presentation**: Surface `{ code, message }` from the standard error envelope; no internal stack traces.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: A first-time user can go from “open app” to “see at least one recommendation or an explicit empty/error state” in under 3 minutes on a local dev setup, following `quickstart.md`.
- **SC-002**: 100% of user-triggered API failures in covered flows display either a connection/transport message or the API `error.code` / `error.message` (verified by test scenarios in `checklist.md`).
- **SC-003**: No user-visible text claims recommendation order or genre rules that contradict `specs/001-movie-recommendations/rules.md` (client defers to API results).

## Assumptions

- The backend from features **001** and **002** remains the source of truth; the frontend is a **thin** single-page or multi-page web UI.
- **Authentication** is out of scope: user id is a shared secret manually entered (same trust model as direct API use).
- **v1** targets modern evergreen browsers; internationalization and WCAG 2.2 AA are desirable stretch goals, not blockers for initial delivery.
- **API base URL** is injected at build or runtime for development and staging, as documented in `rules.md` and `quickstart.md`.

## Clarifications

### Session 2026-04-19

- (Reserved for future `/speckit.clarify` sessions.)
