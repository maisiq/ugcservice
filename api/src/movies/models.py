from pydantic import BaseModel


class User(BaseModel):
    id: str
    bookmarks: list[str]
    reviews: list[str]
    likes: list[str]
