from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    title: str
    author: str
    external_id: str
     
    

class BookRetrieveSchema(BookCreateSchema):
    pass


class BookUpdateSchema(BaseModel):
    title: str | None = None
    author: str | None = None


class ReviewCreateSchema(BaseModel):
    rating: int = Field(ge=1, le=10)
    text: str | None = None
