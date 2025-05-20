from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import URL

from core.settings import postgres_settings


postgres_url = URL.create(
    drivername='postgresql+asyncpg',
    host=postgres_settings.host,
    port=postgres_settings.port,
    username=postgres_settings.user,
    password=postgres_settings.password,
    database=postgres_settings.db
).render_as_string(hide_password=False)

async_engine = create_async_engine(
    postgres_url,
    echo=True
)


# base model class
class Base(DeclarativeBase):
    pass
