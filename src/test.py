from src import pyenv
from src.db import connector

from sklearn.metrics import ndcg_score

from statistics import fmean
from pprint import pprint


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


#NDCG
def apply_relevance(mask, predictions):
    relevant = [mask.get(pred) for pred in predictions]
    return [0 if rel is None else rel for rel in relevant]


def NDCG(truth, predictions):
    relevance = [3, 2, 2, 1, 1]
    relevant_masks = [{t: relevance[i] for (i, t) in enumerate(t_vec)} for t_vec in truth]

    y_true = [relevance for _ in truth]
    y_pred = [apply_relevance(pair[0], pair[1]) for pair in list(zip(relevant_masks, predictions))]

    return float(ndcg_score(y_true, y_pred))


if __name__ == "__main__":
    tests = pyenv.tests

    queries = [test['query'] for test in tests]

    t_segments = [test['segments'] for test in tests]
    t_articles = [test['articles'] for test in tests]

    p_segments, p_articles = list(zip(*list(map(lambda query: query_predictions(query), queries))))

    results = {
        'MRR_segments': MRR(t_segments, p_segments),
        'MRR_articles': MRR(t_articles, p_articles),
        'NDCG_segments': NDCG(t_segments, p_segments),
        'NDCG_articles': NDCG(t_articles, p_articles)
    }
    pprint(results)
