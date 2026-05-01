from typing import Dict
from loguru import logger
from retrieval.query_classifier import QueryClassifier
from indexing.hybrid_retriever import HybridRetriever
from graph.dependency_graph import DependencyGraph


class RetrievalOrchestrator:
    def __init__(self, retriever: HybridRetriever, dep_graph: DependencyGraph):
        self.retriever  = retriever
        self.dep_graph  = dep_graph
        self.classifier = QueryClassifier()

    def run(self, query: str, top_k: int = 8) -> Dict:
        logger.info(f"Query: '{query}' | top_k={top_k}")

        # Step 1 — classify query intent
        query_type = self.classifier.classify(query)
        logger.info(f"Query type: {query_type}")

        # Step 2 — hybrid retrieval with name boosting (inside HybridRetriever)
        base_chunks = self.retriever.retrieve(query, top_k)
        logger.info(f"Retrieved {len(base_chunks)} chunks")

        # Step 3 — graph expansion only for FLOW and IMPACT
        graph_nodes = self._expand_graph(base_chunks, query_type)

        # Step 4 — targeted usages (only matching query symbol)
        usages = self.dep_graph.get_usages(query, max_results=10)

        return {
            "query_type":  query_type,
            "base_chunks": base_chunks,
            "graph_nodes": graph_nodes,
            "usages":      usages,
        }

    def _expand_graph(self, base_chunks: list, query_type: str) -> Dict:
        """Expand graph only for FLOW and IMPACT queries."""
        graph_nodes = {}

        if query_type not in ("FLOW", "IMPACT"):
            return graph_nodes

        for chunk in base_chunks[:3]:
            node_id = f"{chunk.get('file_path')}::{chunk.get('name')}"
            neighbours = self.dep_graph.get_neighbours(node_id, depth=1)
            graph_nodes.update(neighbours)

        logger.info(f"Graph expanded: {len(graph_nodes)} nodes")
        return graph_nodes