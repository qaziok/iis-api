from fastapi import APIRouter, Query, Body
from src.services import splitter
from src.db import connector

router = APIRouter(
    prefix='/add',
    tags=['add'],
    responses={404: {'description': 'Not found'}},
)


@router.post("")
async def add(
        text: str = Body(..., description="Text to index for search",
                         media_type="text/plain"),
        url: str = Query(..., description="URL of the text to index")
):
    documents = splitter.to_documents(text, url=url)
    if (len(documents) > 0):
        results = connector.add_documents(documents)
        return [doc.to_add_response() for doc in results]
    else:
        return []
