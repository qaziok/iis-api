from fastapi import FastAPI  # type: ignore

from .routers import add, search

app = FastAPI(
    title='IIS-API',
    description='API for vector search',
    version='0.2',
)

app.include_router(add.router)
app.include_router(search.router)
