from datetime import datetime

from repositories.borrowed_book import BorrowedBookRepository
from exceptions.repositories import RowDoesNotExist
from models.borrowed_book import BorrowedBook
from services.book import BookService
from exceptions.services import (
    BorrowedBookDoesNotExist,
    BorrowedBookCountPerReaderError,
    BorrowedBookInvalidReturnDateError,
    BorrowedBookUnableToBorrowBook,
    BorrowedBookAlreadyBorrowed,
    # Book errors
    BookDoesNotHaveAnyInstancesError,
)
from schemas.borrowed_book import (
    BorrowedBookOutputSchema,
    BorrowedBookCreateSchema,
    BorrowedBookUpdateSchema,
)


class NoMoreThanTreeBorrowedBooksValidator:
    """validates reader`s borrowed books amount"""

    def __init__(self, repository: BorrowedBookRepository) -> None:
        self.repository = repository

    async def is_satisfied(self, reader_id: int):
        reader_borrowed_books = await self.repository.get_all_by_reader_id(
            reader_id=reader_id
        )
        if len(reader_borrowed_books) < 3:
            raise BorrowedBookCountPerReaderError(
                "BorrowedBook can be borrowed, "
                f"Reader with id = {reader_id} already "
                "have 3 borrowed books"
            )


class BorrowedBookService:
    def __init__(
        self, repository: BorrowedBookRepository, book_service: BookService
    ) -> None:
        self.repository = repository
        # validators
        self.no_more_than_thee_borrowed_books_validator = (
            NoMoreThanTreeBorrowedBooksValidator(self.repository)
        )
        # for managing on book instance count
        self.book_service = book_service

    async def get_all(self) -> list[BorrowedBookOutputSchema]:
        borrowed_books_orm = await self.repository.get_all()
        borrowed_books = [
            BorrowedBookOutputSchema.model_validate(borrowed_book)
            for borrowed_book in borrowed_books_orm
        ]

        return borrowed_books

    async def get_all_by_reader_id(
        self, reader_id: int
    ) -> list[BorrowedBookOutputSchema]:
        borrowed_books_orm = await self.repository.get_all_by_reader_id(
            reader_id=reader_id
        )
        borrowed_books = [
            BorrowedBookOutputSchema.model_validate(borrowed_book)
            for borrowed_book in borrowed_books_orm
        ]

        return borrowed_books

    async def get_all_by_book_id(self, book_id: int) -> list[BorrowedBookOutputSchema]:
        borrowed_books_orm = await self.repository.get_all_by_book_id(book_id=book_id)
        borrowed_books = [
            BorrowedBookOutputSchema.model_validate(borrowed_book)
            for borrowed_book in borrowed_books_orm
        ]

        return borrowed_books

    async def get_one_by_id(self, borrowed_book_id) -> BorrowedBookOutputSchema:
        try:
            borrowed_book_orm = await self.repository.get_one_by_id(
                borrowed_book_id=borrowed_book_id
            )
            borrowed_book = BorrowedBookOutputSchema.model_validate(borrowed_book_orm)
        except RowDoesNotExist as e:
            raise BorrowedBookDoesNotExist(
                f"BorrowedBook with id - {borrowed_book_id} does not exist"
            ) from e

        return borrowed_book

    async def create_one(self, book_id: int, reader_id: int) -> int:
        # check whether reader already have got a borrowed_book
        try:
            self.repository.get_one_by_reader_id_and_book_id(
                reader_id=reader_id, book_id=book_id    
            )
        except RowDoesNotExist:
            pass
        else:
            raise BorrowedBookAlreadyBorrowed(
                "Reader already have BorrowedBook"
            ) 

        self.no_more_than_thee_borrowed_books_validator.is_satisfied(
            reader_id=reader_id
        )

        borrow_at = datetime.now().date()
        new_borrowed_book = BorrowedBookCreateSchema(
            book_id=book_id,
            reader_id=reader_id,
            borrow_at=borrow_at,
        )

        # try to decrease book instances
        try:
            await self.book_service.decrease_book_instances(
                book_id=new_borrowed_book.book_id
            )
        except BookDoesNotHaveAnyInstancesError as e:
            raise BorrowedBookUnableToBorrowBook(
                "Unable to borrow book, haven`t got any instances"
            ) from e

        new_borrowed_book_orm = BorrowedBook(**new_borrowed_book.model_dump())
        new_borrowed_book_id = await self.repository.create_one(
            new_borrowed_book=new_borrowed_book_orm
        )

        return new_borrowed_book_id

    async def update_one(
        self, borrowed_book_id: int, borrowed_book_on_update: BorrowedBookUpdateSchema
    ) -> None:
        try:
            old_borrowed_book = await self.repository.get_one_by_id(
                borrowed_book_id=borrowed_book_id
            )
        except RowDoesNotExist as e:
            raise BorrowedBookDoesNotExist(
                f"BorrowedBook with id - {borrowed_book_id} does not exist"
            ) from e

        # borrow and return date checking
        if borrowed_book_on_update.borrow_at >= borrowed_book_on_update.return_at:
            raise BorrowedBookInvalidReturnDateError(
                "BorrowedBook borrow_at can`t be less or equal than return_at"
            )

        for field, value in old_borrowed_book.model_dump(exclude_unset=True).items():
            setattr(old_borrowed_book, field, value)

        await self.repository.update_one(borrowed_book_on_update=old_borrowed_book)

    async def return_one(self, reader_id: int, book_id) -> None:
        try:
            borrowed_book_on_return_orm = (
                await self.repository.get_one_by_reader_id_and_book_id(
                    reader_id=reader_id, book_id=book_id
                )
            )
        except RowDoesNotExist as e:
            raise BorrowedBookDoesNotExist(
                f"BorrowedBook with reader_id - {reader_id} "
                f"and book_id - {book_id} does not exist"
            ) from e

        # increase book instances amount
        await self.book_service.increase_book_instances(
            book_id=borrowed_book_on_return_orm.book_id
        )

        # set retrun_at date
        borrowed_book_on_return_orm.return_at = datetime.now().date()

        await self.repository.update_one(
            borrowed_book_on_update=borrowed_book_on_return_orm
        )
    
    async def delete_one(self, borrowed_book_on_delete_id: int) -> None:
        try:
            borrowed_book_on_delete_orm = await self.repository.get_one_by_id(
                borrowed_book_id=borrowed_book_on_delete_id
            )
        except RowDoesNotExist as e:
            raise BorrowedBookDoesNotExist(
                f"BorrowedBook with id - {borrowed_book_on_delete_id} does not exist"
            ) from e
        
        await self.repository.delete_one(
            borrowed_book_on_delete=borrowed_book_on_delete_orm
        )
        

