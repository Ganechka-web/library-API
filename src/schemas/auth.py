from pydantic import BaseModel


class UserRegisterationSchema(BaseModel):
    email: str
    password: str
    
    class Config:
        from_attributes = True 


class UserLoginSchema(UserRegisterationSchema):
    pass


class UserSchema(UserRegisterationSchema):
    id: int
