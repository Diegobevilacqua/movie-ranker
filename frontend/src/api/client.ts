import type { CreateUserData, LikedMoviesData, RecommendationsData } from "../types/api";

const DEFAULT_BASE = "http://127.0.0.1:8000";

export function getApiBase(): string {
  const v = import.meta.env.VITE_API_BASE_URL;
  if (typeof v === "string" && v.trim()) {
    return v.trim().replace(/\/$/, "");
  }
  return DEFAULT_BASE;
}

export class ApiError extends Error {
  constructor(
    public readonly status: number,
    public readonly code: string,
    message: string
  ) {
    super(message);
    this.name = "ApiError";
  }
}

export class NetworkError extends Error {
  constructor(
    message: string,
    public readonly causeError?: unknown
  ) {
    super(message);
    this.name = "NetworkError";
  }
}

function joinUrl(base: string, path: string): string {
  const p = path.startsWith("/") ? path : `/${path}`;
  return `${base.replace(/\/$/, "")}${p}`;
}

/**
 * Core JSON + envelope transport. On success, returns the `data` field.
 * On any HTTP or logical API error, throws `ApiError` or `NetworkError`.
 */
export async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const url = joinUrl(getApiBase(), path);
  const headers: HeadersInit = {
    ...(init?.body ? { "Content-Type": "application/json" } : {}),
    ...init?.headers,
  };
  let res: Response;
  try {
    res = await fetch(url, { ...init, headers });
  } catch (e) {
    throw new NetworkError(
      "Cannot reach the API. Is the server running? Check the API base URL and CORS settings.",
      e
    );
  }
  let body: unknown;
  try {
    body = await res.json();
  } catch {
    throw new NetworkError("The server did not return valid JSON.");
  }
  if (!isEnvelope(body)) {
    throw new NetworkError("Unexpected response shape (missing data/error).");
  }
  if (body.error !== null) {
    throw new ApiError(
      res.status,
      body.error.code,
      body.error.message
    );
  }
  if (res.ok) {
    return body.data as T;
  }
  throw new NetworkError(`Unexpected success envelope with status ${res.status}.`);
}

function isEnvelope(
  b: unknown
): b is { data: unknown; error: { code: string; message: string } | null } {
  if (b === null || typeof b !== "object") return false;
  const o = b as Record<string, unknown>;
  return "data" in o && "error" in o;
}

export function postJson<T>(path: string, payload: unknown): Promise<T> {
  return request<T>(path, { method: "POST", body: JSON.stringify(payload) });
}

/* --- API surface (Movie Ranker) --- */

export function createUser(userId: string): Promise<CreateUserData> {
  return postJson<CreateUserData>("/users", { userId: userId.trim() });
}

export function setGenres(
  userId: string,
  genres: string[]
): Promise<CreateUserData> {
  return postJson<CreateUserData>(`/users/${encodeURIComponent(userId)}/genres`, {
    genres,
  });
}

export function getRecommendations(
  userId: string
): Promise<RecommendationsData> {
  return request<RecommendationsData>(
    `/users/${encodeURIComponent(userId)}/recommendations`
  );
}

export function listLikes(userId: string): Promise<LikedMoviesData> {
  return request<LikedMoviesData>(
    `/users/${encodeURIComponent(userId)}/likes`
  );
}

export function addLike(
  userId: string,
  movieId: string
): Promise<{ movieId: string }> {
  return postJson<{ movieId: string }>(
    `/users/${encodeURIComponent(userId)}/likes`,
    { movieId }
  );
}
