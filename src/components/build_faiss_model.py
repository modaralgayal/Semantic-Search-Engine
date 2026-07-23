import math

import faiss


def faissInitL2(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    faissIndex = faiss.IndexFlatL2(dim)
    faissIndex.add(embeddings_np)
    return faissIndex

"""



"""


def faissInitIVFF(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    n = embeddings_np.shape[0]
    quantizer = faiss.IndexFlatL2(dim)

    # nlist should be sqrt(n), but at least 1 and at most n
    nlist = max(1, min(int(math.sqrt(n)), n))
    index = faiss.IndexIVFFlat(quantizer, dim, nlist)
    index.train(embeddings_np)
    index.add(embeddings_np)
    return index

"""



"""


def faissInitIVFPQ(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    n = embeddings_np.shape[0]
    quantizer = faiss.IndexFlatL2(dim)

    # nlist: sqrt(n), at least 1
    nlist = max(1, min(int(math.sqrt(n)), n))

    # PQ params: we need m * 2^bits <= n for training.
    # With 384-dim vectors, good m values are 8, 12, 16, 24.
    # bits=4 gives 16 centroids per sub-vector (need 16 training points per sub-codebook)
    m = 8
    bits = 4
    while n < (1 << bits) and bits > 2:
        bits -= 1

    index = faiss.IndexIVFPQ(quantizer, dim, nlist, m, bits)
    index.train(embeddings_np)
    index.add(embeddings_np)
    return index

"""



"""


