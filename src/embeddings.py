import torch
from sentence_transformers import util


def create_embeddings(document_phrases, user_query, model):
    embeddings = model.encode(document_phrases, convert_to_tensor=True)
    query_embedding = model.encode(user_query, convert_to_tensor=True)

    scores = util.cos_sim(query_embedding, embeddings)
    ranked_indices = torch.argsort(scores[0], descending=True)[:10]

    return scores, ranked_indices
