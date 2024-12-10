from fastapi import APIRouter, Body, Query

from src.db import connector

router = APIRouter(
    prefix='/search',
    tags=['search'],
    responses={404: {'description': 'Not found'}},
)


@router.post("")
async def search(
    query: str = Body(..., media_type="text/plain",
                      description="Query to search"),
    limit: int = Query(5, description="Number of results to return"),

):
    results = connector.search(query, limit)

    return {
        "query": query,
        "results": [doc.to_search_response() for doc in results],
    }
