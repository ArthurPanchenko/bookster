from pydantic import BaseModel, Field

from src.auth.schemas import UserReprSchema


class BookSchema(BaseModel):
    title: str
    author: str
    external_id: str


class ReviewReprShema(BaseModel):
    model_config = {"from_attributes": True}
    rating: int
    text: str | None = None
    user: UserReprSchema


class BookRetrieveSchema(BookSchema):
    model_config = {"from_attributes": True}
    reviews: list[ReviewReprShema] = []


class BookUpdateSchema(BaseModel):
    title: str | None = None
    author: str | None = None


class ReviewCreateSchema(BaseModel):
    rating: int = Field(ge=1, le=10)
    text: str | None = None
