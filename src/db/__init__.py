from src import pyenv

match pyenv.settings.db:
    case "marqo":
        from .marqo_connector import marqo_connector as connector
    case "milvus":
        from .milvus_connector import milvus_connector as connector
    case "chroma":
        from .chroma_connector import chroma_connector as connector
    case "mock":
        from .mock_connector import mock_connector as connector
    case _:
        raise ValueError(f"Unsupported db: {pyenv.settings.db}")
