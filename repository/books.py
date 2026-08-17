from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from models.books import BooksModel
from schemas.books import SBookAdd, SBookUpdate


class BookRepository:
    @classmethod
    async def add_one(cls, data: SBookAdd, session: AsyncSession) -> BooksModel:
        book_dict = data.model_dump()
        book = BooksModel(**book_dict)
        session.add(book)
        await session.commit()
        await session.refresh(book)
        return book

    @classmethod
    async def find_all(cls, session: AsyncSession):
        query = select(BooksModel)
        result = await session.execute(query)
        books_models = result.scalars().all()
        return books_models

    @classmethod
    async def get_by_id(
        cls,
        session: AsyncSession,
        book_id: int,
    ) -> BooksModel | None:
        query = select(BooksModel).where(BooksModel.id == book_id)
        result = await session.execute(query)
        return result.scalar_one_or_none()

    @classmethod
    async def replace_book(
        cls,
        session: AsyncSession,
        book_id: int,
        data: SBookAdd,
    ) -> BooksModel | None:

        book_instance = await BookRepository.get_by_id(session, book_id)

        if book_instance is None:
            return None

        book_dict = data.model_dump()
        for key, value in book_dict.items():
            setattr(book_instance, key, value)
        session.add(book_instance)
        await session.commit()
        await session.refresh(book_instance)

        return book_instance

    @classmethod
    async def update_book(
        cls,
        session: AsyncSession,
        book_id: int,
        data: SBookUpdate,
    ) -> BooksModel | None:

        book_instance = await BookRepository.get_by_id(session, book_id)

        if book_instance is None:
            return None

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(book_instance, key, value)

        session.add(book_instance)
        await session.commit()
        await session.refresh(book_instance)

        return book_instance

    @classmethod
    async def delete_book(cls, session: AsyncSession, book_id: int) -> bool:
        stmt = delete(BooksModel).where(BooksModel.id == book_id)

        result = await session.execute(stmt)
        await session.commit()

        return result.rowcount > 0
