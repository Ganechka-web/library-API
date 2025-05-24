from repositories.reader import ReaderRepository
from models.reader import Reader
from exceptions.repositories import RowDoesNotExist, RowAlreadyExists
from exceptions.services import ReaderDoesNotExist, ReaderEmailAlreadyExists
from schemas.reader import (
    ReaderOutputSchema,
    ReaderCreateSchema,
    ReaderUpdateSchema
)


class ReaderService:
    def __init__(self, repository: ReaderRepository):
        self.repository = repository

    async def get_all(self) -> list[ReaderOutputSchema]: 
        readers_orm = await self.repository.get_all()
        readers = [ReaderOutputSchema.model_validate(reader)
                   for reader in readers_orm]
        
        return readers
    
    async def get_one_by_id(self, reader_id: int) -> ReaderOutputSchema:
        try:
            reader_orm = await self.repository.get_one_by_id(reader_id=reader_id)
            reader = ReaderOutputSchema.model_validate(reader_orm)
        except RowDoesNotExist as e:
            raise ReaderDoesNotExist(
                f'Reader with id - {reader_id}'
                'does not exist'
            ) from e
        
        return reader
    
    async def create_one(self, new_reader: ReaderCreateSchema) -> int:
        try:
            new_reader_orm = Reader(**new_reader.model_dump())
            new_reader_id = await self.repository.create_one(new_reader=new_reader_orm)
        except RowAlreadyExists as e:
            raise ReaderEmailAlreadyExists(
                f'Reader with email - {new_reader.email}' 
                'already exists'
            ) from e
        
        return new_reader_id
    
    async def update_one(self, reader_id: int, reader_on_update: ReaderUpdateSchema) -> None:
        try:
            old_reader_orm = await self.repository.get_one_by_id(reader_id=reader_id)
        except RowDoesNotExist as e:
            raise ReaderDoesNotExist(
                f'Reader with id - {reader_id}'
                'does not exist'
            ) from e 

        for field, value in reader_on_update.model_dump(exclude_unset=True).items():
            setattr(old_reader_orm, field, value)

        try:
            await self.repository.update_one(reader_on_update=old_reader_orm)
        except RowAlreadyExists as e:
            raise ReaderEmailAlreadyExists(
                f'Reader with email - {reader_on_update.email}' 
                'already exists'
            ) from e

    async def delete_one(self, reader_id: int) -> None:
        try:
            reader_on_delete_orm = await self.repository.get_one_by_id(
                                                             reader_id=reader_id)
        except RowDoesNotExist as e:
            raise ReaderDoesNotExist(
                f'Reader with id - {reader_id}'
                'does not exist'
            ) from e

        await self.repository.delete_one(reader_on_delete=reader_on_delete_orm)
