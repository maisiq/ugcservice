from typing import Any, Awaitable, Protocol

from src.core.protocols import ReviewOperations


class UserMovieService(ReviewOperations, Protocol):
    async def rate_movie(self, user_id: Any, movie_id: Any, value: Any) -> Awaitable[None]: ...
