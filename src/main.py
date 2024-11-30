from fastapi import FastAPI

from .routers import add, search

app = FastAPI(
    title='renameme',
    description='Fill the description',
    version='0.1',
)

app.include_router(add.router)
app.include_router(search.router)
