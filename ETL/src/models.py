from uuid import UUID

from pydantic import BaseModel


class AnalyticEvent(BaseModel):
    user_id: UUID
    movie_id: str
    timestamp_ms: int
