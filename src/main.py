from fastapi import FastAPI  # type: ignore
from fastapi.middleware.cors import CORSMiddleware

from .routers import add, search

app = FastAPI(
    title='IIS-API',
    description='API for vector search',
    version='0.2',
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(add.router)
app.include_router(search.router)
