# Feature rules: 004 — Heart-shaped like and save confirmation

## Scope

- **Presentation and client feedback** only. All **HTTP** semantics, envelopes, and error codes follow `specs/003-web-frontend/rules.md` and the server.
- **No** new endpoints, **no** changes to like **business** rules on the server.

## Like control (UI)

- The primary like control on **recommendation rows** MUST be **heart-shaped** (see [spec.md](./spec.md) FR-001); use the [component contract](./contracts/ui-like-control.md) for props and a11y.
- **Liked** vs **not liked** MUST match `GET /users/{userId}/likes` data when that data has been loaded for the session; after **Load recommendations**, the client SHOULD fetch `listLikes` so row state is accurate (see [research.md](./research.md)).

## Success feedback (“saved”)

- **When to show**: Only after **`addLike` succeeds** and the client has **refreshed** `likedIds` (existing `onLike` flow), **and** the `movieId` was **not** already in the previous `likedIds` snapshot (avoids false “saved” on idempotent re-click).
- **When NOT to show**: Any **API error envelope**, **network error**, or **aborted** request; follow existing error banner behavior.
- **Rapid taps**: At most **one** success feedback burst per distinct **new** like per `movieId` until the user navigates away or a defined timeout clears state (implementation detail; must not stack spammy toasts).

## Motion and accessibility

- **Animation** (e.g. pulse) MUST be disabled or replaced per `prefers-reduced-motion: reduce` (CSS and/or behavior); still provide **non-motion** confirmation (filled state + optional `aria-live` per [spec.md](./spec.md) edge cases).
- **Names**: `aria-label` / `aria-pressed` MUST reflect Like vs Liked per [contracts/ui-like-control.md](./contracts/ui-like-control.md).

## Unlike

- Current API has **no** delete-like in MVP; the UI MAY show **liked** state and idempotent **POST** on click. Full **unlike** is out of scope until an API exists.
