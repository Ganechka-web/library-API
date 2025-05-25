from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.exc import NoResultFound
from sqlalchemy import select

from models.borrowed_book import BorrowedBook
from exceptions.repositories import RowDoesNotExist


class BorrowedBookRepository:
    model = BorrowedBook

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def get_all(self) -> list[BorrowedBook]:
        async with AsyncSession(self.engine) as session:
            query = select(self.model)
            result = await session.scalars(query)

            return result.all()

    async def get_all_by_reader_id(self, reader_id: int) -> list[BorrowedBook]:
        async with AsyncSession(self.engine) as session:
            query = select(self.model).where(self.model.reader_id == reader_id)
            result = await session.scalars(query)

            return result.all()

    async def get_all_by_book_id(self, book_id: int) -> list[BorrowedBook]:
        async with AsyncSession(self.engine) as session:
            query = select(self.model).where(self.model.book_id == book_id)
            result = await session.scalars(query) 

            return result.all()
        
    async def get_one_by_id(self, borrowed_book_id: int) -> BorrowedBook:
        async with AsyncSession(self.engine) as session:
            try: 
                query = select(self.model).where(self.model.id == borrowed_book_id)
                result = await session.execute(query)
                borrowed_book = result.scalar_one()
            except NoResultFound as e:
                raise RowDoesNotExist(
                    f'Row with id - {borrowed_book_id}'
                    'does not exist'
                ) from e
        
        return borrowed_book
    
    async def get_one_by_reader_id_and_book_id(
            self, reader_id: int, book_id: int
    ) -> BorrowedBook:
        async with AsyncSession(self.engine) as session:
            try:
                query = (select(self.model)
                        .where(
                            self.model.reader_id == reader_id,
                            self.model.book_id == book_id))
                result = await session.execute(query)
                borrowed_book = result.scalar_one()
            except NoResultFound as e:
                raise RowDoesNotExist(
                    f'Row with reader_id - {reader_id} '
                    f'and book_id - {book_id}'
                    'does not exist'
                ) from e
            
        return borrowed_book

    async def create_one(self, new_borrowed_book: BorrowedBook) -> int:
        async with AsyncSession(self.engine) as session:
            session.add(new_borrowed_book)
            await session.flush()
            new_borrowed_book_id = new_borrowed_book.id

            await session.commit()

            return new_borrowed_book_id
    
    async def update_one(self, borrowed_book_on_update: BorrowedBook) -> None:
        async with AsyncSession(self.engine) as session:
            session.add(borrowed_book_on_update)
            await session.commit()

    async def delete_one(self, borrowed_book_on_delete: BorrowedBook) -> None:
        async with AsyncSession(self.engine) as session:
            await session.delete(borrowed_book_on_delete)
            await session.commit() 
            