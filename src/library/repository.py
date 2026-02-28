from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.exceptions import NotFoundException
from src.library.models import BookModel, ReviewModel


class BookRepository:
    async def create_book(self, book_data, session: AsyncSession):
        book = BookModel(**book_data)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    async def get_book_by_id(self, id: int, session: AsyncSession):
        res = await session.execute(select(BookModel).where(BookModel.id == id))
        return res.scalar_one_or_none()

    async def get_book_or_raise(self, id: int, session: AsyncSession):
        book = await self.get_book_by_id(id, session)
        if not book:
            raise NotFoundException("Book", id)
        return book

    async def get_all_books(self, session: AsyncSession):
        res = await session.execute(select(BookModel))
        return res.scalars().all()

    async def update_book(self, id: int, book_data, session: AsyncSession):
        book = await self.get_book_or_raise(id, session)

        for k, v in book_data.items():
            setattr(book, k, v)

        await session.commit()
        await session.refresh(book)
        return book

    async def delete_book(self, id: int, session: AsyncSession):
        book = await self.get_book_or_raise(id, session)

        await session.delete(book)
        await session.commit()

    async def get_or_none_by_external_id(self, external_id: str, session: AsyncSession):
        stmt = select(BookModel).where(BookModel.external_id == external_id)
        book = (await session.execute(stmt)).scalar_one_or_none()
        return book


class ReviewRepository:
    async def create_review(self, review_data: dict, session: AsyncSession):
        review = ReviewModel(**review_data)

        session.add(review)
        await session.commit()
        await session.refresh(review)
        return review


book_repository = BookRepository()
review_respository = ReviewRepository()
