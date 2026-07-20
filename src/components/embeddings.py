from contextlib import contextmanager
from time import perf_counter

import cos_sim
import numpy as np


def create_embeddings(document_phrases, model):
    print(f"  Encoding {len(document_phrases)} documents...")
    embeddings = list(model.embed(document_phrases, batch_size=256))
    print("  Encoding complete, converting to array...")
    return np.array(embeddings, dtype=np.float32)


def build_flat_index(embeddings):
    lib = embeddings.shape[0]
    dim = embeddings.shape[1]

    index = cos_sim.FlatIndex(dim, lib)
    for i, emb in enumerate(embeddings):
        index.add(emb.tolist(), i)

    return index


def embed_user_query(
    index, embeddings, user_query, faissIndexL2, faissIndexIVFF, faissIndexIVFPQ, model
):
    time_measurements = []
    total_time = [0.0]

    with timer("Query Encoding", time_measurements, total_time):
        query_embedding = list(model.query_embed(user_query))[0]

    with timer("Similarity (Python numpy)", time_measurements, total_time):
        query_norm = query_embedding / np.linalg.norm(query_embedding)
        embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        new_test_scores = np.dot(embeddings_norm, query_norm)
        py_ranked_indices = np.argsort(new_test_scores)[::-1][:10]

    with timer("Similarity (Pybind11 + C++)", time_measurements, total_time):
        c_query = query_embedding.tolist()
        results = index.search(c_query, 10)
        cpp_ranked_indices = results.ids
        cpp_scores = results.scores

    f_query = query_embedding.astype("float32").reshape(1, -1)
    with timer("FAISS FlatIndexL2", time_measurements, total_time):
        D, I = faissIndexL2.search(f_query, k=10)

    with timer("FAISS IVFF", time_measurements, total_time):
        DIVFF, IIVFF = faissIndexIVFF.search(f_query, k=10)

    with timer("FAISS IVFPQ", time_measurements, total_time):
        D, I = faissIndexIVFPQ.search(f_query, k=10)

    time_measurements.append(f"Total time: {total_time[0] * 1000:.3f}ms")

    return (
        D[0],
        I[0],
        DIVFF[0],
        IIVFF[0],
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