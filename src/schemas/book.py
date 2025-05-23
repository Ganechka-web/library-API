from typing import Optional

from pydantic import BaseModel, Field


class BookCreateSchema(BaseModel):
    title: str
    autor: str
    publish_year: int = Field(ge=1)
    isbn: str
    instances: int = Field(ge=1)
    description: str

    class Config:
        from_attributes=True


class BookUpdateSchema(BookCreateSchema):
    title: Optional[str] = None
    autor: Optional[str] = None
    publish_year: Optional[int] = Field(ge=1, default=None)
    isbn: Optional[str] = None
    instances: Optional[int] = Field(ge=1, default=None)
    description: Optional[str] = None


class BookOutputSchema(BookUpdateSchema):
    id: int


class BookSchema(BookCreateSchema):
    id: int
