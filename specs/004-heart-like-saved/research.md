# Research: 004 — Heart-shaped like and save confirmation

## 1. Heart shape (icon delivery)

- **Decision**: Use an **inline SVG** heart in React (single path or two paths), sized via CSS, color via `currentColor` or theme variables so **liked** vs **not liked** are distinct (fill vs stroke).
- **Rationale**: No extra font or npm dependency; crisp at any DPR; full control for animation (`transform` on `<svg>` or wrapper).
- **Alternatives considered**:
  - **Unicode ♥** — inconsistent across OS/fonts; hard to style precisely.
  - **Icon font** — adds build/font pipeline for one glyph.
  - **Image asset** — extra HTTP request and two assets for states unless SVG file (same as inline but less flexible).

## 2. “Saved” feedback (user-visible)

- **Decision**: **Two-layer** confirmation: (1) **visual** transition to **filled** heart (primary state for “liked”); (2) **one-shot** motion on success — e.g. **scale pulse** (≈300–500 ms) on the heart **or** a tiny adjacent check flash — only after successful API path. Optionally **aria-live** announcement “Saved to favorites” once per success (reduced stack with motion for screen readers).
- **Rationale**: Meets spec FR-003 (feedback beyond static state) and SC-003 (perceivable within ~1 s, short duration). Motion stays on the **control** to avoid global toasts and layout shift.
- **Alternatives considered**:
  - **Toast/snackbar** — stronger signal but more layout/CSS; can add later; spec allows “non-intrusive message.”
  - **Confetti / particles** — out of scope and hurts reduced-motion users.

## 3. `prefers-reduced-motion`

- **Decision**: In CSS, wrap keyframe animations in `@media (prefers-reduced-motion: no-preference) { ... }`. For `reduce`, **skip** the pulse; rely on **filled heart + aria-live** (or a static “Saved” text node that appears briefly) so SC edge case is met.
- **Rationale**: Standard platform contract; no extra libraries.
- **Alternatives**: JS `matchMedia` only — redundant if CSS covers all animation.

## 4. Per-row “liked” when opening recommendations

- **Decision**: After **Load recommendations** succeeds, **call `listLikes(currentUserId)`** (same as manual “Refresh list”) so `likedIds` is populated (or `[]`) before showing hearts. If that extra request is undesirable later, a single combined endpoint would be a **future API** change—out of 004 scope.
- **Rationale**: Spec requires distinguishing liked vs not (FR-002); without syncing, all rows look “not liked” until the user has refreshed likes once.
- **Alternatives** — optimistic UI only: rejected; would contradict server truth after reload.

## 5. Error path

- **Decision**: Reuse **existing** `withLoading` + `setLastError` behavior; **no** success feedback hook when `addLike` or follow-up `listLikes` fails (aligns with FR-004 and existing 003 `rules.md`).
- **Rationale**: Single source of truth for errors; no new error UI patterns.

## 6. Unlike / toggle

- **Decision**: **No** new unlike API in v1. **Idempotent** like: if already in `likedIds`, UI shows **liked**; click may still call `addLike` (no-op) — **do not** show a duplicate “saved” feedback if the movie was **already** liked before the click (per rapid-tap and honesty). Implementation: compare previous `likedIds` to new set; only trigger “saved” when `movieId` **newly** appears in the list.
- **Rationale**: Matches current server behavior and avoids false “saved” signals (SC-004).
- **Alternatives** — disable button when liked: possible UX variant; not required by spec (spec allows toggle semantics when product supports unlike).
