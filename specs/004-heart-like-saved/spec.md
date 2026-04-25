# Feature Specification: Heart-shaped like and save confirmation

**Feature Branch**: `004-heart-like-saved`  
**Created**: 2026-04-25  
**Status**: Draft  
**Input**: User description: "make the like button heart shaped and add an effect to let the user know that the like was saved."

**Feature artifacts** (`.specify/memory/constitution.md`): under `/specs/004-heart-like-saved/` use `rules.md` (required when behavior exists), `examples.json`, and `checklist.md` if this feature adds or changes API or cross-cutting rules. This feature is **presentation and feedback** on the existing like flow from the web app; server contracts and business rules for likes remain unchanged unless separately specified.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Recognize and use a heart-shaped like control (Priority: P1)

A user viewing a movie (or movie card) sees a **heart-shaped** control for liking. The control’s shape clearly reads as “favorite / like” rather than a generic button. The liked and not-liked states are visually distinct so the user knows whether the current title is already liked.

**Why this priority**: The heart shape and state clarity are the primary visual change; without them, the feature does not deliver its core value.

**Independent Test**: Open a screen with like affordance; confirm the control is heart-shaped and that liked vs not-liked states are distinguishable without relying on other UI copy.

**Acceptance Scenarios**:

1. **Given** a movie the user has not liked, **When** the like area is shown, **Then** the control is heart-shaped and indicates the “not liked” state.
2. **Given** a movie the user has liked, **When** the like area is shown, **Then** the control is heart-shaped and indicates the “liked” state.
3. **Given** any supported screen size used in product testing, **When** the user looks at the control, **Then** the heart shape remains recognizable (not mistaken for a plain square or circle only).

---

### User Story 2 - Notice when a like is saved (Priority: P1)

After the user triggers a like and the application **successfully** persists that like (per existing server behavior), the user receives a **clear, momentary effect** so they understand the like was saved—not only that the button state changed.

**Why this priority**: Reduces doubt and duplicate taps; matches the explicit request for save feedback.

**Independent Test**: Complete a successful like; observe a distinct feedback effect that does not appear on a failed save.

**Acceptance Scenarios**:

1. **Given** a valid like action that succeeds, **When** the save completes successfully, **Then** the user sees or perceives a dedicated confirmation (e.g., brief animation, pulse, or non-intrusive message) in addition to the liked visual state.
2. **Given** a like action that fails (server or network error), **When** the outcome is failure, **Then** the success-only confirmation effect does **not** run; the user is informed per existing app error patterns.
3. **Given** a successful like, **When** confirmation is shown, **Then** it appears within a short window (on the order of seconds) and does not permanently block the rest of the UI.

---

### User Story 3 - Unlike without confusion (Priority: P2)

If the product already allows removing a like, the heart control supports that flow: the user can tell when they have un-liked, and failure to remove a like is surfaced consistent with errors elsewhere.

**Why this priority**: Keeps the new visuals consistent with existing behavior when toggling off.

**Independent Test**: Like then unlike; states and any confirmation rules for “remove like” remain clear and errors are not silent.

**Acceptance Scenarios**:

1. **Given** a liked movie, **When** the user removes the like successfully, **Then** the control returns to the not-liked appearance (and any product-specific brief feedback for removal, if defined in implementation, does not contradict the heart states).

---

### Edge Cases

- **Rapid repeated taps**: Multiple quick taps do not produce misleading stacked “saved” confirmations (e.g., one clear policy: debounce, or show confirmation once per successful save).
- **Offline or timeout**: No success confirmation if the like was not saved; user sees error handling already defined for the app.
- **Accessibility**: The control has an accessible name (e.g., “Like” / “Unlike” or “Add to favorites”) so screen-reader users get the same intent as the visual heart.
- **Reduced motion**: Users who prefer reduced motion still get an unambiguous saved signal (e.g., state change plus text or icon treatment that does not rely solely on motion).

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: The application MUST present the primary like affordance for a title as a **heart-shaped** graphic or icon (not solely a text label or generic rectangle) everywhere the user can like from the main movie UI covered by this feature.
- **FR-002**: The application MUST distinguish **liked** and **not liked** states visually on the heart control so users can tell current like status at a glance.
- **FR-003**: When a like is **successfully** persisted, the application MUST provide a **noticeable, short-lived feedback** (visual and/or brief non-blocking message) that communicates that the like was saved, beyond only switching to the liked state.
- **FR-004**: When a like **fails** to persist, the application MUST NOT show the success-only “saved” feedback; it MUST follow existing user-visible error behavior for API failures.
- **FR-005**: If the product supports removing a like, the heart control MUST reflect the not-liked state after a successful removal, consistent with **FR-002**.

### Key Entities

- **Like action (UI)**: User gesture on the heart control that triggers the existing like or unlike behavior; no new server entity.
- **Save confirmation (UI)**: Transient feedback tied to successful persistence of a like, scoped to this feature.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: In moderated or hallway testing, **at least 90%** of participants identify the control as “like” or “favorite” without coaching, when shown the movie view for the first time.
- **SC-002**: After a **successful** like, users report noticing that their action was saved (observed or self-reported) in **at least 90%** of successful trials in UX testing, without relying on checking a separate list.
- **SC-003**: The save confirmation is **perceivable within 1 second** after the system acknowledges success, and its visible or announced duration stays **under 5 seconds** for static messaging (animated cues may be shorter).
- **SC-004**: No increase in **false “saved” signals**: success-only feedback does not appear when the like API returns an error, verified in a scripted test matrix of failure cases.

## Assumptions

- The existing like API and “current user” flows from the web frontend specification remain the source of truth; this feature only changes how liking is shown and how success is confirmed.
- “Heart shaped” is satisfied by a standard heart symbol or pictogram; exact pixel design is left to design implementation.
- A brief animation is acceptable for the save effect; users with “reduce motion” preferences receive an alternative non-motion cue (e.g., text or persistent state emphasis) as covered in edge cases.
- Haptic feedback on mobile is optional and only applies if the app ships on platforms that support it; the specification does not require haptics to meet **SC-002** if visual or screen-reader confirmation suffices.
