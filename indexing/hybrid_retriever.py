from typing import List, Dict
import numpy as np
from indexing.faiss_store import FAISSStore
from indexing.bm25_index import BM25Index
from indexing.embedder import Embedder
from loguru import logger


class HybridRetriever:
    def __init__(self, faiss_store: FAISSStore, bm25_index: BM25Index, embedder: Embedder):
        self.faiss    = faiss_store
        self.bm25     = bm25_index
        self.embedder = embedder

    def retrieve(self, query: str, top_k: int = 8) -> List[Dict]:
        #Semantic search
        try:
            raw = self.embedder.embed([query])        # List[List[float]]
            vec = np.array(raw[0], dtype=np.float32) # 1-D numpy array
            if vec.ndim > 1:
                vec = vec.flatten()
            semantic_results = self.faiss.search(vec, top_k * 2)
        except Exception as e:
            logger.warning(f"FAISS search failed: {e}")
            semantic_results = []

        #Keyword search
        try:
            bm25_results = self.bm25.search(query, top_k * 2)
        except Exception as e:
            logger.warning(f"BM25 search failed: {e}")
            bm25_results = []

        #Normalize results to List[Dict]
        semantic_results = self._normalize(semantic_results)
        bm25_results     = self._normalize(bm25_results)

        #Deduplicate by chunk_id
        seen: Dict[str, Dict] = {}
        for chunk in semantic_results + bm25_results:
            cid = chunk.get("chunk_id")
            if cid and cid not in seen:
                seen[cid] = chunk

        merged = list(seen.values())
        logger.info(f"Merged {len(merged)} unique chunks (semantic={len(semantic_results)}, bm25={len(bm25_results)})")

        #Boost: function name match in query
        query_clean = query.lower().replace("_", "").replace(" ", "")

        def rank(chunk: Dict) -> int:
            name = chunk.get("name", "").lower().replace("_", "")
            file = chunk.get("file_path", "").lower().replace("\\", "/")
            filename = file.split("/")[-1].replace(".php", "").replace(".py", "")

            if len(name) > 4 and name in query_clean:
                return 0   # exact function name hit
            if filename and filename in query_clean:
                return 1   # file name hit
            return 2

        merged.sort(key=rank)
        return merged[:top_k]

    def _normalize(self, results) -> List[Dict]:
        """
        Ensure every result is a dict.
        Handles: List[Dict], List[Tuple], or mixed.
        """
        normalized = []
        for item in results:
            if isinstance(item, dict):
                normalized.append(item)
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                # Common pattern: (chunk_dict, score) or (score, chunk_dict)
                for part in item:
                    if isinstance(part, dict):
                        normalized.append(part)
                        break
            else:
                logger.warning(f"Skipping unexpected result type: {type(item)} — {item}")
        return normalized