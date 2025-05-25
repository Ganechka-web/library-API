from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class BorrowedBook(Base):
    __tablename__ = 'borrowed_books'

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int]
    reader_id: Mapped[int]
    borrow_at: Mapped[date]
    return_at: Mapped[date] = mapped_column(nullable=True)
    