from src import pyenv
from src.db import connector

from statistics import fmean
from pprint import pprint
from math import log2

# make queries to the system
def query_predictions(query):
    results = connector.search(query, 5)
    chunks = [doc.to_search_response() for doc in results]
    return [str(chunk['id']) for chunk in chunks], [str(result['url']) for result in chunks]


# MRR
def RR(true, pred):
    try:
        return 1.0 / (pred.index(true[0]) + 1.0)
    except:
        return 0.0


def MRR(truth, predictions):
    rows = list(zip(truth, predictions))
    rr = list(map(lambda row: RR(row[0], row[1]), rows))
    return float(fmean(rr))


# NDCG
def apply_relevance(mask, predictions):
    relevant = [mask.get(pred) for pred in predictions]
    return [0 if rel is None else rel for rel in relevant][:len(mask)]


def DCG(relevances):
    return float(sum(list(map(lambda rel: rel[1] / log2(rel[0] + 2), enumerate(relevances)))))


def NDCG(truth, predictions, relevance=[3, 2, 2, 1, 1]):
    relevant_masks = [{t: relevance[i] for (i, t) in enumerate(t_vec)} for t_vec in truth]

    y_true = [relevance[:len(t)] for t in truth]
    y_pred = [apply_relevance(pair[0], pair[1]) for pair in list(zip(relevant_masks, predictions))]

    rows = list(zip(y_true, y_pred))

    return float(fmean([DCG(row[1]) / DCG(row[0]) for row in rows]))


# F1
def F1(truth, predictions):
    def row_f1(true, pred):
        h = len(set(true).intersection(set(pred)))
        p = h / len(pred) if len(pred) > 0 else 0
        r = h / len(true) if len(true) > 0 else 0
        return 2 * p * r / (p + r) if p + r > 0 else 0

    rows = list(zip(truth, predictions))
    hits = list(map(lambda row: row_f1(*row), rows))
    return float(fmean(hits))


if __name__ == "__main__":
    print(pyenv.settings)
    tests = pyenv.tests

    queries = [test['query'] for test in tests]

    t_segments = [test['segments'] for test in tests]
    t_articles = [test['articles'] for test in tests]

    p_segments, p_articles = list(zip(*list(map(lambda query: query_predictions(query), queries))))

    print('''
    MRR - mean reciprocal rank
    NDCG - normalized discounted gain (rel = [3, 2, 2, 1, 1])
    NDCG2 - binary normalized discounted gain (rel = [1, 1, 1, 1, 1])
    F1 - in this case its average hit rate
    ''')

    results = {
        'F1_articles': F1(t_articles, p_articles),
        'F1_segments': F1(t_segments, p_segments),
        'MRR_articles': MRR(t_articles, p_articles),
        'MRR_segments': MRR(t_segments, p_segments),
        'NDCG2_articles': NDCG(t_articles, p_articles, [1, 1, 1, 1, 1]),
        'NDCG2_segments': NDCG(t_segments, p_segments, [1, 1, 1, 1, 1]),
        'NDCG_articles': NDCG(t_articles, p_articles),
        'NDCG_segments': NDCG(t_segments, p_segments)
    }
    pprint(results)
