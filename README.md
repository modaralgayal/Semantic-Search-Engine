# Semantic-Search-Engine

## General Information

- This is a Semantic Search Engine that uses cosine similarity to find the suitable
  search result for the user input.

# Benchmark: `util.cos_sim` (Python) vs. Custom C++ (Pybind11 + `FlatIndex`)

## Run 1 — Initial Comparison (Index Rebuilt Every Query)

### Query

> **"backpack"**

### Timing Breakdown

| Stage                            |   Time (ms) |
| -------------------------------- | ----------: |
| Query Encoding                   |      11.182 |
| Similarity (util python library) |       6.061 |
| Similarity (Pybind11 + C++)      |     141.909 |
| **Total**                        | **159.152** |

The C++ path was **~23x slower** here. Root cause: the C++ `cos_sim` function rebuilt the entire `FlatIndex` from scratch — copying every embedding into the index — on _every single query_. This wasn't a fair comparison, since `util.cos_sim` only ever operates on an already-existing tensor; it was never asked to redo the equivalent of "load the whole corpus" on each call.

### Fix Applied

Restructured the C++ binding so `FlatIndex` is built **once**, immediately after the corpus embeddings are computed, and each query only calls `index.search(...)` — mirroring exactly what `util.cos_sim` was already doing (operating on a pre-existing, already-embedded corpus).

---

## Run 2 — After Fix: Index Built Once, Only Search Is Timed

### Query

> **"Red charger model 3830"**

### Top Search Results

| Rank | Product                | Score |
| ---: | ---------------------- | ----: |
|    1 | Red Charger model 3830 | 1.000 |
|    2 | Red Charger model 3747 | 0.932 |
|    3 | Red Charger model 3686 | 0.925 |
|    4 | Red Charger model 3714 | 0.921 |
|    5 | Red Charger model 3207 | 0.916 |
|    6 | Red Charger model 3629 | 0.915 |
|    7 | Red Charger model 5839 | 0.915 |
|    8 | Red Charger model 30   | 0.915 |
|    9 | Red Charger model 3668 | 0.914 |
|   10 | Red Charger model 377  | 0.908 |

### Timing Breakdown

| Stage                            |  Time (ms) |
| -------------------------------- | ---------: |
| Query Encoding                   |     20.369 |
| Similarity (util python library) |      3.993 |
| Similarity (Pybind11 + C++)      |      6.101 |
| **Total**                        | **30.464** |

## Conclusion

Once the index-construction cost was removed from the per-query timing, the picture changes substantially:

- These results are taken in sample size of 10k. The top result is a perfect match (score 1.000), confirming the underlying cosine similarity math is correct on both implementations.
- `util.cos_sim` is faster (3.993ms vs. 6.101ms) — roughly 1.5x — but the two implementations are in the same performance ballpark for this corpus size and query.
- The remaining gap is a reasonable target for further investigation — likely attributable to util.cos_sim dispatching to a BLAS-backed, SIMD-vectorized, possibly multi-threaded batched matrix multiply, versus the custom C++ implementation's simpler per-row loop.
