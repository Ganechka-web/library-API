from fastapi import FastAPI

from api.endpoints.auth import auth_router


app = FastAPI(
    title='Library-API',
    description='API for library'
)

app.include_router(auth_router)
