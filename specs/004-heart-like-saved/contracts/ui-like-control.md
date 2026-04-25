# UI contract: Like heart control (004)

> Informal **component interface** for implementation and tests. **Not** an HTTP contract.

## Component name (suggested)

`LikeHeartButton` — presentational; parent owns `onClick` and disabled state.

## Props (TypeScript shape)

| Prop | Type | Required | Description |
|------|------|----------|-------------|
| `movieId` | `string` | yes | For keys and `aria-describedby` if needed. |
| `liked` | `boolean` | yes | Whether this title is in the current `likedIds` set. |
| `disabled` | `boolean` | yes | Mirror global loading or missing user. |
| `onPress` | `() => void` | yes | Invokes parent like handler (e.g. `onLike(movieId)`). |
| `showSaveFeedback` | `boolean` | no | If true, apply **success-only** one-shot visual (e.g. animation class) for this render cycle / short duration. Parent clears after timeout. |
| `className` | `string` | no | Optional layout hook. |

## Accessibility (required)

- **Role**: native `<button type="button">`.
- **Accessible name**:
  - `liked === false` → e.g. `aria-label="Like {title or movieId}"` (title preferred when available).
  - `liked === true` → e.g. `aria-label="Liked"`, `aria-pressed="true"`.
- **Focus**: visible focus ring consistent with `frontend` styles.
- **Live region**: optional **sibling** `aria-live="polite"` in parent (not required inside the button) for “Saved to favorites” when specified in [rules.md](../rules.md).

## Visual (required)

- Control area shows a **heart** silhouette or symbol (SVG), not the word “Like” as the only affordance (spec FR-001). Text may appear as a supplement for a11y but not as the only shape.
- **Liked**: visually distinct (e.g. filled heart / accent); **not liked**: outline or empty heart.

## Events

- `onPress` is invoked only on user activation (click, Enter, Space) — standard button behavior.

## Out of scope

- **Unlike** as a first-class action (no `DELETE` in current API); idempotent re-like may remain possible without duplicate “saved” feedback (see [research.md](../research.md)).
