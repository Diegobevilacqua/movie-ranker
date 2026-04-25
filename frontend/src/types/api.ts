/** Success payloads inside the `data` field of a 2xx response. */

export type CreateUserData = {
  userId: string;
  preferredGenres: string[];
};

export type MovieOut = {
  id: string;
  title: string;
  genres: string[];
};

export type RecommendationsData = {
  movies: MovieOut[];
};

export type LikedMoviesData = {
  movieIds: string[];
};
