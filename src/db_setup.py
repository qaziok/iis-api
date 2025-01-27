from datasets import load_dataset, concatenate_datasets
from tqdm import tqdm

from src import pyenv
from src.db import connector
from src.services import splitter

from random import sample


if __name__ == "__main__":
    ds = load_dataset("wikimedia/wikipedia", "20231101.pl", split='train')
    dsout = ds

    # filter the dataset to contain only articles with a maximum number of characters
    if pyenv.settings.max_chars:
        dsout = ds.filter(lambda record: len(record['text']) <= int(pyenv.settings.max_chars))

    # shuffle the dataset and select the first n records
    if pyenv.settings.max_records:
        dsout = dsout.shuffle(seed=42).select(range(int(pyenv.settings.max_records)))

    # ensure that the dataset contains the articles from the tests
    if pyenv.settings.include_tests == 'true':
        articles = list(set([article for test in pyenv.tests for article in test['articles']]))
        dsa = ds.filter(lambda record: record['url'] in articles)
        dsout = concatenate_datasets([dsa, dsout])

    print(f'\n---Dataset will contain {dsout.num_rows} articles---\n')

    for record in tqdm(dsout):
        docs = splitter.to_documents(record['text'], url=record['url'])
        if (len(docs) > 0):
            connector.add_documents(docs)
