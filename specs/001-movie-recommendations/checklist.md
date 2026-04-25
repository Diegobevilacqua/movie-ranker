# Feature checklist: Genre-Based Movie Recommendations

**Spec**: [spec.md](./spec.md)  
**Created**: 2026-04-19

Use pass/fail items only. Align with `.specify/memory/constitution.md` before merge.

## Specification & artifacts

- [ ] `spec.md` matches shipped behavior for this release scope
- [ ] `rules.md` defines deterministic ranking, genre overlap, exclusion of likes, and validation errors (no logic only in code)
- [ ] `examples.json` includes every supported valid request class and defined error cases (scenario coverage)
- [ ] `checklists/requirements.md` completed for this revision

## Behavior

- [ ] Recommendations use shared genres only; no ML or undeclared randomness
- [ ] Liked movies never appear in recommendations for that user
- [ ] Same preferences, likes, and catalog snapshot → identical ranked order
- [ ] API responses use standard JSON envelopes and status codes per constitution

## Quality gates

- [ ] Automated tests cover all `examples.json` cases (exact output matching)
- [ ] Invalid entity references return **400** with error envelope where applicable
- [ ] No undefined behavior paths for inputs in scope
