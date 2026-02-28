from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependecies import get_current_user
from src.core.db import get_db
from src.core.exceptions import BookServiceError
from src.library.repository import book_repository, review_respository
from src.library.schemas import (
    BookCreateSchema,
    BookRetrieveSchema,
    BookUpdateSchema,
    ReviewCreateSchema,
)
from src.library.service import get_book_by_id, search

book_router = APIRouter()


@book_router.get("/search")
async def external_search(q: str):
    try:
        response = await search(q)
    except BookServiceError as e:
        raise HTTPException(status_code=e.status, detail=e.message)
    return response


@book_router.get("/search/{book_id}")
async def external_get_by_id(book_id: str):
    try:
        response = await get_book_by_id(book_id)
    except BookServiceError as e:
        raise HTTPException(status_code=e.status, detail=e.message)
    return response


@book_router.post("/search/{book_external_id}/reviews")
async def create_review(
    book_external_id: str,
    review_data: ReviewCreateSchema,
    session: AsyncSession = Depends(get_db),
    user=Depends(get_current_user),
):
    book = await book_repository.get_or_none_by_external_id(book_external_id, session)
    if book is None:
        try:
            response = await get_book_by_id(book_external_id)
        except BookServiceError as e:
            raise HTTPException(status_code=e.status, detail=e.message)
        book_data = BookCreateSchema(
            title=response["title"],
            author=response["authors"][0],
            external_id=response["id"],
        )
        book = await book_repository.create_book(book_data.model_dump(), session)

    review_dict_data = review_data.model_dump(exclude_unset=True)
    review_dict_data["book_id"] = book.id
    review_dict_data["user_id"] = user.id

    review = await review_respository.create_review(review_dict_data, session)

    return review


@book_router.post("/books/", response_model=BookRetrieveSchema)
async def create_book(book: BookCreateSchema, session: AsyncSession = Depends(get_db)):
    created_book = await book_repository.create_book(book.model_dump(), session)
    return created_book


@book_router.get("/books/{id}")
async def get_book(id: int, session: AsyncSession = Depends(get_db)):
    book = await book_repository.get_book_or_raise(id, session)
    return book


@book_router.patch("/books/{id}")
async def update_book(
    id: int, updated_book: BookUpdateSchema, session: AsyncSession = Depends(get_db)
):
    return await book_repository.update_book(
        id, updated_book.model_dump(exclude_unset=True), session
    )


@book_router.get("/books/", response_model=List[BookRetrieveSchema])
async def list_books(session: AsyncSession = Depends(get_db)):
    return await book_repository.get_all_books(session)


@book_router.delete("/books/{id}")
async def delete_book(id: int, session: AsyncSession = Depends(get_db)):
    await book_repository.delete_book(id, session)
    return {"status": status.HTTP_204_NO_CONTENT}
