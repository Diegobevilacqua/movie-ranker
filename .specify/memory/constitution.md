<!--
Sync Impact Report
- Version change: 2.3.0 → 2.4.0
- Modified principles: n/a (additive scenario coverage + state determinism)
- Added sections: Scenario coverage; State determinism
- Removed sections: none
- Templates requiring updates:
  - .specify/templates/plan-template.md — ✅ updated
  - .specify/templates/spec-template.md — ✅ updated
  - .specify/templates/tasks-template.md — ✅ updated
  - .specify/templates/commands/*.md — ⚠ not present (skipped)
- Follow-up TODOs: none
-->

# Movie Ranker — Project Rules

## Specification layout

- Store each feature under `/specs/<feature-name>/` using kebab-case names aligned with the feature branch when applicable.
- Every feature MUST include:
  - `spec.md` — requirements, scenarios, scope, success criteria. MUST NOT contain algorithms, scoring formulas, decision tables, or procedural logic.
  - `rules.md` — all business logic for that feature (including recommendation rules, scoring steps, tie-breaks, validation rules, and error outcomes). REQUIRED whenever the feature affects runtime behavior.
  - `examples.json` — structured inputs and expected outputs (including expected errors). REQUIRED.
  - `checklist.md` — pass/fail completion criteria for that feature. REQUIRED.
- `spec.md` states *what* must hold; `rules.md` states *how* deterministic decisions are made. If they conflict, fix `spec.md` first, then `rules.md`, then `examples.json`.

## Domain behavior

- Produce recommendations using **shared genres only**: rank or filter candidates by overlap between the user’s stated genres (or profile genres) and each candidate’s genres. MUST NOT use collaborative signals, popularity-only ranking, embeddings, trained models, or ML libraries for recommendations.
- **Scoring MUST be deterministic**: same inputs and same catalog snapshot yield the same ordered results. Document ordering and tie-breaks in `rules.md`.
- MUST NOT use randomness, sampling, or probabilistic weighting unless `rules.md` explicitly defines a deterministic pseudo-random seed tied to documented inputs (default: forbid randomness entirely).
- MUST NOT add ML-based or learned ranking.

## Entity constraints

- **IDs**: Every entity identifier MUST be a **string** and MUST be **unique** within that entity type’s store (e.g., catalog, user profiles) as defined in `rules.md` for the feature. Document ID formats and uniqueness scope in `rules.md`; reflect valid and invalid cases in `examples.json`.
- **References**: Any field that points to another entity (foreign key, list of IDs, embedded ref) MUST be **validated** against the authoritative store before applying business rules. Validation MUST run in the service/domain layer implementing `rules.md`, not only at persistence.
- **Invalid references**: Requests that reference a non-existent ID, wrong entity type, or violate referential rules MUST fail with HTTP **400** and the standard **API contracts** error envelope. MUST NOT return **404** for a broken reference embedded in a request body when the route target exists—**404** remains for missing path resources per **API contracts**.

## API and code structure

- Implement the HTTP API with **Python** and **FastAPI**.
- Define request bodies, response bodies, and internal DTOs with **Pydantic** models.
- Organize code with **routers** (HTTP adapters) and **services** (application orchestration). Routers parse/validate input, call services, map results to responses.
- **MUST NOT place business rules or scoring in routers** (no conditional recommendation logic in route handlers beyond delegating to services/modules that implement `rules.md`).
- Implement rule logic in dedicated modules or service functions that map 1:1 to `rules.md` sections where practical; keep controllers thin.

## API contracts

- Every endpoint MUST return **JSON** (`Content-Type: application/json`).
- **Success responses** MUST use this shape: top-level keys `data` and `error`; `error` MUST be JSON `null`; `data` MUST hold the endpoint payload (object, array, or scalar as defined by the contract). Example:

  ```json
  {
    "data": {},
    "error": null
  }
  ```

- **Error responses** MUST use this shape:

  ```json
  {
    "data": null,
    "error": {
      "code": "string",
      "message": "string"
    }
  }
  ```

  `code` MUST be a stable machine-readable identifier; `message` MUST be safe for clients (no stack traces or internal secrets).

- **HTTP status codes** MUST follow this mapping:
  - **200** — request succeeded; response body uses the success envelope with `error: null`.
  - **400** — request validation failed (malformed JSON, missing fields, invalid types, business validation rejected at the edge); response body uses the error envelope.
  - **404** — requested resource does not exist; response body uses the error envelope.
  - **500** — unexpected server failure; response body uses the error envelope.

- MUST NOT return success payloads or errors outside these envelopes except for documented infrastructure endpoints (none by default — add only via amended rules).

## Rules discipline

- All business logic for a feature MUST live in that feature’s `rules.md` and corresponding code implementing those rules.
- `spec.md` MUST remain free of executable logic (no step-by-step algorithms, no numeric thresholds unless restating externally agreed constants that are fully specified in `rules.md`).
- Document every behavior branch: empty inputs, missing genres, ties, invalid IDs, and API error shapes. Unspecified cases MUST be treated as blocked until `rules.md` and `examples.json` are updated.

## Validation

- Treat `examples.json` as the conformance suite: implementations MUST satisfy every example.
- Where examples include HTTP responses, expected bodies MUST use the **API contracts** envelopes and status codes above.
- Automated tests MUST cover `examples.json` (directly or via shared fixtures loaded from it).
- Edge cases listed in `spec.md` MUST appear in `examples.json` or have explicit rule clauses in `rules.md` plus tests; no “we’ll handle it later” paths.

## Strict output matching

- Serialized outputs MUST match `examples.json` expected values **exactly** for every covered case:
  - **Same field names** at every object level (including nested objects inside `data` where applicable).
  - **Same structure** (object vs array vs scalar; nesting depth and shape).
  - **Same ordering for arrays** (element order MUST match the example).
- **MUST NOT** add fields not present in the corresponding example.
- **MUST NOT** omit fields that the example includes for that case.
- Serialization MUST preserve key order as shown in `examples.json` for objects where the example implies an ordering (default: follow the example’s key order exactly).

## Implementation strictness

- If a behavior is **not** explicitly defined in `spec.md`, `rules.md`, or `examples.json`, it MUST NOT be implemented.
- On unspecified inputs or states, the system MUST respond with a **defined error** (per `rules.md` / `examples.json`, using the **API contracts** error envelope and appropriate status code). MUST NOT infer, guess, or apply “reasonable defaults” not written in those artifacts.
- **Partial implementations are NOT allowed**: a feature is not shippable until all scenarios in scope have matching specs, rules, examples, checklist items, and code—no stubbed or half-defined behavior in production paths.

## Scenario coverage

- Define **request classes** (distinct valid input shapes, query combinations, or equivalence classes per endpoint or operation) in `rules.md` for the feature.
- **Every valid request class** that the implementation MUST support MUST be represented by at least one example in `examples.json` (success or expected error outcome as appropriate).
- If a syntactically or schema-valid request falls **outside** the request classes covered by `examples.json`, that case MUST be treated as **unspecified behavior** and MUST NOT receive a success response: handle it per **Implementation strictness** using a **defined error** in `rules.md` / `examples.json` (e.g., reject as out-of-scope input) until new examples and rules are added.
- **Expanding** which inputs are supported MUST follow **Spec evolution**: add or extend `spec.md` and `rules.md`, add the new cases to `examples.json` **before** implementing or enabling them in code.

## State determinism

- **Inputs** (path, query, headers, body) and **required application state** (e.g., catalog snapshot, user profile, session prerequisites) MUST be **explicitly defined** in `spec.md` / `rules.md` and reflected in `examples.json` where they affect outcomes.
- **Missing or incomplete state** (absent required data, uninitialized prerequisites, empty collections where disallowed) MUST be specified as **defined error cases** in `rules.md` with matching entries in `examples.json`; MUST NOT rely on implicit defaults or assumed presence of data.
- **MUST NOT** assume fields, records, or side-loaded data exist without a rule and example covering that branch.

## Spec evolution

- Any behavior change MUST be applied in this order:
  1. Update `spec.md`.
  2. Update `rules.md`.
  3. Update `examples.json`.
  4. Update `checklist.md`.
  5. Then update application code and tests to match.
- **Code changes without corresponding updates** to `spec.md`, `rules.md`, `examples.json`, and `checklist.md` (for the affected scope) are **NOT allowed**.

## Definition of done

- All items in `checklist.md` for the feature are satisfied.
- Runtime behavior matches `examples.json` **exactly** per **Strict output matching** for covered cases.
- No undefined behavior paths remain: every supported request class and relevant error condition has a defined outcome in `rules.md` and is verified by tests and/or checklist items.
- **Scenario coverage**: every supported valid request class appears in `examples.json`; no success paths for request classes absent from examples.
- **State determinism**: required inputs and state are explicit; missing/incomplete state matches defined errors in `rules.md` / `examples.json`.
- No partial implementation: meets **Implementation strictness**.
- Artifact updates preceded code changes per **Spec evolution** for the release scope.

## Governance

- Amend these rules only by editing `.specify/memory/constitution.md`, bumping **version** (semver: MAJOR for incompatible rule or stack changes; MINOR for new obligations; PATCH for clarifications), and updating **Last Amended** (ISO date). Keep **Ratified** as the original adoption date unless resetting governance deliberately.
- Reviews MUST verify **Spec evolution** order for behavior changes, **Strict output matching** against `examples.json`, **Entity constraints** (ID shape/uniqueness, reference validation, **400** on invalid references), **Scenario coverage** (examples cover every supported request class), and **State determinism** (explicit required state and defined errors for gaps) before merge.

**Version**: 2.4.0 | **Ratified**: 2026-04-19 | **Last Amended**: 2026-04-19
