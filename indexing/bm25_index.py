import pickle
import os
from rank_bm25 import BM25Okapi
from typing import List, Dict
from loguru import logger
from config.settings import settings

class BM25Index:
    def __init__(self):
        self.bm25 = None
        self.chunks: List[Dict] = []

    def build(self, chunks: List[Dict]):
        self.chunks = chunks
        tokenized = [c["content"].lower().split() for c in chunks]
        self.bm25 = BM25Okapi(tokenized)
        logger.info(f"BM25 index built with {len(chunks)} documents")

    def search(self, query: str, top_k: int = 8) -> List[Dict]:
        if not self.bm25:
            return []
        tokenized_query = query.lower().split()
        scores = self.bm25.get_scores(tokenized_query)
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
        return [self.chunks[i] for i in top_indices if scores[i] > 0]

    def save(self):
        os.makedirs(os.path.dirname(settings.BM25_INDEX_PATH), exist_ok=True)
        with open(settings.BM25_INDEX_PATH, "wb") as f:
            pickle.dump({"bm25": self.bm25, "chunks": self.chunks}, f)
        logger.info("BM25 index saved.")

    def load(self):
        with open(settings.BM25_INDEX_PATH, "rb") as f:
            data = pickle.load(f)
        self.bm25 = data["bm25"]
        self.chunks = data["chunks"]
        logger.info(f"BM25 index loaded: {len(self.chunks)} docs")