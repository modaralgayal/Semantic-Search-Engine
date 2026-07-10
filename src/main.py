from time import perf_counter

import matplotlib.pyplot as plt
from sentence_transformers import SentenceTransformer

import embeddings
from get_products import get_posts


class SemanticSearch:
    def __init__(self):
        self.products = []
        self.top_scores = []
        self.ranked_indices = []
        self.best_result = ""
        self.best_res_score = 0
        self.best_res_idx = 0
        self.time_measurements = []
        
        self.build_model()
        self.products = get_posts()
        self.embeddings = embeddings.create_embeddings(self.products, self.model)

    def build_model(self):
        start = perf_counter()
        print("Loading model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Model Loaded!")
        end = perf_counter()
        time = end - start
        print(f"Load model: {time}")
        return True

    def take_input(self):
        user_query = str(input("Enter your query here (c to exit): "))

        if user_query.strip().lower() == "c":
            return False

        if len(user_query) == 0 or len(user_query) > 30:
            raise ValueError("Invalid input: Either empty or too large.")

        self.user_query = user_query
        return True

    def encode_query(self, user_query):
        self.top_scores, self.ranked_indices, performance_report = (
            embeddings.embed_user_query(self.embeddings, user_query, self.model)
        )

        self.time_measurements = self.time_measurements + performance_report

    def print_search_results(self):

        print("\n" + "=" * 80)
        print("TOP SEARCH RESULTS")
        print("=" * 80)

        for rank, idx in enumerate(self.ranked_indices, start=1):
            if rank == 1:
                self.best_res_score = self.top_scores[0][idx]
                self.best_result = self.products[idx]
                self.best_res_idx = idx
            print(
                f"{rank:2}. {self.products[idx]:<55}"
                f" Score: {self.top_scores[0][idx]:.3f}"
            )

        print("=" * 80)

    def visualize(self):
        values = self.top_scores.tolist()[0]
        fix, ax = plt.subplots()
        ax.scatter(range(len(values)), values)
        ax.set_ylim(-0.05, 1)
        ax.annotate(
            self.best_result,
            xy=(self.best_res_idx, self.best_res_score),
            xycoords="data",
            xytext=(self.best_res_idx + 5, self.best_res_score - 0.15),
            textcoords="data",
            va="top",
            ha="left",
            arrowprops=dict(facecolor="black", shrink=0.05),
        )
        plt.show()

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
