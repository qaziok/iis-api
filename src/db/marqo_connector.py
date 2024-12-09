# https://docs.marqo.ai/latest/examples/marqo/text-search/#introduction

import logging
from marqo import Client
from marqo.errors import IndexAlreadyExistsError

from .base_connector import BaseConnector
from src import pyenv
from src.models import Document


def __ad_documents_to_marqo(documents: list[Document]) -> list[dict]:
    """Transforms a list of Document objects to a list of dictionaries that can be added to Marqo"""
    return [
        {
            "_id": document.id,
            "data": document.data,
            "url": document.url,
        } for document in documents
    ]


def __ad_marqo_to_documents(documents: list[Document], response: list[dict]) -> list[Document]:
    """Transforms the add documents response from Marqo to a list of Document objects"""
    response = []
    for doc in response:
        og_doc = next((d for d in documents if d.id == doc["_id"]), None)
        if og_doc:
            response.append(
                Document(
                    id=doc["_id"],
                    data=og_doc["data"],
                    url=og_doc["url"],
                )
            )


def __s_marqo_to_documents(response: list[dict]) -> list[Document]:
    """Transforms the search response from Marqo to a list of Document objects"""
    return [
        Document(
            id=doc["_id"],
            data=doc["data"],
            url=doc["url"],
            score=doc["_score"],
        ) for doc in response
    ]


class __MarqoConnector(BaseConnector):
    def __init__(self):
        self.client = Client(pyenv.settings.marqo_url)
        self.index_name = pyenv.settings.marqo_index_name
        try:
            self.client.create_index(
                self.index_name, model=pyenv.settings.marqo_model)
        except IndexAlreadyExistsError:
            logging.info(f"Index '{self.index_name}' already exists")

    @property
    def index(self):
        return self.client.index(self.index_name)

    def add_documents(self, documents: list[Document]) -> list[Document]:
        docs = __ad_documents_to_marqo(documents)

        result = self.index.add_documents(docs, tensor_fields=["data"])

        if result["errors"]:
            logging.error(f"Error adding documents: {docs}")

        return __ad_marqo_to_documents(documents, result["items"])

    def search(self, query: str, limit: int) -> list[Document]:
        data = self.index.search(query, limit=limit)

        return __s_marqo_to_documents(data['hits'])


marqo_connector = __MarqoConnector()
