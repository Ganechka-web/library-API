from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy import select

from models.reader import Reader
from exceptions.repositories import RowDoesNotExist, RowAlreadyExists


class ReaderRepository:
    model = Reader

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    async def get_all(self) -> list[Reader]:
        async with AsyncSession(self.engine) as session:
            query = select(self.model)
            readers = await session.scalars(query)

        return readers
    
    async def get_one_by_id(self, reader_id: int) -> Reader:
        async with AsyncSession(self.engine) as session: 
            try:
                query = select(self.model).where(self.model.id == reader_id)
                result = await session.execute(query)
                reader = result.scalar_one()
            except NoResultFound as e:
                raise RowDoesNotExist(
                    f'Row with id - {reader_id} does not exist'
                ) from e
        return reader
    
    async def create_one(self, new_reader: Reader) -> int:
        async with AsyncSession(self.engine) as session:
            try:
                session.add(new_reader)
                await session.flush()
                new_reader_id = new_reader.id

                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise RowAlreadyExists(
                    'Row with the same field '
                    'already exists'
                ) from e
        
        return new_reader_id
    
    async def update_one(self, reader_on_update: Reader) -> None:
        async with AsyncSession(self.engine) as session:
            try: 
                session.add(reader_on_update)
                await session.commit()
            except IntegrityError as e:
                await session.rollback()
                raise RowAlreadyExists(
                    'Row with the same field '
                    'already exists'
                ) from e

    async def delete_one(self, reader_on_delete: Reader) -> None:
        async with AsyncSession(self.engine) as session:
            await session.delete(reader_on_delete)
            await session.commit()