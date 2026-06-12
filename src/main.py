from sentence_transformers import SentenceTransformer

import embeddings


class SemanticSearch:
    def __init__(self):
        self.products = []
        self.top_scores = []
        self.ranked_indices = []

        with open("products/products.txt") as f:
            for p in f:
                self.products.append(str(p.strip("\n")))

        self.build_model()

    def build_model(self):
        print("Loading model...")
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        print("Model Loaded!")
        return True

    def take_input(self):
        user_query = str(input("Enter your query here (c to exit): "))

        if user_query.strip().lower() == "c":
            return False

        if len(user_query) == 0 or len(user_query) > 30:
            raise ValueError("Invalid input: Either empty or too large.")

        self.user_query = user_query
        return True

    def create_embeddings(self, document_phrases, user_query):
        self.top_scores, self.ranked_indices = embeddings.create_embeddings(
            document_phrases, user_query, self.model
        )

    def print_search_results(self):

        print("\n" + "=" * 80)
        print("TOP SEARCH RESULTS")
        print("=" * 80)

        for rank, idx in enumerate(self.ranked_indices, start=1):
            print(
                f"{rank:2}. {self.products[idx]:<55}"
                f" Score: {self.top_scores[0][idx]:.3f}"
            )

        print("=" * 80)

    def run(self):
        if not self.take_input():
            return False
        self.create_embeddings(self.products, self.user_query)
        self.print_search_results()
        return True


if __name__ == "__main__":
    search_engine = SemanticSearch()
    while True:
        if not search_engine.run():
            print("Goodbye!")
            break
