from pydantic import BaseModel

from uuid import UUID


class AnalyticEvent(BaseModel):
    user_id: UUID
    movie_id: str
    timestamp_ms: int
