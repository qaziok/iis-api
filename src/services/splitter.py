from itertools import islice
from transformers import AutoTokenizer
from semantic_text_splitter import TextSplitter
from os.path import exists, join
from uuid import UUID
import hashlib


from src import pyenv
from src.models import Document


class _Splitter:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained(
            pyenv.settings.tokenizer)

        path = join("/tmp", pyenv.settings.tokenizer.replace("/", "_"))
        if not exists(path):
            self.tokenizer.save_pretrained(path)

        self.text_splitter = TextSplitter.from_huggingface_tokenizer_file(
            join(path, "tokenizer.json",), int(pyenv.settings.chunk_size))

    @staticmethod
    def window(seq, n):
        it = iter(seq)
        result = tuple(islice(it, n))
        if len(result) == n:
            yield result
        for elem in it:
            result = result[1:] + (elem,)
            yield result

    @staticmethod
    def create_uuid(url, index, _text):
        hash_string = hashlib.md5(f"{url}/{index}".encode()).hexdigest()
        return UUID(hex=hash_string, version=4)

    def to_documents(self, text, **kwargs):
        chunks = self.text_splitter.chunks(text)

        docs = [
            Document(
                id=self.create_uuid(kwargs.get('url'), i, chunk),
                data=chunk,
                url=kwargs.get('url'),
            ) for i, chunk in enumerate(chunks)
        ]

        # for prev, doc, next in self.window([None, *docs, None], 3):
        #     doc.prev_id = prev.id if prev else None
        #     doc.next_id = next.id if next else None

        return docs


splitter = _Splitter()
