from datetime import date
from typing import Optional

from pydantic import BaseModel, Field


class BorrowedBookCreateSchema(BaseModel):
    book_id: int = Field(ge=1)
    reader_id: int = Field(ge=1)
    borrow_at: date

    class Config:
        from_attributes = True


class BorrowedBookUpdateSchema(BaseModel):
    borrow_at: Optional[date] = None
    return_at: Optional[date] = None


class BorrowedBookOutputSchema(BorrowedBookCreateSchema):
    id: int = Field(ge=1)
    return_at: Optional[date] = None
