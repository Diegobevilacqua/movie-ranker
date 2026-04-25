import { describe, it, expect, vi, afterEach } from "vitest";
import { request, getApiBase, ApiError, NetworkError } from "./client";

function mockFetch(implementation: (input: RequestInfo | URL) => Promise<Response>) {
  vi.stubGlobal("fetch", vi.fn(implementation));
}

afterEach(() => {
  vi.unstubAllGlobals();
  vi.clearAllMocks();
});

describe("getApiBase", () => {
  it("uses default when env unset", () => {
    expect(getApiBase()).toBe("http://127.0.0.1:8000");
  });
});

describe("request (envelopes)", () => {
  it("returns data for 200 success envelope (recommendations example)", async () => {
    mockFetch(async () => ({
      ok: true,
      status: 200,
      json: () =>
        Promise.resolve({
          data: {
            movies: [
              { id: "m1", title: "Action One", genres: ["action", "sci-fi"] },
            ],
          },
          error: null,
        }),
    } as Response));

    const data = await request("/users/u1/recommendations");
    expect(data).toEqual({
      movies: [
        { id: "m1", title: "Action One", genres: ["action", "sci-fi"] },
      ],
    });
    expect((globalThis.fetch as ReturnType<typeof vi.fn>).mock.calls[0][0]).toBe(
      "http://127.0.0.1:8000/users/u1/recommendations"
    );
  });

  it("throws ApiError for 404 error envelope (missing user)", async () => {
    mockFetch(async () => ({
      ok: false,
      status: 404,
      json: () =>
        Promise.resolve({
          data: null,
          error: { code: "USER_NOT_FOUND", message: "user not found" },
        }),
    } as Response));

    await expect(request("/users/missing_user_x/recommendations")).rejects.toMatchObject({
      name: "ApiError",
      status: 404,
      code: "USER_NOT_FOUND",
      message: "user not found",
    } satisfies Partial<ApiError>);
  });

  it("throws NetworkError when fetch rejects", async () => {
    mockFetch(async () => {
      throw new TypeError("Failed to fetch");
    });

    await expect(request("/users/u1/likes")).rejects.toBeInstanceOf(NetworkError);
  });
});
