from sentence_transformers import SentenceTransformer
from ..config import settings
import numpy as np

class EmbeddingService:
    def __init__(self):
        self.model = SentenceTransformer(settings.embedding_model)

    def encode(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def encode_single(self, text: str) -> list[float]:
        return self.encode([text])[0]

embedding_service = EmbeddingService()