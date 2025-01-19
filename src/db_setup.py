from datasets import load_dataset, concatenate_datasets
from tqdm import tqdm

from src import pyenv
from src.db import connector
from src.services import splitter

from random import sample


if __name__ == "__main__":
    ds = load_dataset("wikimedia/wikipedia", "20231101.pl", split='train')

    if pyenv.settings.max_records:
        rnd = sample(range(ds.num_rows), int(pyenv.settings.max_records))
        dsout = ds.select(rnd)

    # load articles from tests
    if pyenv.settings.include_tests == 'true':
        articles = list(set([article for test in pyenv.tests for article in test['articles']]))
        dsa = ds.filter(lambda record: record['url'] in articles)
        dsout = concatenate_datasets([dsout, dsa])

    print(f'\n---Dataset will contain {dsout.num_rows} articles---\n')

    if pyenv.settings.max_chars:
        dsout = dsout.filter(lambda record: len(record['text']) <= int(pyenv.settings.max_chars))

    for record in tqdm(dsout):
        docs = splitter.to_documents(record['text'], url=record['url'])
        connector.add_documents(docs)
