from typing import Annotated

from fastapi import HTTPException, status, Cookie
from jose.exceptions import ExpiredSignatureError, JWTError

from api.endpoints.auth import auth_service
from security.jwt import get_jwt_payload
from exceptions.services import UserDoesNotExist


async def get_current_user(access_token: Annotated[str, Cookie()]):
    try: 
        payload = get_jwt_payload(token=access_token)
        user_id = payload['user_id']
        if user_id is None:
            raise JWTError()
        current_user = await auth_service.get_one_by_id(user_id=user_id)

    except UserDoesNotExist as e:
           raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                detail='user not found'
           ) from e
    except ExpiredSignatureError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='token expired'
        ) from e
    except JWTError as e:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail='invalid token'
        ) from e
    
    return current_user