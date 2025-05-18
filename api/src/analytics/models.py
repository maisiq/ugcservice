from uuid import UUID

from pydantic import BaseModel


class ViewMessage(BaseModel):
    user_id: UUID
    movie_id: str
    timestamp_ms: int
