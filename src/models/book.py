from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Text

from core.database import Base


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    autor: Mapped[str] = mapped_column(nullable=False)
    publish_year: Mapped[int]
    isbn: Mapped[str] = mapped_column(unique=True)
    instances: Mapped[int] = mapped_column(default=1)
    description: Mapped[str] = mapped_column(Text, nullable=True)
    