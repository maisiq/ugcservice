from typing import Any, Awaitable, Protocol

from core.protocols import ReviewOperations


class UserMovieService(ReviewOperations, Protocol):
    async def like(self, user_id: Any, movie_id: Any) -> Awaitable[None]: ...