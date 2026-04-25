# Tasks: Web frontend (003)

**Input**: `/specs/003-web-frontend/` (plan, spec, rules, examples, data-model)  
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, `contracts/openapi.yaml`

## Phase 1: Setup (Shared Infrastructure)

- [X] **T001** Add FastAPI CORS for Vite dev origins in `src/movie_ranker/main.py`
- [X] **T002** [P] Append Node/frontend ignore patterns to repo `.gitignore` (`node_modules/`, `frontend/dist/`, `coverage/`)
- [X] **T003** Scaffold Vite+React+TS in `frontend/` with `package.json`, `vite.config.ts`, `tsconfig`, `index.html`, `src/main.tsx`, `.env.example`

## Phase 2: Foundational (Blocking)

- [X] **T004** Add Vitest + jsdom in `frontend/` and `npm test` script
- [X] **T005** Implement `frontend/src/api/client.ts` and `frontend/src/types/api.ts` (base URL from `VITE_API_BASE_URL`, default `http://127.0.0.1:8000`, envelope parse, typed `ApiError`)
- [X] **T006** Add `frontend/src/api/client.test.ts` covering envelope success/error patterns aligned with `specs/003-web-frontend/examples.json`

**Checkpoint**: API client and tests pass before full UI

## Phase 3: User Story 1 (P1) — Known user flow

- [X] **T007** [US1] Build `frontend/src/App.tsx` + components: current `userId` input, set user, set genres, load recommendations, list likes, like button per row; preserve recommendation and likes order from API; loading and `lastError` display

## Phase 4: User Story 2 (P2) — Register user

- [X] **T008** [US2] Add “Register new user” action calling `POST /users` with `{ userId }`, set current user on success, show API `error` envelope on failure

## Phase 5: User Story 3 (P3) — Network / errors

- [X] **T009** [US3] Distinguish network/transport errors from JSON API errors in UI copy (`client` throws or returns discriminated type)

## Phase 6: Polish

- [X] **T010** [P] Run `pytest` and `cd frontend && npm test`; fix regressions
- [X] **T011** [P] Link `README.md` to `specs/003-web-frontend/quickstart.md` (one line)

## Dependencies

- T001 before manual browser E2E; T002–T006 sequential per file; T007 depends on T005; T008–T009 extend T007; T010 after T007
