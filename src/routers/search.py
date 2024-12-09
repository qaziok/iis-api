from fastapi import APIRouter, Request  # type: ignore

from ..db import connector

router = APIRouter(
    prefix='/search',
    tags=['search'],
    responses={404: {'description': 'Not found'}},
)


@router.post("")
async def search(request: Request):
    query = await request.body()
    text = query.decode('utf-8')

    results = connector.search(text, 5)

    return {
        "query": text,
        "results": [doc.to_search_response() for doc in results],
    }
