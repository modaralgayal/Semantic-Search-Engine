from contextlib import contextmanager
from time import perf_counter

import cosine_similarity
import numpy as np
import torch
from sentence_transformers import util


def create_embeddings(document_phrases, model):
    embeddings = model.encode(document_phrases, convert_to_tensor=True)
    return embeddings


def embed_user_query(embeddings, user_query, model):
    time_measurements = []
    total_time = [0.0]

    with timer("Query Encoding", time_measurements, total_time):
        query_embedding = model.encode(user_query, convert_to_tensor=True)

    with timer("Similarity (util python library)", time_measurements, total_time):
        new_test_scores = util.cos_sim(query_embedding, embeddings)

    with timer("Sorting", time_measurements, total_time):
        ranked_indices = torch.argsort(new_test_scores[0], descending=True)[:10]

    time_measurements.append(f"Total time: {total_time[0]:.6f}s")
    return new_test_scores, ranked_indices, time_measurements


# the contextmanager makes sure some code (timer() function) run before a block of code.
@contextmanager
def timer(label, log_list, totals):
    start = perf_counter()
    yield  # <-- The "with" part of the code starts running here.
    elapsed = perf_counter() - start
    totals[0] += elapsed
    log_list.append(f"{label}: {elapsed:.6f}s")


def run():
    vec = np.array([0.43535, 0.23256, 0.23252])
    result = cosine_similarity.cosine_similarity(vec, vec)
    result = torch.tensor(result)
    ranked_indices = torch.argsort(result[0], descending=True)[:10]

    print(ranked_indices)
    return result


if __name__ == "__main__":
    run()
