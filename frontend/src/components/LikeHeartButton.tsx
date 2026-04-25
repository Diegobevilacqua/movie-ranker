export type LikeHeartButtonProps = {
  movieId: string;
  /** Used for accessible naming */
  movieTitle: string;
  liked: boolean;
  disabled: boolean;
  onPress: () => void;
  showSaveFeedback?: boolean;
  className?: string;
};

/**
 * Heart-shaped like control (see specs/004-heart-like-saved/contracts/ui-like-control.md).
 */
export function LikeHeartButton({
  movieId,
  movieTitle,
  liked,
  disabled,
  onPress,
  showSaveFeedback = false,
  className = "",
}: LikeHeartButtonProps) {
  const label = liked ? `Liked: ${movieTitle}` : `Like ${movieTitle}`;

  return (
    <button
      type="button"
      className={[
        "like-heart",
        liked ? "like-heart--liked" : "",
        showSaveFeedback ? "like-heart--save-pulse" : "",
        className,
      ]
        .filter(Boolean)
        .join(" ")}
      disabled={disabled}
      onClick={onPress}
      data-testid={`like-heart-${movieId}`}
      aria-pressed={liked}
      aria-label={label}
    >
      <svg
        className="like-heart__icon"
        viewBox="0 0 24 24"
        width={22}
        height={22}
        aria-hidden
        focusable="false"
      >
        <path
          className="like-heart__path"
          d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"
        />
      </svg>
    </button>
  );
}
