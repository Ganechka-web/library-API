from fastapi import FastAPI

from api.endpoints.auth import auth_router
from api.endpoints.book import book_router
from api.endpoints.reader import reader_router
from api.endpoints.borrowed_book import borrowed_book_router


app = FastAPI(
    title='Library-API',
    description='API for library'
)

app.include_router(auth_router)
app.include_router(book_router)
app.include_router(reader_router)
app.include_router(borrowed_book_router)
