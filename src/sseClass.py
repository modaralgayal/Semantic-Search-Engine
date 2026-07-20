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

        print("Generating product names...", flush=True)
        self.products = components.get_products.get_posts()
        print(f"Generated {len(self.products)} product names", flush=True)

        print("Creating embeddings (this may take a while)...", flush=True)
        self.embeddings = components.embeddings.create_embeddings(
            self.products, self.model
        )
        print(f"Embeddings created: {self.embeddings.shape}", flush=True)

        print("Building flat index...", flush=True)
        self.index = components.embeddings.build_flat_index(self.embeddings)
        print("Flat index built", flush=True)

        print("Initializing FAISS indexes...", flush=True)
        if not self.initiate_faiss():
            raise RuntimeError("Failed to initialize FAISS index")
        print("FAISS indexes ready", flush=True)

    def initiate_faiss(self):
        self.faissIndexL2 = components.build_faiss_model.faissInitL2(self.embeddings)
        self.faissIndexIVFF = components.build_faiss_model.faissInitIVFF(
            self.embeddings
        )
        self.faissIndexIVFPQ = components.build_faiss_model.faissInitIVFPQ(
            self.embeddings
        )

        return (
            self.faissIndexL2 is not None
            and self.faissIndexIVFF is not None
            and self.faissIndexIVFPQ is not None
        )

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