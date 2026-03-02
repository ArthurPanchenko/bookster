import json
from typing import List

import redis.asyncio as redis
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.dependecies import get_current_user
from src.core.db import get_db
from src.core.exceptions import BookServiceError
from src.core.redis_client import get_redis
from src.library.repository import book_repository, review_respository
from src.library.schemas import (
    BookRetrieveSchema,
    BookSchema,
    ReviewCreateSchema,
)
from src.library.service import get_book_by_id, search

book_router = APIRouter()


@book_router.get("/search", description="Search book by title")
async def external_search(q: str):
    try:
        response = await search(q)
    except BookServiceError as e:
        raise HTTPException(status_code=e.status, detail=e.message)
    return response


@book_router.get("/search/{book_id}", description="Get book by external id")
async def book_detail_by_external_id(
    book_id: str,
    session: AsyncSession = Depends(get_db),
    redis_client: redis.Redis = Depends(get_redis),
):

    cached = await redis_client.get(book_id)
    if cached:
        return json.loads(cached)

    book = await book_repository.get_or_none_by_external_id(book_id, session)
    if book is None:
        try:
            response = await get_book_by_id(book_id)
        except BookServiceError as e:
            raise HTTPException(status_code=e.status, detail=e.message)
        return BookRetrieveSchema(
            title=response["title"],
            external_id=response["id"],
            author=response["authors"][0],
        )
    else:
        book = BookRetrieveSchema.model_validate(book)
        book_dict = book.model_dump_json()
        await redis_client.set(book_id, book_dict)
        return book


@book_router.post(
    "/search/{book_external_id}/reviews",
    description="Create review to book by external id. AUTH REQUIRED",
)
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
        book_data = BookSchema(
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


@book_router.get(
    "/books/",
    response_model=List[BookRetrieveSchema],
    description="Get all local-saved books",
)
async def list_books(session: AsyncSession = Depends(get_db)):

    return await book_repository.get_all_books(session)
