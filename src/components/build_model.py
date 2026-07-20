from time import perf_counter
from sentence_transformers import SentenceTransformer


def build_model():
    start = perf_counter()
    print("Loading model...")
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    print("Model Loaded!")
    end = perf_counter()
    time = end - start
    print(f"Load model: {time}")
    return model