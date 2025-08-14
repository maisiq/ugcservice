from pydantic import BaseModel


class User(BaseModel):
    bookmarks: list[str]
    reviews: list[dict]
    ratings: list[dict]
