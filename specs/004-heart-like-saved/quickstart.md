# Quickstart: 004 — Heart-shaped like and save confirmation

> See [../003-web-frontend/quickstart.md](../003-web-frontend/quickstart.md) to run the **API** and **Vite** dev server. The steps below are **extra checks** for this feature.

## Verify locally

1. **Start API** (e.g. `uvicorn` on `http://127.0.0.1:8000` per repo README / 003 quickstart).
2. **Start frontend**: `cd frontend && npm run dev` (Vite, typically port **5173**).
3. **Open** the app, set a user, set genres, **Load recommendations**.
4. **Confirm**:
   - Each row shows a **heart** (not only the word “Like”) with distinct **unliked** appearance.
5. **Click the heart** on a movie that is not yet liked:
   - You see a **brief “saved”** effect (e.g. pulse) **or**, with OS “reduced motion” on, a non-animation cue (e.g. live region / clear filled state) per [research.md](./research.md).
   - The heart shows **liked** after success.
6. **Simulate error** (optional): stop the API, click the heart:
   - **No** success-only “saved” feedback; an error appears per existing 003 behavior.

## Run tests

```bash
cd frontend
npm test
```

Add or run component tests for `LikeHeartButton` / `App` that mock `fetch` and assert a11y names and no feedback on failure.

## Env

Unchanged: `VITE_API_BASE_URL` in `frontend` (default `http://127.0.0.1:8000`).
