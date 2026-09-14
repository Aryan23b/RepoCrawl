import streamlit as st
from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

class EmbeddingService:
    def __init__(self):
        self.model = self._load_model()

    @staticmethod
    @st.cache_resource(show_spinner="Loading embedding model...")
    def _load_model():
        return SentenceTransformer(EMBEDDING_MODEL)

    def create_embeddings(self, chunks):
        texts = [f"File: {c.path}\n{c.content}" for c in chunks]
        return self.model.encode(
            texts,
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )

    def create_query_embedding(self, query):
        return self.model.encode(
            [query],
            convert_to_numpy=True,
            normalize_embeddings=True,
            show_progress_bar=False,
        )[0]
