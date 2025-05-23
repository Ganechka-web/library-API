from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from models.book import Book
from exceptions.repositories import RowDoesNotExist


class BookRepository:
    model = Book

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def get_all(self) -> list[Book]:
        async with AsyncSession(self.engine) as session:
            query = select(self.model)
            books = await session.scalars(query)

        return books
    
    async def get_one_by_id(self, book_id: int) -> Book:
        async with AsyncSession(self.engine) as session: 
            try:
                query = select(self.model).where(self.model.id == book_id)
                result = await session.execute(query)
                book = result.scalar_one()
            except NoResultFound as e:
                raise RowDoesNotExist(
                    f'Row with id - {book_id} does not exist'
                ) from e
        return book
    
    async def create_one(self, new_book: Book) -> int:
        async with AsyncSession(self.engine) as session:
            session.add(new_book)
            await session.flush()
            new_book_id = new_book.id

            await session.commit()
        
        return new_book_id
    
    async def update_one(self, book_on_update: Book) -> None:
        async with AsyncSession(self.engine) as session:
            session.add(book_on_update)
            await session.commit()

    async def delete_one(self, book_on_delete: Book) -> None:
        async with AsyncSession(self.engine) as session:
            await session.delete(book_on_delete)
            await session.commit()
            