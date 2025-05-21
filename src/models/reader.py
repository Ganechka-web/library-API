from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Reader(Base):
    __tablename__ = 'readers'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
