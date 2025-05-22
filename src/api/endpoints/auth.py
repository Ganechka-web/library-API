from fastapi import (
    APIRouter, HTTPException, 
    status, Response
)

from core.database import async_engine
from repositories.auth import AuthRepository
from services.auth import AuthService
from exceptions.services import (
    UserDoesNotExist,
    UserPasswordVerificationFailedError
)
from schemas.auth import (
    UserRegisterationSchema,
    UserLoginSchema
)


auth_router = APIRouter(prefix='/auth')
auth_repository = AuthRepository(engine=async_engine)
auth_service = AuthService(repository=auth_repository)


@auth_router.post('/register/')
async def register(new_user: UserRegisterationSchema) -> int:
    new_user_id = await auth_service.register(new_user=new_user)

    return new_user_id


@auth_router.post('/login/')
async def login(response: Response, user_credentials: UserLoginSchema) -> str:
    try:
        user_access_token = await auth_service.login(
            user_credentials=user_credentials)
    except UserDoesNotExist as e:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail='user not found'
        ) from e
    except UserPasswordVerificationFailedError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='unvalid password'
        ) from e
    
    response.set_cookie('access_token', 
                        user_access_token, 
                        httponly=True)
    return user_access_token
    