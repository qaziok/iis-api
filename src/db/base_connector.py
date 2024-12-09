from abc import ABC, abstractmethod
from typing import List

from src.models import Document


class BaseConnector(ABC):
    @abstractmethod
    def add_documents(self, documents: List[Document]) -> List[Document]:
        raise NotImplementedError

    @abstractmethod
    def search(self, query: str, limit: int) -> List[Document]:
        raise NotImplementedError
