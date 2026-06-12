import numpy as np
from sentence_transformers import SentenceTransformer, util
import torch

import similarity_functions

print("Loading model...")
MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("Model Loaded")


def convert_document_to_matrix():
    document_phrases = []
    with open(f"products/products.txt") as f:
        for x in f:
            document_phrases.append(str(x.strip("\n")))

    return document_phrases


def search():
    user_query = str(input("Enter your search query here: "))

    if len(user_query) == 0 or len(user_query) > 40:
        raise ValueError("Input is invalid.")

    document_phrases = convert_document_to_matrix()
    embeddings = MODEL.encode(document_phrases, convert_to_tensor=True)
    query_embedding = MODEL.encode(user_query, convert_to_tensor=True)


    scores = util.cos_sim(query_embedding, embeddings)
    ranked_indices = torch.argsort(scores[0], descending=True)[:11]
    print("Most relevant results:")
    for i in range(len(ranked_indices)): 
        print(f"{document_phrases[ranked_indices[i]]}")

    return True


if __name__ == "__main__":
    search()
