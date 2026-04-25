# Feature checklist: List liked movies

**Spec**: [spec.md](./spec.md)  
**Created**: 2026-04-19

## Specification & artifacts

- [x] `spec.md` and `rules.md` approved for this scope
- [x] `examples.json` covers: unknown user (404), empty likes (200), non-empty ordered list (200)
- [x] `checklists/requirements.md` (spec quality) complete

## Behavior

- [x] GET returns **404** + `USER_NOT_FOUND` for unknown `userId`
- [x] GET returns **200** + `movieIds` sorted ascending; empty array when no likes
- [x] No duplicates in `movieIds`
- [x] Envelope shape matches `.specify/memory/constitution.md`

## Quality gates

- [x] Contract tests assert exact `examples.json` bodies where applicable
- [x] Determinism: two GETs in a row return identical JSON
