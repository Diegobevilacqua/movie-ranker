# Implementation Plan: Genre-Based Movie Recommendations (MVP)

**Branch**: `001-movie-recommendations` | **Date**: 2026-04-19 | **Spec**: [spec.md](./spec.md)  
**Input**: Feature specification from `/specs/001-movie-recommendations/spec.md` + project context (rule-based, deterministic, strict envelopes)

## Summary

Deliver a **Python/FastAPI** service with **in-memory** storage for MVP. Users are created with preferred **genres**; **movies** live in a catalog; users **like** movies by ID. **GET recommendations** returns a **deterministic, ranked** list of catalog movies that **share ≥1 genre** with the user and **exclude liked** titles—**no ML**, **no randomness**, **no heuristics** outside `rules.md`. All HTTP responses use the **`{ data, error }` envelope** per `.specify/memory/constitution.md`.

## Technical Context

| Field | Value |
|-------|--------|
| **Language/Version** | Python 3.12+ |
| **Primary dependencies** | FastAPI, Uvicorn, Pydantic v2 |
| **Storage** | In-memory repositories (dicts keyed by string IDs); no DB for MVP |
| **Testing** | pytest; contract tests load `examples.json` per feature folder |
| **Target platform** | Linux/macOS/Windows dev; container-ready later |
| **Project type** | HTTP JSON API (backend only) |
| **Performance** | Not a gate for MVP; deterministic correctness first |
| **Constraints** | Strict JSON envelopes; 200/400/404/500 mapping; no unspecified behavior |
| **Scale/scope** | Single-process MVP; catalog + users + likes in RAM |

## Constitution Check

*GATE: Passed — design aligns with `.specify/memory/constitution.md` (FastAPI + Pydantic, thin routers, rules in `rules.md`, `examples.json` as conformance, envelopes, deterministic genre overlap, no ML). Re-check after contracts/examples are frozen.*

## Project Structure

### Documentation (this feature)

```text
specs/001-movie-recommendations/
├── spec.md
├── plan.md                 # this file
├── research.md
├── data-model.md
├── quickstart.md
├── contracts/
│   └── openapi.yaml
├── features/
│   ├── create-user/
│   ├── list-movies/
│   ├── like-movie/
│   └── get-recommendations/
├── tests/                  # test-layer specs (conventions); executable tests live under repo tests/
│   ├── README.md
│   ├── unit/SPEC.md
│   ├── integration/SPEC.md
│   └── contract/SPEC.md
└── checklist.md
```

Each `features/<name>/` holds **`rules.md`**, **`examples.json`**, **`checklist.md`** (and optional thin `spec.md` slice if needed). Cross-cutting `spec.md` remains the parent feature narrative.

### Source code (repository root)

```text
src/movie_ranker/
├── main.py                 # FastAPI app, include routers
├── api/
│   ├── deps.py             # shared deps (store)
│   └── routers/
│       ├── users.py        # POST /users, GET .../recommendations, POST .../like
│       └── movies.py       # GET /movies
├── services/
│   ├── user_service.py
│   ├── movie_service.py
│   └── recommendation_service.py
├── domain/
│   ├── models.py           # Pydantic/domain types
│   └── rules/              # maps to features/*/rules.md
│       ├── create_user.py
│       ├── list_movies.py
│       ├── like_movie.py
│       └── recommend.py    # isolated ranking; only place for scoring steps
├── store/
│   └── memory.py           # InMemoryStore: users, movies
└── errors.py               # map domain failures → error codes + HTTP status

tests/
├── contract/               # examples.json driven
└── unit/
```

**Structure decision**: One package `movie_ranker`; **routers** only parse/validate and call **services**; **domain/rules** encode behavior from each feature’s `rules.md`; **recommendation** logic lives only under `domain/rules/recommend.py` (and `features/get-recommendations/rules.md`).

---

## 1. Architecture

| Layer | Responsibility |
|--------|------------------|
| **Routers** (`api/routers/`) | HTTP I/O, Pydantic request/response models, map success/error to **`{ data, error }`**, call services, **no ranking or genre logic**. |
| **Services** (`services/`) | Orchestration: load from store, call domain rule functions, persist mutations. |
| **Domain / rules** (`domain/rules/`) | Pure functions implementing **`rules.md`** for each feature; **recommendation** isolated in `recommend.py`. |
| **Store** (`store/memory.py`) | Thread-safe enough for MVP (`asyncio.Lock` if needed); string IDs; validate refs before write. |

**Stack**: Python + **FastAPI** + **Pydantic**. **In-memory** store for MVP.

---

## 2. Data model

| Entity | Fields | Rules |
|--------|--------|--------|
| **User** | `id: str` (unique), `genres: set[str]` (normalized), `liked_movies: set[str]` (movie IDs) | Create assigns ID; genres non-empty when required by `create-user/rules.md`; likes validated against catalog. |
| **Movie** | `id: str` (unique), `genres: list[str]` (ordered as stored for deterministic tie-breaks) | Catalog seeded or created at startup; genres non-empty per `list-movies/rules.md`. |

Relationships: User references Movie only via **`liked_movies`** IDs; validation **400** if movie ID missing (constitution).

---

## 3. API surface

All responses JSON; envelope **`{ "data": … \| null, "error": … \| null }`**.

| Method | Path | Purpose |
|--------|------|---------|
| `POST` | `/users` | Create user with body `{ "genres": string[] }` (exact field names in `examples.json`). Returns user `id` + stored genres. |
| `GET` | `/movies` | List catalog movies (deterministic order per `list-movies/rules.md`). |
| `POST` | `/users/{user_id}/like` | Body `{ "movieId": string }`; idempotent like; **400** invalid movie. |
| `GET` | `/users/{user_id}/recommendations` | Ranked recommendations; **404** if user missing; **200** + `data` list per examples. |

---

## 4. Feature breakdown (`/specs` alignment)

| Feature folder | Responsibility |
|----------------|----------------|
| `specs/001-movie-recommendations/features/create-user/` | POST /users — ID generation, genre normalization, duplicates policy. |
| `specs/001-movie-recommendations/features/list-movies/` | GET /movies — ordering of list. |
| `specs/001-movie-recommendations/features/like-movie/` | POST …/like — idempotency, invalid movie **400**. |
| `specs/001-movie-recommendations/features/get-recommendations/` | GET …/recommendations — **only** place for overlap, exclusion, ranking. |

Parent `spec.md` + this `plan.md` tie the four together.

---

## 5. Rules mapping

| Feature | `rules.md` owns | Code module |
|---------|-----------------|-------------|
| create-user | ID format, uniqueness, min/max genres, normalization | `domain/rules/create_user.py` |
| list-movies | Sort key for catalog listing | `domain/rules/list_movies.py` |
| like-movie | Idempotent like, invalid ref → **400** | `domain/rules/like_movie.py` |
| get-recommendations | Shared-genre filter, exclude likes, **tie-break**, empty states | `domain/rules/recommend.py` |

**Recommendation logic** appears **only** in `get-recommendations/rules.md` + `recommend.py`. No other module computes scores or ordering.

---

## 6. Validation strategy

- Each feature maintains **`examples.json`** (inputs + expected HTTP status + exact `data`/`error` bodies).
- **pytest** loads cases (by convention `tests/contract/test_examples_<feature>.py` or parametrized loader).
- Assertions: status code, full JSON **equality** (field order as per constitution strict matching).
- **No** success path for request classes **not** in `examples.json** (scenario coverage).

---

## 7. Error handling

| HTTP | When |
|------|------|
| **200** | Success; `error: null`. |
| **400** | Validation, invalid body, unknown movie on like, bad reference in body. |
| **404** | `user_id` in path does not exist (resource not found). |
| **500** | Unexpected internal errors only. |

**Error codes** (`error.code`, stable):

| Code | Use |
|------|-----|
| `INVALID_INPUT` | Schema / missing required fields / empty genres when disallowed. |
| `USER_NOT_FOUND` | Reserved for consistency; path user missing → prefer **404** with `code` e.g. `NOT_FOUND` or `USER_NOT_FOUND` per examples. |
| `MOVIE_NOT_FOUND` | Like target not in catalog (**400**). |
| `INTERNAL_ERROR` | 500 only. |

Exact `code` strings **frozen in `examples.json`** per feature.

---

## 8. Non-functional constraints

- **Deterministic**: Same store snapshot + same request → same response body and order.
- **No randomness** (no `random`, no shuffled sets without ordered sort key).
- **No ML**; **no popularity** or hidden weights—only rules in `rules.md`.
- **No behavior** not present in `spec.md` / `rules.md` / `examples.json`.

---

## 9. Implementation order

1. **Project skeleton** — FastAPI app, envelope helper, error mapper, `InMemoryStore`, Pydantic models.  
2. **Data models** — User, Movie in `domain/models.py`; seed minimal catalog in store.  
3. **create-user** — `rules.md` + `examples.json` → `create_user` + router POST /users.  
4. **list-movies** — `rules.md` + `examples.json` → GET /movies.  
5. **like-movie** — `rules.md` + `examples.json` → POST …/like.  
6. **get-recommendations** — `rules.md` + `examples.json` → `recommend.py` + GET …/recommendations **last**.

---

## Complexity Tracking

None — constitution gates satisfied without waiver.
