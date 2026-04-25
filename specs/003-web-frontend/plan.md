# Implementation Plan: Web frontend for Movie Ranker

**Branch**: `003-web-frontend` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/003-web-frontend/spec.md` — *Build a frontend for the app.*

## Summary

Deliver a **browser-based SPA** in `frontend/` that uses **React**, **Vite**, and **TypeScript** to call the existing **Movie Ranker** FastAPI service. The UI lets users **register or select a `userId`**, **set preferred genres**, **view recommendations** (primary source of movie cards in v1; no `GET /movies` in the current API), **like movies**, and **list liked ids**, surfacing the standard JSON **envelopes** and errors per `specs/003-web-frontend/rules.md`. A small **CORS** update on the server is required for local two-origin dev. See [research.md](./research.md) for technology choices; [data-model.md](./data-model.md) and [contracts/openapi.yaml](./contracts/openapi.yaml) describe client-facing contracts.

## Technical Context

| Field | Value |
|-------|--------|
| **Language/Version** | **TypeScript** (5.x) / **ES2022** target; **Node.js 20+** for tooling only (not a runtime service). |
| **Primary dependencies** | **React 18+**, **Vite 5+**; **native `fetch`** (no mandatory HTTP wrapper library). |
| **Storage (client)** | `sessionStorage` or in-memory for current `userId` (optional; no durable client DB in v1). |
| **Testing** | **Vitest**; **@testing-library/react** for component tests; `examples.json`-aligned table tests for envelope parsing. |
| **Target platform** | **Evergreen desktop browsers** (Chrome, Firefox, Edge, Safari current); Vite dev server on `127.0.0.1:5173`. |
| **Project type** | **Web SPA** + existing **JSON REST** backend in `src/movie_ranker/`. |
| **Performance** | Perceived list interactions under **300 ms** after network (excluding network RTT); no jank for typical catalog sizes in seed data. |
| **Constraints** | **No** client-side re-ranking; **no** new recommendation rules; CORS for dev; **VITE_**-prefixed env for API URL. |
| **Scale/scope** | Single-page flows; **4–6** main UI sections (user, genres, recommendations, like, list likes, errors). |

## Constitution Check

*GATE: Passed — re-check after implementation.*

- **Artifacts**: `specs/003-web-frontend/` includes `spec.md`, `rules.md`, `examples.json`, `checklist.md`; planning adds `plan.md`, `research.md`, `data-model.md`, `quickstart.md`, `contracts/`. Evolution order is respected for future behavior changes.
- **Domain (backend)**: The frontend does **not** add ranking, randomness, or ML; it displays API results. Recommendation logic stays in **001** server code / `rules.md`.
- **Stack (server)**: Unchanged: Python, FastAPI, Pydantic. New **TypeScript** SPA is a separate `frontend/` project (see **Complexity tracking**).
- **Rules vs spec**: UI behavior and envelope handling in `003` `rules.md`; no algorithms in `spec.md`.
- **API contracts**: Client consumes the same **200/400/404/500** and `{ data, error }` envelopes; no success bodies outside the envelope.
- **Strict outputs**: Client tests for parsers match **typed** `examples.json` (where fixed bodies apply); integration tests use live or mocked API consistent with 001/002.
- **Entities**: `userId` and `movieId` remain strings; the client does not change validation semantics; **404** for missing user path is surfaced as in API.
- **Scenario coverage**: Valid request classes for the UI are covered by `spec.md` + `checklist.md`; `examples.json` covers envelope shapes for test harnesses.
- **State determinism**: UI displays server order for recommendations and likes lists; no reordering of business-ordered lists except where `rules.md` allows.

## Project Structure

### Documentation (this feature)

```text
specs/003-web-frontend/
├── spec.md
├── plan.md
├── research.md
├── data-model.md
├── quickstart.md
├── rules.md
├── examples.json
├── checklist.md
└── contracts/
    └── openapi.yaml
```

### Source code (repository root)

```text
src/movie_ranker/                    # existing Python API (CORS + optional tweaks only)
src/movie_ranker/main.py

frontend/                            # new Vite + React + TS (created in implementation)
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── .env.example
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── api/
    │   └── client.ts                # base URL, fetch, envelope parse
    ├── components/                  # screens / layout / forms
    └── types/
        └── api.ts

tests/                               # existing Python tests unchanged except API CORS
frontend/
└── src/
    ├── api/
    │   └── client.test.ts
    └── …
```

**Structure decision**: **Option 2 (web app)** — one existing Python service plus one new `frontend/` SPA; no monorepo tooling beyond `npm` in `frontend/` for v1.

## Implementation steps (for `/speckit.tasks` or ad hoc)

1. **CORS** — In `create_app` in [main.py](../../src/movie_ranker/main.py), add `CORSMiddleware` with `allow_origins` for Vite default ports; keep tight for non-prod.
2. **Scaffold** — `npm create vite@latest frontend -- --template react-ts`; add **Vitest** + Testing Library; add `.env.example` with `VITE_API_BASE_URL=`.
3. **API client** — Implement `client.ts` per `data-model.md`: `GET/POST` helpers, envelope parsing, typed errors.
4. **UI flows** — Wire screens: register/select user, genres form, recommendations list, like button, likes list, global error/loading.
5. **Tests** — Unit tests for envelope success/error; optional smoke test for a component with mocked `fetch`.
6. **Docs** — Point `README` or root docs to `specs/003-web-frontend/quickstart.md` for dev workflow.

## Complexity tracking

| Violation | Why needed | Simpler alternative rejected because |
|-----------|------------|-------------------------------------|
| **Second top-level app (`frontend/`) in a Python-first repo** | Product asks for a **browser** experience; Jinja-embedded UIs add coupling and complicate the same CORS/SPA interop problems without modern component ergonomics. | Server-only HTML forms would not meet “frontend app” intent and are slower to iterate. |
| **CORS in FastAPI** | Browsers enforce same-origin; SPA on `:5173` and API on `:8000` require explicit allowlist in dev. | “Single origin” is possible via Vite proxy, but the API must still be explicit for other dev hosts and is needed for any non-proxied setup. |

## Post–Phase 1 (agent context)

The Cursor rules file `.cursor/rules/specify-rules.mdc` is updated to reference **this** `plan.md` for implementation context.

---

_Phase 2 (task breakdown) is **not** produced by `/speckit.plan` — use `/speckit.tasks` to generate `tasks.md`._
