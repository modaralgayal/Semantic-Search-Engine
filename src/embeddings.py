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
    total_time = 0

    start = perf_counter()
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    end = perf_counter()
    time = end - start
    total_time += time
    time_measurements.append(f"Query Encoding: {time}")

    start = perf_counter()

    scores = cosine_similarity.cosine_similarity(query_embedding, embeddings)
    scores = torch.tensor(scores)
    print("Cosine similarity found: ", scores)
    # scores = util.cos_sim(query_embedding, embeddings)
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


def run():
    vec = np.array([0.43535, 0.23256, 0.23252])
    result = cosine_similarity.cosine_similarity(vec, vec)
    result = torch.tensor(result)
    ranked_indices = torch.argsort(result[0], descending=True)[:10]

    print(ranked_indices)
    return result


if __name__ == "__main__":
    run()
