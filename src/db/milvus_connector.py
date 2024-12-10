# https://milvus.io/docs/integrate_with_sentencetransformers.md

from src.db import BaseConnector


class _MilvusConnector(BaseConnector):
    raise NotImplementedError("Milvus connector is not implemented yet")


milvus_connector = _MilvusConnector()
