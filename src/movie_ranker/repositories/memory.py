"""In-memory repository — users, catalog movies, likes."""

from __future__ import annotations

from movie_ranker.models.domain import Movie, UserProfile


class InMemoryRepository:
    def __init__(self, seed_movies: list[Movie] | None = None) -> None:
        self._users: dict[str, UserProfile] = {}
        self._movies: dict[str, Movie] = {}
        self._likes: dict[str, set[str]] = {}
        for m in seed_movies or []:
            self._movies[m.id] = m

    # --- users ---
    def get_user(self, user_id: str) -> UserProfile | None:
        return self._users.get(user_id)

    def upsert_user(self, profile: UserProfile) -> UserProfile:
        self._users[profile.user_id] = profile
        return profile

    def set_preferred_genres(self, user_id: str, genres: list[str]) -> UserProfile:
        u = self._users.get(user_id)
        if u is None:
            raise KeyError(user_id)
        updated = UserProfile(user_id=user_id, preferred_genres=list(genres))
        self._users[user_id] = updated
        return updated

    # --- movies ---
    def get_movie(self, movie_id: str) -> Movie | None:
        return self._movies.get(movie_id)

    def all_movies(self) -> list[Movie]:
        return list(self._movies.values())

    # --- likes ---
    def add_like(self, user_id: str, movie_id: str) -> None:
        if user_id not in self._likes:
            self._likes[user_id] = set()
        self._likes[user_id].add(movie_id)

    def get_likes(self, user_id: str) -> set[str]:
        return set(self._likes.get(user_id, ()))
