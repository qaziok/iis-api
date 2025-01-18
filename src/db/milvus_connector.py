# https://milvus.io/docs/integrate_with_sentencetransformers.md

from pymilvus import MilvusClient, DataType, FieldSchema, CollectionSchema
from sentence_transformers import SentenceTransformer

from src import pyenv
from src.db import BaseConnector
from src.models import Document


class _MilvusConnector(BaseConnector):
    def __init__(self):
        self.client = MilvusClient(uri=pyenv.settings.milvus_url)
        self.model = SentenceTransformer(pyenv.settings.milvus_model)
        self.collection_name = pyenv.settings.index_name
        self.__db_init()

    def __db_init(self):
        fields = [
            FieldSchema(name="id", dtype=DataType.VARCHAR,
                        is_primary=True, max_length=36),
            FieldSchema(name="vector",
                        dtype=DataType.FLOAT_VECTOR, dim=768),
        ]

        schema = CollectionSchema(fields=fields, enable_dynamic_field=True)

        if not self.client.has_collection(collection_name=self.collection_name):
            self.client.create_collection(
                collection_name=self.collection_name, schema=schema)

        self.client.load_collection(self.collection_name)

        index_params = self.client.prepare_index_params()
        index_params.add_index(
            field_name="vector",
            metric_type=pyenv.settings.milvus_metric_type,
            index_type=pyenv.settings.milvus_index_type,
            index_name="vector_index",
        )

        indexes = self.client.list_indexes(
            collection_name=self.collection_name
        )
        if 'vector_index' in indexes:
            details = self.client.describe_index(
                collection_name=self.collection_name,
                index_name="vector_index"
            )

            if (details['metric_type'] != pyenv.settings.milvus_metric_type or
                    details['index_type'] != pyenv.settings.milvus_index_type):
                self.client.drop_index(
                    collection_name=self.collection_name,
                    index_name='vector_index'
                )
        self.client.create_index(self.collection_name, index_params)

    def add_documents(self, documents: list[Document]) -> list[Document]:
        embeddings = self.model.encode([doc.data for doc in documents])

        documents_to_insert = [
            {"id": str(doc.id), "vector": emb,
             "url": doc.url, "data": doc.data}
            for doc, emb in zip(documents, embeddings)
        ]

        res = self.client.insert(collection_name=self.collection_name,
                                 data=documents_to_insert)

        documents_to_return = []
        for id in res['ids']:
            og_doc = next(
                (d for d in documents if str(d.id) == id), None)
            if og_doc:
                documents_to_return.append(og_doc)
        return documents_to_return

    def search(self, query: str, limit: int) -> list[Document]:
        query_embedding = self.model.encode([query])

        res = self.client.search(
            collection_name=self.collection_name,
            data=query_embedding,
            limit=limit,
            output_fields=["url", "data"]
        )

        return [
            Document(
                id=doc['id'],
                data=doc['entity']['data'],
                url=doc['entity']['url'],
                score=1-doc['distance']
            )
            for doc in res[0]
        ]


milvus_connector = _MilvusConnector()
