import numpy as np
from config.settings import TOP_K

class RetrievalService:
    def __init__(self, embedding_service):
        self.embedding_service = embedding_service

    def search(self, query, chunks, embeddings, top_k=TOP_K):
        if not chunks or embeddings is None:
            return []

        query_embedding = self.embedding_service.create_query_embedding(query)
        scores = np.dot(embeddings, query_embedding)

        k = min(top_k, len(chunks))
        indices = np.argsort(scores)[::-1][:k]

        return [
            {"score": float(scores[i]), "chunk": chunks[i]}
            for i in indices
        ]
