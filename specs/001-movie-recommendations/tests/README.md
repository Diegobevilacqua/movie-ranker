# Tests layout: 001-movie-recommendations

Mirrors how automated tests are organized for this feature. **Executable tests** live under the repository `tests/` tree at project root when code exists; this folder documents **scope and conventions** for each layer.

| Directory | Purpose |
|-----------|---------|
| `unit/` | Fast, isolated tests of pure functions and domain rules modules (`domain/rules/*.py`) with no HTTP or store I/O unless mocked. |
| `integration/` | API + in-memory store together: request/response through FastAPI `TestClient`, real router and service wiring, no external services. |
| `contract/` | Load `specs/001-movie-recommendations/features/*/examples.json`; assert HTTP status and **exact** JSON bodies (envelope + `data`/`error`) per `.specify/memory/constitution.md`. |

See `SPEC.md` in each subdirectory for acceptance criteria for that layer.
