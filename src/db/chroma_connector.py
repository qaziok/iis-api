# https://docs.trychroma.com/guides/embeddings

from src.db import BaseConnector


class _ChromaConnector(BaseConnector):
    raise NotImplementedError("Chroma connector is not implemented yet")


chroma_connector = _ChromaConnector()
