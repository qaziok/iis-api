# https://docs.trychroma.com/guides/embeddings

from .base_connector import BaseConnector


class __ChromaConnector(BaseConnector):
    raise NotImplementedError("Chroma connector is not implemented yet")


chroma_connector = __ChromaConnector()
