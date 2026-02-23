
from pydantic import BaseModel


class BookCreateSchema(BaseModel):
    id: int
    title: str
    author: str


class BookRetrieveSchema(BookCreateSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: str | None = None
    author: str | None = None
