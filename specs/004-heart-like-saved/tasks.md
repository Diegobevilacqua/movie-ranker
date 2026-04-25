# Tasks: 004 — Heart-shaped like and save confirmation

**Input**: Design documents from `/specs/004-heart-like-saved/`  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 [P] Add `LikeHeartButton` presentational component at `frontend/src/components/LikeHeartButton.tsx` per `contracts/ui-like-control.md`
- [x] T002 [P] Extend `frontend/src/index.css` with heart, pulse animation, and `prefers-reduced-motion` rules

## Phase 2: Foundational (Blocking)

- [x] T003 Load `listLikes` when loading recommendations in `frontend/src/App.tsx` so `likedIds` is populated for row state
- [x] T004 Track "new like" in `onLike` using pre-request `likedIds` snapshot; set transient `saveFeedbackMovieId` and clear on timer per `data-model.md` and `rules.md`

## Phase 3: User Story 1 — Heart-shaped control and liked state (P1)

**Independent test**: Row shows heart SVG; liked vs not distinct when `listLikes` has loaded.

- [x] T005 [US1] Wire `LikeHeartButton` in recommendation row in `frontend/src/App.tsx` with `liked={likedIds?.includes(m.id) ?? false}` and movie title for labels

## Phase 4: User Story 2 — Save confirmation (P1)

**Independent test**: New like shows pulse/live region; API error shows no success feedback.

- [x] T006 [US2] Pass `showSaveFeedback={saveFeedbackMovieId === m.id}` and add `aria-live` region for "Saved to favorites" when appropriate in `frontend/src/App.tsx`
- [x] T007 [US2] [P] Add `frontend/src/components/LikeHeartButton.test.tsx` for labels and save-feedback class

## Phase 5: Polish

- [x] T008 [P] Run `npm test` in `frontend/` and fix any failures

## Dependencies

- T001, T002 parallel → T003, T004 → T005 → T006 → T007, T008

## Notes

- No backend or API changes.
