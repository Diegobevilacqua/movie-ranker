# Implementation Plan: Heart-shaped like and save confirmation

**Branch**: `004-heart-like-saved` | **Date**: 2026-04-25 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/004-heart-like-saved/spec.md`

## Summary

Update the **Movie Ranker** React SPA in `frontend/` so the **recommendation row** like affordance is a **heart-shaped** control with clear **liked vs not-liked** visuals, and add **short-lived success feedback** only when `POST /users/{userId}/likes` succeeds and `likedIds` refresh (existing flow). **No new API routes or server behavior**; client presentation and a11y only. See [research.md](./research.md) for icon and motion decisions; [data-model.md](./data-model.md) for UI state; [contracts/ui-like-control.md](./contracts/ui-like-control.md) for component props. [rules.md](./rules.md) and [checklist.md](./checklist.md) cover UI behavior and QA; HTTP shapes remain in `specs/003-web-frontend/`.

## Technical Context

| Field | Value |
|-------|--------|
| **Language/Version** | **TypeScript** (5.x) / **ES2022**; **Node.js 20+** for tooling. |
| **Primary dependencies** | **React 18+**, **Vite 5+** (same as [003 plan](../003-web-frontend/plan.md)). |
| **Storage (client)** | Unchanged; session/in-memory for `userId` and `likedIds`. New **transient** client-only state for “just saved” feedback (see [data-model.md](./data-model.md)). |
| **Testing** | **Vitest** + **@testing-library/react**; test heart renders, `aria-pressed` or `aria-label`, and that success feedback is not called when `addLike` throws. |
| **Target platform** | Evergreen **desktop** browsers; same as 003. |
| **Project type** | **Web SPA** (extend `frontend/`) + unchanged **JSON REST** backend. |
| **Performance** | Feedback animations use **CSS** (GPU-friendly `transform`); single short timeout per success; no extra network beyond existing like + list. |
| **Constraints** | **No** new recommendation or like **business** rules; **no** success toast/animation on API or network error; **respect `prefers-reduced-motion`** (see [research.md](./research.md)). |
| **Scale/scope** | **One** primary surface: recommendation list rows; optional future reuse of the same **presentational** component. |

## Constitution Check

*GATE: Passed — re-check after implementation.*

- **Artifacts**: `specs/004-heart-like-saved/` includes `spec.md`, `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `rules.md`, `examples.json`, `checklist.md`, `contracts/`. **No** new scoring or catalog rules; server `rules.md` (001/002) unchanged.
- **Domain (backend)**: Likes stay **idempotent** `POST` as today; the UI may show “already liked” using `GET /users/{id}/likes` (see [rules.md](./rules.md)) — **no** new ranking, randomness, or ML.
- **Stack (server)**: Unchanged: Python, FastAPI. Client remains TypeScript in `frontend/`.
- **Rules vs spec**: UI affordance and a11y in [rules.md](./rules.md); [spec.md](./spec.md) stays free of implementation detail.
- **API contracts**: Still consume `{ data, error }` envelopes; **no** new endpoints. [examples.json](./examples.json) documents **inherited** like success for regression alignment.
- **Strict outputs (server)**: N/A to this feature; client must not add fields to API requests.
- **Entities**: `userId`, `movieId` remain **strings**; no new ID types.
- **Scenario coverage**: Valid like/list flows already in 002/003; 004 adds **UI** acceptance in [checklist.md](./checklist.md).
- **State determinism**: Liked set for display comes from **server** `listLikes` order/contents; “saved” feedback fires only after successful `addLike` + successful refresh in the existing `onLike` path.

## Project Structure

### Documentation (this feature)

```text
specs/004-heart-like-saved/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── rules.md
├── examples.json
├── checklist.md
└── contracts/
    └── ui-like-control.md
```

### Source code (repository root)

```text
frontend/
├── src/
│   ├── App.tsx                         # wire heart + feedback; optional listLikes on load recommendations
│   ├── index.css                        # heart styles, @keyframes, prefers-reduced-motion
│   └── components/                      # (recommended) LikeHeartButton.tsx — heart SVG, props in contracts
│       └── LikeHeartButton.tsx
└── src/**/*.test.ts(x)                 # a11y + error-path tests
```

**Structure decision**: **Single `frontend/` SPA** (continues [003](../003-web-frontend/plan.md)). Extract a small **presentational** `LikeHeartButton` (or inline in `App.tsx` if kept minimal) with styles colocated in `index.css` or a co-located CSS module per project convention.

## Implementation steps (for `/speckit.tasks` or ad hoc)

1. **Liked state on rows** — When loading recommendations, also **fetch `listLikes`** (or call existing refresh path) so `likedIds` is populated and each row can show **liked** vs not (spec FR-002). If `likedIds` is `null` until first refresh, document one fetch after recommendations load.
2. **Replace text button** — Swap `btn--like` text “Like” for a **heart** (inline **SVG** recommended in [research.md](./research.md)), keep **keyboard** focus and `type="button"`.
3. **Success feedback** — On successful `onLike` completion only: apply a **one-shot** visual (e.g., scale/opacity keyframes on the heart) and/or a short **`aria-live="polite"`** region (“Saved to favorites”); see [rules.md](./rules.md) for when **not** to show it.
4. **Reduced motion** — Use `@media (prefers-reduced-motion: reduce)` to skip or shorten motion; keep non-motion confirmation (aria-live and/or static filled state).
5. **Rapid clicks** — Avoid stacking duplicate “saved” announcements (debounce or single in-flight like per `movieId` as in [rules.md](./rules.md)).
6. **Tests** — Component or `App` tests: mock `addLike` reject → no success class/live region; success → expected behavior.

## Complexity tracking

> No additional projects or server layers. Optional extract of `LikeHeartButton` is a **component boundary** for clarity, not a new deployable.

| Violation | Why needed | Simpler alternative rejected because |
|-----------|------------|-------------------------------------|
| *None* | — | — |

## Phase 0 & 1 outputs

| Phase | Artifact | Status |
|-------|----------|--------|
| 0 | [research.md](./research.md) | Done — icon, feedback, a11y, motion |
| 1 | [data-model.md](./data-model.md) | Done — client UI state |
| 1 | [contracts/ui-like-control.md](./contracts/ui-like-control.md) | Done — component contract |
| 1 | [quickstart.md](./quickstart.md) | Done — run + verify |
| 1 | Agent context (`.cursor/rules/specify-rules.mdc`) | Updated → this `plan.md` |

Phase 2 (`tasks.md`) is produced by `/speckit.tasks`, not this command.

## Constitution Check (post–Phase 1 design)

- Design adds **no** new API surface or Pydantic models.
- [rules.md](./rules.md) ties UI to existing envelope error handling in [003 `rules.md`](../003-web-frontend/rules.md).
- **GATE: still passed.**
