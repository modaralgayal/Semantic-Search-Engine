from time import perf_counter

import torch
from sentence_transformers import util


def create_embeddings(document_phrases, model):
    embeddings = model.encode(document_phrases, convert_to_tensor=True)
    return embeddings


def embed_user_query(embeddings, user_query, model):
    time_measurements = []
    total_time = 0

    start = perf_counter()
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    end = perf_counter()
    time = end - start
    total_time += time
    time_measurements.append(f"Query Encoding: {time}")

    start = perf_counter()

    scores = util.cos_sim(query_embedding, embeddings)
    end = perf_counter()
    time = end - start
    total_time += time
    time_measurements.append(f"Similarity: {time}")

    start = perf_counter()

    ranked_indices = torch.argsort(scores[0], descending=True)[:10]
    end = perf_counter()
    time = end - start
    total_time += time
    time_measurements.append(f"Sorting: {time}")
    time_measurements.append(f"Total time: {total_time}")

    return scores, ranked_indices, time_measurements
