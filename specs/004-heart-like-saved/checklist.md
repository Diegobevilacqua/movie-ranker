# Checklist: 004 — Heart-shaped like and save confirmation

| # | Criterion | Pass? |
|---|-----------|-------|
| 1 | Recommendation rows use a **heart-shaped** like control (not text-only). | [ ] |
| 2 | **Liked** vs **not liked** are visually distinct. | [ ] |
| 3 | After a **new** successful like, user gets **short** success feedback (motion and/or aria-live), **within ~1 s** of success. | [ ] |
| 4 | **No** success-only feedback on API/network error. | [ ] |
| 5 | **`prefers-reduced-motion`**: no reliance on motion alone for “saved” understanding. | [ ] |
| 6 | **Screen reader**: control has clear name; “saved” announced if spec calls for live region. | [ ] |
| 7 | **Idempotent** re-like on already-liked movie does **not** produce a fake “newly saved” signal. | [ ] |
| 8 | **`listLikes`** after load recommendations (or equivalent) so rows reflect server liked state. | [ ] |

**Sign-off**: _date / name_
