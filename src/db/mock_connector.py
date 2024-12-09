import random
from typing import List

from .base_connector import BaseConnector
from ..models import Document


class __MockConnector(BaseConnector):
    def __init__(self):
        self.documents = {}

    def add_documents(self, documents: List[Document]) -> List[Document]:
        for document in documents:
            self.documents[document.id] = document

        return documents

    def search(self, query: str, limit: int) -> List[Document]:
        random.seed(hash(query))

        if not len(self.documents):
            return []

        return random.choices(list(self.documents.values()), k=limit)


mock_connector = __MockConnector()
