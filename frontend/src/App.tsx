import { useCallback, useState } from "react";
import {
  addLike,
  createUser,
  getRecommendations,
  listLikes,
  setGenres,
  ApiError,
  NetworkError,
} from "./api/client";
import type { MovieOut } from "./types/api";

function parseGenreInput(raw: string): string[] {
  return raw
    .split(/[,;]+/)
    .map((g) => g.trim())
    .filter(Boolean);
}

function formatError(e: unknown): { title: string; code?: string; message: string } {
  if (e instanceof ApiError) {
    return { title: "API error", code: e.code, message: e.message };
  }
  if (e instanceof NetworkError) {
    return { title: "Connection error", message: e.message };
  }
  if (e instanceof Error) {
    return { title: "Error", message: e.message };
  }
  return { title: "Error", message: String(e) };
}

export function App() {
  const [userIdInput, setUserIdInput] = useState("");
  const [currentUserId, setCurrentUserId] = useState<string | null>(null);
  const [genresInput, setGenresInput] = useState("action, drama");
  const [recommendations, setRecommendations] = useState<MovieOut[] | null>(null);
  const [likedIds, setLikedIds] = useState<string[] | null>(null);
  const [lastError, setLastError] = useState<ReturnType<typeof formatError> | null>(null);
  const [loading, setLoading] = useState(false);

  const clearError = useCallback(() => setLastError(null), []);

  const withLoading = useCallback(
    async <T,>(fn: () => Promise<T>): Promise<T | undefined> => {
      setLoading(true);
      setLastError(null);
      try {
        return await fn();
      } catch (e) {
        setLastError(formatError(e));
        return undefined;
      } finally {
        setLoading(false);
      }
    },
    []
  );

  const onSetUser = useCallback(() => {
    const id = userIdInput.trim();
    if (!id) {
      setLastError({ title: "Validation", message: "User id must be non-empty." });
      return;
    }
    setCurrentUserId(id);
    setRecommendations(null);
    setLikedIds(null);
    setLastError(null);
  }, [userIdInput]);

  const onRegister = useCallback(async () => {
    const id = userIdInput.trim();
    if (!id) {
      setLastError({ title: "Validation", message: "User id must be non-empty." });
      return;
    }
    const res = await withLoading(() => createUser(id));
    if (res) {
      setCurrentUserId(res.userId);
      setRecommendations(null);
      setLikedIds(null);
    }
  }, [userIdInput, withLoading]);

  const onSaveGenres = useCallback(async () => {
    if (!currentUserId) {
      setLastError({ title: "Validation", message: "Set a current user first." });
      return;
    }
    const genres = parseGenreInput(genresInput);
    if (genres.length === 0) {
      setLastError({
        title: "Validation",
        message: "Genres must be a non-empty list (see API rules).",
      });
      return;
    }
    await withLoading(() => setGenres(currentUserId, genres));
  }, [currentUserId, genresInput, withLoading]);

  const onLoadRecommendations = useCallback(async () => {
    if (!currentUserId) {
      setLastError({ title: "Validation", message: "Set a current user first." });
      return;
    }
    const res = await withLoading(() => getRecommendations(currentUserId));
    if (res) {
      setRecommendations(res.movies);
    }
  }, [currentUserId, withLoading]);

  const onRefreshLikes = useCallback(async () => {
    if (!currentUserId) {
      setLastError({ title: "Validation", message: "Set a current user first." });
      return;
    }
    const res = await withLoading(() => listLikes(currentUserId));
    if (res) {
      setLikedIds(res.movieIds);
    }
  }, [currentUserId, withLoading]);

  const onLike = useCallback(
    async (movieId: string) => {
      if (!currentUserId) return;
      const res = await withLoading(async () => {
        await addLike(currentUserId, movieId);
        return listLikes(currentUserId);
      });
      if (res) {
        setLikedIds(res.movieIds);
      }
    },
    [currentUserId, withLoading]
  );

  const apiBase =
    import.meta.env.VITE_API_BASE_URL?.trim() || "http://127.0.0.1:8000";

  return (
    <div className="app">
      <header className="app__header">
        <div className="app__brand">
          <div className="app__title-block">
            <span className="app__eyebrow">Local · rule-based</span>
            <h1 className="app__title">Movie Ranker</h1>
            <p className="app__subtitle">
              Set a user, define genres, explore ranked recommendations, and track likes. Responses follow the
              API&apos;s <code>data</code> / <code>error</code> JSON envelope.
            </p>
          </div>
          <div className="app__api-pill" title="VITE_API_BASE_URL or default">
            <span>API</span>
            <code>{apiBase}</code>
          </div>
        </div>
      </header>

      <div className="app__status" aria-live="polite">
        {loading && (
          <div className="app__loading">
            <span className="spinner" aria-hidden />
            <span>Request in progress…</span>
          </div>
        )}
      </div>

      {lastError && (
        <div className="alert" role="alert">
          <div className="alert__row">
            <span className="alert__title">{lastError.title}</span>
            {lastError.code && <code className="alert__code">{lastError.code}</code>}
          </div>
          <div>{lastError.message}</div>
          <button type="button" className="alert__dismiss" onClick={clearError}>
            Dismiss
          </button>
        </div>
      )}

      <main className="app__main">
        <div className="layout-grid">
          <div>
            <section className="card">
              <div className="card__head">
                <h2 className="card__title">Session</h2>
                {currentUserId ? (
                  <span className="pill-ok">Active</span>
                ) : (
                  <span className="status-idle">No user</span>
                )}
              </div>
              <div className="field">
                <label className="label" htmlFor="uid">
                  User id
                </label>
                <input
                  id="uid"
                  className="input"
                  type="text"
                  autoComplete="off"
                  value={userIdInput}
                  onChange={(e) => setUserIdInput(e.target.value)}
                  placeholder="e.g. demo"
                />
                <p className="hint">Use an existing id or register a new one below.</p>
              </div>
              <div className="btn-row">
                <button type="button" className="btn" onClick={onSetUser} disabled={loading}>
                  Set current user
                </button>
                <button
                  type="button"
                  className="btn btn--ghost"
                  onClick={onRegister}
                  disabled={loading}
                >
                  Register user
                </button>
              </div>
              <div className="meta-foot">
                Current user:
                {currentUserId ? <code>{currentUserId}</code> : <span>—</span>}
              </div>
            </section>

            <section className="card">
              <div className="card__head">
                <h2 className="card__title">Preferences</h2>
              </div>
              <div className="field">
                <label className="label" htmlFor="genres">
                  Preferred genres
                </label>
                <input
                  id="genres"
                  className="input"
                  type="text"
                  value={genresInput}
                  onChange={(e) => setGenresInput(e.target.value)}
                  placeholder="action, drama, …"
                />
                <p className="hint">Comma-separated. Must be a non-empty list to save.</p>
              </div>
              <div className="btn-row">
                <button
                  type="button"
                  className="btn"
                  onClick={onSaveGenres}
                  disabled={loading || !currentUserId}
                >
                  Save genres
                </button>
              </div>
            </section>
          </div>

          <div>
            <section className="card">
              <div className="card__head">
                <h2 className="card__title">Recommendations</h2>
              </div>
              <p className="hint hint--tight-below">
                Deterministic shared-genre ranking from the server. Order is preserved.
              </p>
              <div className="btn-row">
                <button
                  type="button"
                  className="btn"
                  onClick={onLoadRecommendations}
                  disabled={loading || !currentUserId}
                >
                  Load recommendations
                </button>
              </div>
              {recommendations && recommendations.length === 0 && (
                <p className="empty">No matches with current preferences. Try different genres.</p>
              )}
              {recommendations && recommendations.length > 0 && (
                <ul className="film-list">
                  {recommendations.map((m) => (
                    <li key={m.id} className="film-list__row">
                      <div className="film-list__info">
                        <span className="film-list__title">{m.title}</span>
                        <span className="film-list__id">{m.id}</span>
                        <div className="film-list__genres">
                          {m.genres.map((g) => (
                            <span key={g} className="chip">
                              {g}
                            </span>
                          ))}
                        </div>
                      </div>
                      <button
                        type="button"
                        className="btn--like"
                        onClick={() => onLike(m.id)}
                        disabled={loading || !currentUserId}
                      >
                        Like
                      </button>
                    </li>
                  ))}
                </ul>
              )}
            </section>

            <section className="card">
              <div className="card__head">
                <h2 className="card__title">Liked movies</h2>
              </div>
              <p className="hint hint--tight-below">
                Movie ids in server order (lexicographic for this API).
              </p>
              <div className="btn-row">
                <button
                  type="button"
                  className="btn"
                  onClick={onRefreshLikes}
                  disabled={loading || !currentUserId}
                >
                  Refresh list
                </button>
              </div>
              {likedIds && likedIds.length > 0 && (
                <ul className="likes-list">
                  {likedIds.map((id) => (
                    <li key={id}>
                      <span className="chip chip--id">{id}</span>
                    </li>
                  ))}
                </ul>
              )}
              {likedIds && likedIds.length === 0 && (
                <p className="empty">No likes yet. Like a title from the list above.</p>
              )}
            </section>
          </div>
        </div>
      </main>

      <footer className="app__footer">Movie Ranker — development UI. Run the FastAPI server on the API host above.</footer>
    </div>
  );
}
