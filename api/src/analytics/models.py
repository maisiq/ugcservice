from uuid import UUID

from pydantic import BaseModel


class View(BaseModel):
    movie_id: str
    timestamp_ms: int


class ViewMessage(View):
    user_id: UUID
