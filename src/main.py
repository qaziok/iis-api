from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.routers import add, search

app = FastAPI(
    title='IIS-API',
    description='API for vector search',
    version='0.3',
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
