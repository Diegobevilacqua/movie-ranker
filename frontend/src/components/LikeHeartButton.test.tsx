import { describe, it, expect, vi } from "vitest";
import { render, screen, fireEvent } from "@testing-library/react";
import { LikeHeartButton } from "./LikeHeartButton";

describe("LikeHeartButton", () => {
  it("shows Like label when not liked", () => {
    render(
      <LikeHeartButton
        movieId="m1"
        movieTitle="Action One"
        liked={false}
        disabled={false}
        onPress={() => {}}
      />
    );
    const btn = screen.getByTestId("like-heart-m1");
    expect(btn.getAttribute("aria-label")).toBe("Like Action One");
    expect(btn.getAttribute("aria-pressed")).toBe("false");
  });

  it("shows Liked label when liked", () => {
    render(
      <LikeHeartButton
        movieId="m1"
        movieTitle="Action One"
        liked
        disabled={false}
        onPress={() => {}}
      />
    );
    const btn = screen.getByTestId("like-heart-m1");
    expect(btn.getAttribute("aria-label")).toBe("Liked: Action One");
    expect(btn.getAttribute("aria-pressed")).toBe("true");
  });

  it("calls onPress when clicked", () => {
    const onPress = vi.fn();
    render(
      <LikeHeartButton
        movieId="m1"
        movieTitle="T"
        liked={false}
        disabled={false}
        onPress={onPress}
      />
    );
    fireEvent.click(screen.getByTestId("like-heart-m1"));
    expect(onPress).toHaveBeenCalledTimes(1);
  });

  it("applies save feedback class when showSaveFeedback", () => {
    const { container } = render(
      <LikeHeartButton
        movieId="m1"
        movieTitle="T"
        liked
        disabled={false}
        onPress={() => {}}
        showSaveFeedback
      />
    );
    const btn = container.querySelector("button.like-heart--save-pulse");
    expect(btn).toBeTruthy();
  });
});
