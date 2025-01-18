# https://docs.trychroma.com/guides/embeddings

# autopep8: off
# weird chromadb fix
__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

from chromadb import HttpClient
from chromadb.utils import embedding_functions

from src import pyenv
from src.db import BaseConnector
from src.models import Document
# autopep8: on


class _ChromaConnector(BaseConnector):
    def __init__(self):
        self.client = HttpClient(
            host=pyenv.settings.chroma_host, port=int(pyenv.settings.chroma_port))
        self.index = self.client.get_or_create_collection(
            name=pyenv.settings.index_name,
            embedding_function=self.embedding_function,
            metadata=self.metadata
        )

    @property
    def embedding_function(self):
        return embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=pyenv.settings.chroma_model,
            device=pyenv.settings.chroma_device
        )

    @property
    def metadata(self):
        initial = {
            "hnsw:space": pyenv.settings.chroma_hnsw_space,
            "hnsw:ef_construction": pyenv.settings.chroma_hnsw_ef_construction,
            "hnsw:search_ef": pyenv.settings.chroma_hnsw_search_ef,
            "hnsw:M": pyenv.settings.chroma_hnsw_m
        }

        metadata = {key: value for key, value in initial.items()
                    if value is not None}

        return metadata if metadata else None

    def add_documents(self, documents: list[Document]) -> list[Document]:
        docs, ids, meta = self.__ad_documents_to_chroma(documents)

        self.index.upsert(ids=ids, metadatas=meta, documents=docs)

        return documents

    def search(self, query: str, limit: int) -> list[Document]:
        data = self.index.query(query_texts=[query], n_results=limit)

        return self.__s_chroma_to_documents(data)

    @staticmethod
    def __ad_documents_to_chroma(documents: list[Document]):
        data = [(document.data, str(document.id),
                 {"url": document.url}) for document in documents]

        docs, ids, meta = zip(*data)
        return list(docs), list(ids), list(meta)

    @staticmethod
    def __s_chroma_to_documents(response) -> list[Document]:
        zipped = response['documents'][0], response['ids'][0], response['metadatas'][0], response['distances'][0]

        return [Document(id=id, data=doc, url=meta['url'], score=1-dist) for doc, id, meta, dist in zip(*zipped)]


chroma_connector = _ChromaConnector()
