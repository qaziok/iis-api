import sys

from datasets import load_dataset

from src.services import splitter


def print_record(record):
    print()
    print('*\n*\n*\n*\n*')
    print(f'ID: {record['id']}, URL: {record['url']}, TITLE: {record['title']}')
    print('*\n*\n*\n*\n*')
    print()


def print_segments(record):
    segments = splitter.to_documents(record['text'], url=record['url'])
    for segment in segments:
        print(f'---{segment.id}---')
        print(segment.data)
        print('------------------------------------------')
        print()


if __name__ == "__main__":
    ds = load_dataset("wikimedia/wikipedia", "20231101.pl", split='train')

    records = ds.filter(lambda record: sys.argv[1] in record['title'])

    for record in records:
        print_record(record)
        print_segments(record)
