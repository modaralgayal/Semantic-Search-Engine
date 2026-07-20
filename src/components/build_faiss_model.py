import faiss

# The flat L2 index is slow even compared to normal cosine similarity
# since it's comparisons are "too accurate."


def faissInitL2(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    faissIndex = faiss.IndexFlatL2(dim)
    faissIndex.add(embeddings_np)
    return faissIndex


# We can sacrifice a little bit of accuracy for performance.
def faissInitIVFF(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    quantizer = faiss.IndexFlatL2(dim)

    # nlist represents how many culsters (voronoi cells)
    # my index puts vectors into.
    nlist = 50
    index = faiss.IndexIVFFlat(quantizer, dim, nlist)
    index.train(embeddings_np)
    index.add(embeddings_np)
    return index  # <-- Results shown are quite similar to the flatl2 index.
    # However ~5x faster than flat.


def faissInitIVFPQ(embeddings):
    embeddings_np = embeddings.astype("float32")
    dim = embeddings_np.shape[1]
    quantizer = faiss.IndexFlatL2(dim)

    nlist = 50
    m = 8
    bits = 8
    index = faiss.IndexIVFPQ(quantizer, dim, nlist, m, bits)
    index.train(embeddings_np)
    index.add(embeddings_np)
    return index  # <-- Results shown are quite as accurate to the flatl2 index.
    # However ~7x faster than flat.
