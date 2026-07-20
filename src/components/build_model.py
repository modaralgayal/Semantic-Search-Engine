from time import perf_counter
from fastembed import TextEmbedding


def build_model():
    start = perf_counter()
    print("Loading model...")
    model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Model Loaded!")
    end = perf_counter()
    time = end - start
    print(f"Load model: {time}")
    return model