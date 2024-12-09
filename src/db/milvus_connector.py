# https://milvus.io/docs/integrate_with_sentencetransformers.md

from .base_connector import BaseConnector


class __MilvusConnector(BaseConnector):
    raise NotImplementedError("Milvus connector is not implemented yet")


milvus_connector = __MilvusConnector()
