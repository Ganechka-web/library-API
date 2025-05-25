from repositories.book import BookRepository
from exceptions.repositories import RowDoesNotExist, RowAlreadyExists
from exceptions.services import (
    BookDoesNotExist, 
    BookISBNAlreadyExists,
    BookDoesNotHaveAnyInstancesError
)
from models.book import Book
from schemas.book import (
    BookOutputSchema,
    BookCreateSchema,
    BookUpdateSchema
)


class BookService:
    def __init__(self, repository: BookRepository):
        self.repository = repository
    
    async def get_all(self) -> list[BookOutputSchema]:
        books_orm = await self.repository.get_all()
        books = [BookOutputSchema.model_validate(book) 
                 for book in books_orm]
        return books
    
    async def get_one_by_id(self, book_id: int) -> BookOutputSchema:
        try:
            book_orm = await self.repository.get_one_by_id(book_id=book_id)
        except RowDoesNotExist as e:
            raise BookDoesNotExist(
                f'Book with id - {book_id}'
                'does not exist'
            ) from e
        book = BookOutputSchema.model_validate(book_orm)

        return book
    
    async def create_one(self, new_book: BookCreateSchema) -> int:
        try: 
            new_book_orm = Book(**new_book.model_dump())
            new_book_id = await self.repository.create_one(new_book=new_book_orm)
        except RowAlreadyExists as e:
            raise BookISBNAlreadyExists(
                f'Book with isbn - {new_book.isbn}, '
                'already exists'
            ) from e

        return new_book_id
    
    async def update_one(self, book_id: int, book_on_update: BookUpdateSchema) -> None:
        old_book_orm = await self.get_one_by_id(book_id=book_id)

        for field, value in book_on_update.model_dump(exclude_unset=True).items():
            setattr(old_book_orm, field, value)
        
        await self.repository.update_one(book_on_update=old_book_orm)

    async def delete_one(self, book_id: int) -> None:
        book_on_delete = await self.get_one_by_id(book_id=book_id)
        await self.repository.delete_one(book_on_delete=book_on_delete)

    async def increase_book_instances(self, book_id: int, amount: int = 1) -> None:
        """increase book instances amount and updates book"""
        try:
            book_orm = await self.repository.get_one_by_id(book_id=book_id)
        except RowDoesNotExist as e:
            raise BookDoesNotExist(
                f'Book with id - {book_id}'
                'does not exist'
            ) from e

        book_orm.instances += amount

        await self.repository.update_one(book_on_update=book_orm)

    async def decrease_book_instances(self, book_id: int, amount: int = 1) -> None:
        """decrease book instances amount and updates book"""
        try:
            book_orm = await self.repository.get_one_by_id(book_id=book_id)
        except RowDoesNotExist as e:
            raise BookDoesNotExist(
                f'Book with id - {book_id}'
                'does not exist'
            ) from e

        if book_orm.instances == 0:
            raise BookDoesNotHaveAnyInstancesError(
                'Can`t decrease book instances amount less than 0'
            ) 
        
        book_orm.instances -= amount

        await self.repository.update_one(book_on_update=book_orm)
