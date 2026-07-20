import json
import os
from pathlib import Path

import faiss
import numpy as np

from . import components


class SemanticSearch:
    def __init__(self):
        self.products = []
        self.top_scores = []
        self.ranked_indices = []
        self.best_result = ""
        self.best_res_score = 0
        self.best_res_idx = 0
        self.time_measurements = []

        if not self.build_model():
            raise RuntimeError("Failed to build model")

        self._load_precomputed_data()

    def _load_precomputed_data(self):
        """Load pre-computed data instead of computing at startup."""
        data_dir = Path(__file__).resolve().parent / "data"

        # Load products
        print("Loading products...", flush=True)
        with open(data_dir / "products.json") as f:
            self.products = json.load(f)
        print(f"Loaded {len(self.products)} products", flush=True)

        # Load embeddings
        print("Loading embeddings...", flush=True)
        self.embeddings = np.load(data_dir / "embeddings.npy")
        print(f"Embeddings loaded: {self.embeddings.shape}", flush=True)

        # Build custom flat index from loaded embeddings (fast, ~0.01s)
        print("Building flat index...", flush=True)
        self.index = components.embeddings.build_flat_index(self.embeddings)
        print("Flat index built", flush=True)

        # Load FAISS indexes from pre-computed files
        print("Loading FAISS indexes...", flush=True)
        self.faissIndexL2 = faiss.read_index(str(data_dir / "faiss_l2.index"))
        self.faissIndexIVFF = faiss.read_index(str(data_dir / "faiss_ivff.index"))
        self.faissIndexIVFPQ = faiss.read_index(str(data_dir / "faiss_ivfpq.index"))
        print("FAISS indexes loaded", flush=True)

    def build_model(self):
        self.model = components.build_model.build_model()
        return self.model is not None

    def take_input(self):
        try:
            self.user_query = components.inp.take_input()
        except ValueError as e:
            print(e)
            return True
        return self.user_query is not None

    def encode_query(self, user_query):
        (
            self.top_scores,
            self.ranked_indices,
            self.top_scoresivff,
            self.ranked_indicesivff,
            performance_report,
        ) = components.embeddings.embed_user_query(
            self.index,
            self.embeddings,
            user_query,
            self.faissIndexL2,
            self.faissIndexIVFF,
            self.faissIndexIVFPQ,
            self.model,
        )

        self.time_measurements = self.time_measurements + performance_report

    def print_search_results(self):
        components.print_res.print_search_results(
            self.ranked_indices, self.top_scores, self.products
        )

        components.print_res.print_search_results(
            self.ranked_indicesivff, self.top_scoresivff, self.products
        )

        return True

    def visualize(self):
        components.visualize(
            self.top_scores, self.best_result, self.best_res_idx, self.best_res_score
        )
        return True

    def print_timing_results(self):
        print("\n")
        for stat in self.time_measurements:
            print(stat)
        print("\n")

    def run(self):
        self.time_measurements = []
        if not self.take_input():
            return False
        self.encode_query(self.user_query)
        self.print_search_results()
        self.print_timing_results()
        # self.visualize()
        return True


if __name__ == "__main__":
    search_engine = SemanticSearch()
    while True:
        if not search_engine.run():
            print("Goodbye!")
            break