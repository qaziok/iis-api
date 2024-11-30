from fastapi import APIRouter, HTTPException, Request  # type: ignore

router = APIRouter(
    prefix='/add',
    tags=['add'],
    responses={404: {'description': 'Not found'}},
)


@router.post("/")
async def add(request: Request):
    input_data = await request.body()
    text = input_data.decode('utf-8')
    url = request.query_params.get('url')

    if not text:
        return HTTPException(status_code=400, detail="No text provided")

    if not url:
        return HTTPException(status_code=400, detail="No URL provided")

    # Split into words
    words = text.split()

    # Create chunks of 1000 tokens
    chunk_size = 500
    chunks = [words[i:i + chunk_size]
              for i in range(0, len(words), chunk_size)]

    # Create list of dictionaries with id and data, where data is a chunk of words joined back
    result = []
    for i, chunk in enumerate(chunks):
        chunk_dict = {
            "id": str(i),
            "data": " ".join(chunk),
            "url": url
        }
        # Add previous chunk if exists
        if i > 0:
            chunk_dict["prev"] = " ".join(chunks[i-1])
        # Add next chunk if exists
        if i < len(chunks) - 1:
            chunk_dict["next"] = " ".join(chunks[i+1])

        result.append(chunk_dict)

    return result
