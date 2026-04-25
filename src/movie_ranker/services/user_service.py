"""Application services — orchestration and rule-backed behavior."""

from __future__ import annotations

from movie_ranker.errors import AppError
from movie_ranker.models.domain import Movie, UserProfile
from movie_ranker.models.dto import CreateUserRequest, LikedMoviesData, MovieOut, RecommendationsData
from movie_ranker.repositories.memory import InMemoryRepository


def _normalize(g: str) -> str:
    return g.strip().lower()


def _shared_genre_count(user_genres_norm: set[str], movie: Movie) -> int:
    movie_norm = {_normalize(g) for g in movie.genres}
    return len(user_genres_norm & movie_norm)


class UserService:
    def __init__(self, repo: InMemoryRepository) -> None:
        self._repo = repo

    def create_user(self, req: CreateUserRequest) -> UserProfile:
        uid = req.userId
        existing = self._repo.get_user(uid)
        if existing:
            return existing
        p = UserProfile(user_id=uid, preferred_genres=[])
        return self._repo.upsert_user(p)

    def set_preferred_genres(self, user_id: str, genres: list[str]) -> UserProfile:
        if not self._repo.get_user(user_id):
            raise AppError(404, "USER_NOT_FOUND", "user not found")
        return self._repo.set_preferred_genres(user_id, genres)

    def add_like(self, user_id: str, movie_id: str) -> None:
        if not self._repo.get_user(user_id):
            raise AppError(404, "USER_NOT_FOUND", "user not found")
        if self._repo.get_movie(movie_id) is None:
            raise AppError(400, "MOVIE_NOT_FOUND", "movie not found")
        self._repo.add_like(user_id, movie_id)

    def list_likes(self, user_id: str) -> LikedMoviesData:
        if self._repo.get_user(user_id) is None:
            raise AppError(404, "USER_NOT_FOUND", "user not found")
        ids = sorted(self._repo.get_likes(user_id))
        return LikedMoviesData(movieIds=ids)

    def get_recommendations(self, user_id: str) -> RecommendationsData:
        user = self._repo.get_user(user_id)
        if user is None:
            raise AppError(404, "USER_NOT_FOUND", "user not found")
        if not user.preferred_genres:
            return RecommendationsData(movies=[])

        user_norm = {_normalize(g) for g in user.preferred_genres}
        liked = self._repo.get_likes(user_id)

        candidates: list[tuple[int, str, Movie]] = []
        for m in self._repo.all_movies():
            if m.id in liked:
                continue
            sc = _shared_genre_count(user_norm, m)
            if sc < 1:
                continue
            candidates.append((sc, m.id, m))

        candidates.sort(key=lambda t: (-t[0], t[1]))
        out = [MovieOut(id=m.id, title=m.title, genres=list(m.genres)) for _, _, m in candidates]
        return RecommendationsData(movies=out)
