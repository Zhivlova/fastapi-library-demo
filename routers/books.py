from fastapi import APIRouter, status, HTTPException
from database import SessionDep

from schemas.books import SBook, SBookAdd, SBookUpdate
from repository.books import BookRepository

router = APIRouter(prefix="/books", tags=["Книги"])


@router.post("", response_model=SBook, status_code=status.HTTP_201_CREATED)
async def create_book(
    book: SBookAdd, session: SessionDep,
):
    book_model = await BookRepository.add_one(book, session)
    return book_model


@router.get("", response_model=list[SBook], status_code=status.HTTP_200_OK)
async def get_books(session: SessionDep,):
    books = await BookRepository.find_all(session)
    return books


@router.get("/{book_id}", response_model=SBook)
async def get_book(
    session: SessionDep, book_id: int,
):
    book = await BookRepository.get_by_id(session, book_id)
    if book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена",
        )
    return book


@router.put("/{book_id}", response_model=SBook)
async def replace_book(session: SessionDep, book: SBookAdd, book_id: int):
    replaced_book = await BookRepository.replace_book(session, book_id, book)
    if replaced_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена",
        )
    return replaced_book


@router.patch("/{book_id}", response_model=SBook)
async def update_book(session: SessionDep, book: SBookUpdate, book_id: int):
    updated_book = await BookRepository.update_book(session, book_id, book)
    if updated_book is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена",
        )
    return updated_book


@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(session: SessionDep, book_id: int):
    deleted = await BookRepository.delete_book(session, book_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Книга с ID {book_id} не найдена",
        )
    return
