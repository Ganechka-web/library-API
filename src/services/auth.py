from repositories.auth import AuthRepository
from exceptions.services import (
    UserDoesNotExist,
    UserPasswordVerificationFailedError
)
from exceptions.repositories import RowDoesNotExist
from models.user import User
from security.password import get_password_hash, check_password
from security.jwt import get_signed_jwt
from schemas.auth import (
    UserRegisterationSchema,
    UserLoginSchema,
    UserSchema
)


class AuthService:
    def __init__(self, repository: AuthRepository):
        self.repository = repository

    async def register(self, new_user: UserRegisterationSchema) -> int:
        new_user_password_hash = get_password_hash(
            new_user.password
        )
        new_user.password = new_user_password_hash

        new_user = User(**new_user.model_dump())
        new_user_id = await self.repository.register(new_user=new_user)

        return new_user_id
    
    async def get_one_by_id(self, user_id: int) -> UserSchema:
        try:
            user = await self.repository.get_one_by_id(user_id=user_id)
        except RowDoesNotExist as e:
            raise UserDoesNotExist(
                f'User with id - {user_id} ' \
                f'does not exist'
            ) from e
        
        return UserSchema.model_validate(user)
    
    async def login(self, user_credentials: UserLoginSchema) -> str:
        """logins user and retrun jwt access token"""
        try:
            user = await self.repository.get_one_by_email(
                email=user_credentials.email
            )
        except RowDoesNotExist as e:
            raise UserDoesNotExist(
                f'User with email - {user_credentials.email} ' \
                f'does not exist'
            ) from e
        
        is_passwords_equal = check_password(
            user_credentials.password,
            user.password
        )
        if is_passwords_equal:
            user_token = get_signed_jwt(user_id=user.id)
        else:
            raise UserPasswordVerificationFailedError(
                f'User with email - {user_credentials.email}' \
                'didn`t pass verification by password'
            )
        
        return user_token
    