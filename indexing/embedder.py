from sentence_transformers import SentenceTransformer
from typing import List
from config.settings import settings
from loguru import logger

class Embedder:
    def __init__(self):
        logger.info(f"Loading embedding model: {settings.EMBEDDING_MODEL}")
        self.model = SentenceTransformer(settings.EMBEDDING_MODEL)

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(texts, show_progress_bar=True, convert_to_numpy=True).tolist()

    def embed_single(self, text: str) -> List[float]:
        return self.model.encode([text], convert_to_numpy=True)[0].tolist()