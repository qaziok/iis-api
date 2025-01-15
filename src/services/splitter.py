from itertools import islice
from transformers import AutoTokenizer
from semantic_text_splitter import TextSplitter
from os.path import exists, join
from uuid import UUID
import hashlib
import string


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
    
    @staticmethod
    def preprocess(text):
        headers = ['\nPrzypisy\n', '\nBibliografia\n', '\nLinki zewnętrzne\n', '\nZobacz też\n']
        for header in headers:
            ridx = text.rfind(header)
            if ridx > 0:
                text = text[:text.rfind(header)]
        return text
    
    @staticmethod
    def invalid(chunk):
        length = len(chunk.split()) <= 8 # if chunk is too short
        punctuation = not any(char in string.punctuation for char in chunk) # if chunk contains no punctuation
        return all([length, punctuation])

    def to_documents(self, text, **kwargs):
        text = self.preprocess(text)
        chunks = self.text_splitter.chunks(text)
        parsed = []

        # merge invalid chunks
        for prev, chunk, _ in self.window([None, *chunks, None], 3):
            if not self.invalid(chunk):
                if prev is not None and self.invalid(prev):
                    parsed.append(prev + "\n" + chunk)
                else:
                    parsed.append(chunk)

        docs = [
            Document(
                id=self.create_uuid(kwargs.get('url'), i, chunk),
                data=chunk,
                url=kwargs.get('url'),
            ) for i, chunk in enumerate(parsed)
        ]

        # for prev, doc, next in self.window([None, *docs, None], 3):
        #     doc.prev_id = prev.id if prev else None
        #     doc.next_id = next.id if next else None

        return docs


splitter = _Splitter()
