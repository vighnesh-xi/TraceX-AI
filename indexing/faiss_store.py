import faiss
import numpy as np
import json
import os
from typing import List, Dict, Tuple
from loguru import logger
from config.settings import settings

class FAISSStore:
    def __init__(self, dim: int = 384):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)
        self.metadata: List[Dict] = []

    def add(self, embeddings: List[List[float]], chunks: List[Dict]):
        vectors = np.array(embeddings, dtype="float32")
        self.index.add(vectors)
        self.metadata.extend(chunks)
        logger.info(f"FAISS index now has {self.index.ntotal} vectors")

    def search(self, query_embedding: List[float], top_k: int = 8) -> List[Tuple[Dict, float]]:
        vec = np.array([query_embedding], dtype="float32")
        distances, indices = self.index.search(vec, top_k)
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx < len(self.metadata):
                results.append((self.metadata[idx], float(dist)))
        return results

    def save(self):
        os.makedirs(os.path.dirname(settings.FAISS_INDEX_PATH), exist_ok=True)
        faiss.write_index(self.index, settings.FAISS_INDEX_PATH + ".bin")
        with open(settings.FAISS_INDEX_PATH + "_meta.json", "w") as f:
            json.dump(self.metadata, f, indent=2)
        logger.info("FAISS index saved.")

    def load(self):
        self.index = faiss.read_index(settings.FAISS_INDEX_PATH + ".bin")
        with open(settings.FAISS_INDEX_PATH + "_meta.json") as f:
            self.metadata = json.load(f)
        logger.info(f"FAISS index loaded: {self.index.ntotal} vectors")