from typing import Annotated

from fastapi import APIRouter, Path, HTTPException, Depends, status

from core.database import async_engine
from dependencies import get_current_user
from repositories.reader import ReaderRepository
from services.reader import ReaderService
from exceptions.services import ReaderDoesNotExist, ReaderEmailAlreadyExists
from schemas.reader import (
    ReaderOutputSchema,
    ReaderCreateSchema,
    ReaderUpdateSchema
)


reader_router = APIRouter(prefix='/readers', tags=['reader'],
                          dependencies=[Depends(get_current_user)])
reader_repository = ReaderRepository(async_engine)
reader_service = ReaderService(reader_repository)


@reader_router.get('/')
async def get_all() -> list[ReaderOutputSchema]:
    readers = await reader_service.get_all()

    return readers


@reader_router.get('/{reader_id}')
async def get_one_by_id(reader_id: Annotated[int, Path()]) -> ReaderOutputSchema:
    try:
        reader = await reader_service.get_one_by_id(reader_id=reader_id)
    except ReaderDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Reader not found'
        )

    return reader


@reader_router.post('/create/')
async def create_one(new_reader: ReaderCreateSchema) -> int:
    try:
        new_reader_id = await reader_service.create_one(new_reader=new_reader)
    except ReaderEmailAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='Reader email already exists'               
        )
    return new_reader_id


@reader_router.patch('/update/{reader_id}')
async def update_one(
    reader_id: Annotated[int, Path()], 
    reader_on_update: ReaderUpdateSchema
) -> None:
    try:
        await reader_service.update_one(reader_id=reader_id, 
                                        reader_on_update=reader_on_update)
    except ReaderDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Reader not found'
        )
    except ReaderEmailAlreadyExists:
        raise HTTPException(
            status.HTTP_409_CONFLICT,
            detail='Reader email already exists'               
        )
    

@reader_router.delete('/delete/{reader_id}')
async def delete_one(reader_id: Annotated[int, Path()]) -> None:
    try:
        await reader_service.delete_one(reader_id=reader_id)
    except ReaderDoesNotExist:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='Reader not found'
        )
    