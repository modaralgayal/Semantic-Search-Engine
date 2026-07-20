from contextlib import contextmanager
from time import perf_counter

import cos_sim
import numpy as np
import torch
from sentence_transformers import util


def create_embeddings(document_phrases, model):
    embeddings = model.encode(document_phrases, convert_to_tensor=True)
    return embeddings


def build_flat_index(embeddings):
    embeddings_np = embeddings.cpu().numpy()
    lib = embeddings_np.shape[0]
    dim = embeddings_np.shape[1]

    index = cos_sim.FlatIndex(dim, lib)
    for i, emb in enumerate(embeddings_np):
        index.add(emb.tolist(), i)

    return index


def embed_user_query(
    index, embeddings, user_query, faissIndexL2, faissIndexIVFF, faissIndexIVFPQ, model
):
    time_measurements = []
    total_time = [0.0]

    with timer("Query Encoding", time_measurements, total_time):
        query_embedding = model.encode(user_query, convert_to_tensor=True)

    with timer("Similarity (util python library)", time_measurements, total_time):
        new_test_scores = util.cos_sim(query_embedding, embeddings)
        py_ranked_indices = torch.argsort(new_test_scores[0], descending=True)[:10]

    with timer("Similarity (Pybind11 + C++)", time_measurements, total_time):
        c_query = query_embedding.cpu().numpy().tolist()
        results = index.search(c_query, 10)
        cpp_ranked_indices = results.ids
        cpp_scores = results.scores

    f_query = query_embedding.cpu().numpy().astype("float32").reshape(1, -1)
    with timer("FAISS FlatIndexL2", time_measurements, total_time):
        D, I = faissIndexL2.search(f_query, k=10)

    with timer("FAISS IVFF", time_measurements, total_time):
        DIVFF, IIVFF = faissIndexIVFF.search(f_query, k=10)

    with timer("FAISS IVFPQ", time_measurements, total_time):
        D, I = faissIndexIVFPQ.search(f_query, k=10)

    time_measurements.append(f"Total time: {total_time[0] * 1000:.3f}ms")

    return (
        torch.tensor(D[0]),
        torch.tensor(I[0]),
        torch.tensor(DIVFF[0]),
        torch.tensor(IIVFF[0]),
        time_measurements,
    )


# the contextmanager makes sure some code (timer() function) run before a block of code.
@contextmanager
def timer(label, log_list, totals):
    start = perf_counter()
    yield  # <-- The "with" part of the code starts running here.
    elapsed = perf_counter() - start
    totals[0] += elapsed
    log_list.append(f"{label}: {elapsed*1000:.3f}ms")
