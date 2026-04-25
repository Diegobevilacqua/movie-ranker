# Data model (client): 004 — Heart-shaped like and save confirmation

> Server DTOs and envelopes are unchanged from [003 data-model](../003-web-frontend/data-model.md). This file adds **ephemeral** UI state for the like control and save feedback.

## Existing (from 003)

- `LikedMoviesData.data.movieIds: string[]` — authoritative for **is this movie liked** when loaded.
- `MovieOut` rows in recommendations include `id`, `title`, `genres`.

## New: transient “save success” signal (client-only)

| Field | Type | Description |
|-------|------|-------------|
| `saveFeedbackKey` | `string \| null` | Typically `movieId` that **newly** received a successful like in the last interaction cycle; drives one-shot visual/a11y feedback. Clear after a short timeout (e.g. 1.5–2.5 s) or when a new like succeeds elsewhere. |
| `saveFeedbackNonce` | `number` (optional) | If needed to re-trigger feedback for the same `movieId` on a later true save (bump on each **eligible** success). |

Implementation may collapse to **React state** in `App` or a small hook: e.g. `justSaved: { movieId: string; expiresAt: number } | null`.

## Derived per recommendation row

| Derivation | Rule |
|------------|------|
| `isLiked` | `likedIds != null && likedIds.includes(movie.id)` |
| `showSavePulse` | `saveFeedbackKey === movie.id` **and** `prefers-reduced-motion` is false (otherwise skip motion only) |
| `announceSaved` | After success, for reduced-motion users or as supplement: one **aria-live** message tied to the same event (see [rules.md](./rules.md)) |

## No new server entities

- **Like** persistence remains the same `POST /users/{userId}/likes` + `GET .../likes` contract.
