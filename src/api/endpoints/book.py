from typing import Annotated

from fastapi import APIRouter, Depends, Path, HTTPException, status

from core.database import async_engine
from repositories.book import BookRepository
from services.book import BookService
from dependencies import get_current_user
from exceptions.services import BookDoesNotExist
from schemas.book import (
    BookOutputSchema,
    BookCreateSchema,
    BookUpdateSchema
)


book_router = APIRouter(prefix='/books', tags=['book'], 
                        dependencies=[Depends(get_current_user)])
book_repository = BookRepository(async_engine)
book_service = BookService(book_repository)


@book_router.get('/')
async def get_all() -> list[BookOutputSchema]:
    books = await book_service.get_all()

    return books  


@book_router.get('/{book_id}')
async def get_one_by_id(
    book_id = Annotated[int, Path()]
) -> BookOutputSchema:
    try:
        book = await book_service.get_one_by_id(book_id=book_id)
    except BookDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    return book


@book_router.post('/create/')
async def create_one(new_book: BookCreateSchema) -> int:
    new_book_id = await book_service.create_one(new_book=new_book)

    return new_book_id


@book_router.patch('/update/{book_id}')
async def update_one(
    book_id: Annotated[int, Path()], 
    book_on_update: BookUpdateSchema
) -> None:
    try: 
        await book_service.update_one(book_id=book_id,
                                      book_on_update=book_on_update)
    except BookDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )


@book_router.delete('/delete/{book_id}')
async def delete_one(book_id: Annotated[int, Path]) -> None:
    try: 
        await book_service.delete_one(book_id=book_id)
    except BookDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Book not found'
        )
    