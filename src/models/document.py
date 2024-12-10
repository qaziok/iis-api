from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Document(BaseModel):
    id: UUID
    data: str
    url: str
    score: Optional[float] = None

    def to_search_response(self):
        return self.model_dump()

    def to_add_response(self):
        return self.model_dump(exclude={'score'})
