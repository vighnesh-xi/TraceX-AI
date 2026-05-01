import networkx as nx
from typing import Dict, List
from loguru import logger

NOISE_SYMBOLS = {
    "login", "test", "generate_api_logs", "__file__",
    "__init__", "handle", "map", "earlyReturn",
    "up", "down", "boot", "register",
}


class DependencyGraph:
    def __init__(self):
        self.graph = nx.DiGraph()

    def build(self, chunks: List[Dict]):
        """Build dependency graph from parsed chunks."""
        self.graph.clear()

        for chunk in chunks:
            node_id = f"{chunk.get('file_path')}::{chunk.get('name')}"
            self.graph.add_node(node_id, **{
                "file_path": chunk.get("file_path", ""),
                "name":      chunk.get("name", ""),
                "type":      chunk.get("type", ""),
                "tags":      chunk.get("tags", []),
                "file_type": chunk.get("file_type", ""),
            })

        # Add edges based on same-file proximity (sibling methods)
        file_chunks: Dict[str, List] = {}
        for chunk in chunks:
            fp = chunk.get("file_path", "")
            file_chunks.setdefault(fp, []).append(chunk)

        for fp, fc in file_chunks.items():
            for i in range(len(fc) - 1):
                src = f"{fp}::{fc[i].get('name')}"
                dst = f"{fp}::{fc[i+1].get('name')}"
                if src in self.graph and dst in self.graph:
                    self.graph.add_edge(src, dst, relation="sibling")

        logger.info(
            f"Dependency graph built: "
            f"{self.graph.number_of_nodes()} nodes, "
            f"{self.graph.number_of_edges()} edges"
        )

    def get_neighbours(self, node_id: str, depth: int = 1) -> Dict:
        """Return neighbouring nodes, filtering out noise symbols."""
        neighbours = {}
        if node_id not in self.graph:
            return neighbours

        try:
            ego = nx.ego_graph(self.graph, node_id, radius=depth)
            for neighbour in ego.nodes:
                name = neighbour.split("::")[-1]
                # Skip noise
                if name in NOISE_SYMBOLS:
                    continue
                if any(name.startswith(n) for n in ("class_",)):
                    continue
                neighbours[neighbour] = dict(self.graph.nodes[neighbour])
        except Exception as e:
            logger.warning(f"Graph neighbour error for {node_id}: {e}")

        return neighbours

    def get_usages(self, query: str, max_results: int = 10) -> List[str]:
        """
        Return only graph nodes whose symbol name closely matches
        the queried symbol. Avoids returning the full graph neighbourhood.
        """
        # Clean the query to extract the likely symbol name
        query_clean = (
            query.lower()
            .replace("where is", "")
            .replace("where does", "")
            .replace("how does", "")
            .replace("explain", "")
            .replace("find", "")
            .replace("api", "")
            .replace("function", "")
            .replace("method", "")
            .replace("work", "")
            .replace("?", "")
            .replace("_", "")
            .replace(" ", "")
            .strip()
        )

        matched = []
        for node_id in self.graph.nodes:
            name = node_id.split("::")[-1].lower().replace("_", "")

            # Skip noise symbols entirely
            if name in NOISE_SYMBOLS:
                continue
            if any(name.startswith(n) for n in ("class_",)):
                continue

            # Match if symbol and query overlap meaningfully
            if len(query_clean) >= 4 and (
                query_clean in name or name in query_clean
            ):
                matched.append(node_id)

        return matched[:max_results]

    def get_node(self, node_id: str) -> Dict:
        """Return attributes of a single node."""
        if node_id in self.graph:
            return dict(self.graph.nodes[node_id])
        return {}

    def all_nodes(self) -> Dict:
        """Return all nodes as a dict."""
        return dict(self.graph.nodes(data=True))