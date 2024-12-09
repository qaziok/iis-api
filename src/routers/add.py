from fastapi import APIRouter, HTTPException, Request  # type: ignore

from ..services.splitter import splitter
from ..db import connector

router = APIRouter(
    prefix='/add',
    tags=['add'],
    responses={404: {'description': 'Not found'}},
)


@router.post("")
async def add(request: Request):
    input_data = await request.body()
    text = input_data.decode('utf-8')
    url = request.query_params.get('url')

    if not text:
        return HTTPException(status_code=400, detail="No text provided")

    if not url:
        return HTTPException(status_code=400, detail="No URL provided")

    documents = splitter.to_documents(text, url=url)
    results = connector.add_documents(documents)

    return [doc.to_add_response() for doc in results]
