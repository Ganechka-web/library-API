from typing import Optional

from pydantic import BaseModel, EmailStr


class ReaderCreateSchema(BaseModel):
    name: str
    email: EmailStr

    class Config:
        from_attributes = True


class ReaderUpdateSchema(ReaderCreateSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class ReaderOutputSchema(ReaderCreateSchema):
    id: int
