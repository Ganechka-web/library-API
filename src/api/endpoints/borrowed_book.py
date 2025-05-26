from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, Depends, status

from core.database import async_engine
from dependencies import get_current_user
from repositories.borrowed_book import BorrowedBookRepository
from services.borrowed_book import BorrowedBookService
from exceptions.services import (
    BorrowedBookCountPerReaderError,
    BorrowedBookUnableToBorrowBook,
    BorrowedBookDoesNotExist,
    BorrowedBookAlreadyBorrowed,
    BorrowedBookAlreadyReturned
)
from api.endpoints.book import book_service


borrowed_book_router = APIRouter(prefix="/borrowed-book", tags=["borrowed-book"],
                                 dependencies=[Depends(get_current_user)])
borrowed_book_repository = BorrowedBookRepository(async_engine)
borrowed_book_service = BorrowedBookService(
    repository=borrowed_book_repository, book_service=book_service
)


@borrowed_book_router.post("/borrow/{book_id}/{reader_id}")
async def borrow_one(
    book_id: Annotated[int, Path()], reader_id: Annotated[int, Path()]
) -> int:
    try:
        new_borrowed_book_id = await borrowed_book_service.create_one(
            book_id=book_id, reader_id=reader_id
        )
    except BorrowedBookCountPerReaderError:
        raise HTTPException(
            status.HTTP_409_CONFLICT, detail="Reader already have got 3 borrowed books"
        )
    except BorrowedBookUnableToBorrowBook:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Now unable to borrow book, haven`t got any instances yet",
        )  
    except BorrowedBookAlreadyBorrowed:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail="Reader have already borrowed this book"
        )
    return new_borrowed_book_id


@borrowed_book_router.post("/return/{book_id}/{reader_id}")
async def return_one(
    book_id: Annotated[int, Path()], reader_id: Annotated[int, Path()]
) -> None:
    try:
        await borrowed_book_service.return_one(
            reader_id=reader_id, book_id=book_id
        )
    except BorrowedBookDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='BorrowedBook not found'
        )
    except BorrowedBookAlreadyReturned:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='BorrowedBook has already returned'
        )
    