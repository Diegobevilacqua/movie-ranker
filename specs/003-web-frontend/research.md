# Phase 0 research: 003 — Web frontend

## 1. Framework: SPA (React + Vite + TypeScript)

- **Decision**: Use **React 18+**, **Vite**, and **TypeScript** in a new `frontend/` package at the repository root.
- **Rationale**: Strong ecosystem for `fetch` + forms, fast dev server, type-safe DTOs aligned with Pydantic JSON, single-page flow for “current user” without full page reloads. Matches common FastAPI + Vite CORS dev setups.
- **Alternatives considered**:
  - **Vue + Vite** — fine; team ecosystem slightly smaller for this stack.
  - **Next.js** — unnecessary SSR for internal MVP; adds Node hosting assumptions.
  - **No framework (vanilla TS)** — lower bundle size but slower feature velocity for multi-view flows.

## 2. Styling: vanilla CSS or minimal utility layer

- **Decision**: **Plain CSS** (or CSS modules if colocated) with a small set of custom properties for theming. No Tailwind in v1 to avoid extra build deps unless `tasks` add it.
- **Rationale**: Keep footprint small; can migrate to a utility framework later.
- **Alternatives**: Tailwind, styled-components.

## 3. HTTP: native `fetch` + thin API module

- **Decision**: **Native `fetch`**, one module `apiClient.ts` (or similar) that prepends `VITE_API_BASE_URL`, parses envelopes, and throws/returns structured errors.
- **Rationale**: No axios dependency; envelope handling centralized per `rules.md`.
- **Alternatives**: axios, ky.

## 4. CORS and API base URL

- **Decision**: Document **FastAPI `CORSMiddleware`** for `http://127.0.0.1:5173` and `http://localhost:5173` in local dev; **not** a frontend-only fix for production. Frontend reads `import.meta.env.VITE_API_BASE_URL` defaulting to `http://127.0.0.1:8000` per `rules.md`.
- **Rationale**: Browsers require CORS; Vite and API on different ports is standard.
- **Alternatives**: Same-origin only via Vite proxy (also valid; can be noted in `quickstart.md` as optional).

## 5. Current API surface (gap analysis)

- **Finding**: The running API **does not** expose `GET /movies` today; **movie titles for browsing** are obtained via `GET /users/{userId}/recommendations` (`data.movies`). `spec.md` and `rules.md` were written to match this to avoid a blocking backend task for pure UI. A future `GET /movies` (or static catalog) can be added in a follow-up spec without changing the thin-client rule.

## 6. Testing

- **Decision**: **Vitest** for unit tests of envelope parsing and API helpers; optional **@testing-library/react** for component smoke tests. E2E (Playwright) **deferred** unless tasks demand it.
- **Rationale**: Fast feedback; contract cases can mirror `examples.json` in TS.

## 7. Package manager

- **Decision**: **npm** (lockfile `package-lock.json`) unless the repo already standardizes pnpm; current repo is Python-first, so npm is the lowest-friction default.

All **NEEDS CLARIFICATION** items from the initial plan template are resolved by the above.
