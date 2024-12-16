from datasets import load_dataset
from tqdm import tqdm

from src import pyenv
from src.db import connector
from src.services import splitter


if __name__ == "__main__":
    print(pyenv.settings)

    ds = load_dataset("wikimedia/wikipedia", "20231101.pl", split='train')

    if pyenv.settings.max_chars:
        ds = ds.filter(lambda record: len(
            record['text']) <= int(pyenv.settings.max_chars))

    for record in tqdm(ds):
        docs = splitter.to_documents(record['text'], url=record['url'])
        connector.add_documents(docs)
