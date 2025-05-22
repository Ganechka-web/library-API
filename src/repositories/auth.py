from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.exc import DatabaseError
from sqlalchemy import select

from models.user import User
from exceptions.repositories import RowDoesNotExist


class AuthRepository:
    model = User

    def __init__(self, engine: AsyncEngine):
        self.engine = engine

    async def register(self, new_user: User) -> int:
        """registers new user and reurns his id"""
        async with AsyncSession(self.engine) as session:
            session.add(new_user)
            await session.flush()
            new_user_id = new_user.id

            await session.commit()

            return new_user_id
    
    async def get_one_by_id(self, user_id: int):
        async with AsyncSession(self.engine) as session:
            try: 
                query = select(self.model).where(self.model.id == user_id)
                user = await session.scalar(query)
            except DatabaseError as e:
                raise RowDoesNotExist(
                    f'Row with id - {user_id} does not exist'
                ) from e
            
            return user
    
    async def get_one_by_email(self, email: str) -> User:
        async with AsyncSession(self.engine) as session:
            try:
                query = select(self.model).where(self.model.email == email)
                user = await session.scalar(query)
            except DatabaseError as e:
                raise RowDoesNotExist(
                    f'Row with email - {email} does not exist'
                ) from e
            
            return user
    