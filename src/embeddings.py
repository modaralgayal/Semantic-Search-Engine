from time import perf_counter

import torch
from sentence_transformers import util


def create_embeddings(document_phrases, user_query, model):
    time_measurements = []

    start = perf_counter()
    embeddings = model.encode(document_phrases, convert_to_tensor=True)
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    end = perf_counter()
    time = end - start
    time_measurements.append(f"Query Encoding: {time}")

    start = perf_counter()

    scores = util.cos_sim(query_embedding, embeddings)
    end = perf_counter()
    time = end - start
    time_measurements.append(f"Similarity: {time}")

    start = perf_counter()

    ranked_indices = torch.argsort(scores[0], descending=True)[:10]
    end = perf_counter()
    time = end - start
    time_measurements.append(f"Sorting: {time}")

    return scores, ranked_indices, time_measurements
