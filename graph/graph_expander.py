from typing import List, Dict
import networkx as nx
from graph.dependency_graph import DependencyGraph

class GraphExpander:
    def __init__(self, dep_graph: DependencyGraph):
        self.graph = dep_graph.graph

    def expand(self, node_ids: List[str], depth: int = 2) -> Dict[str, Dict]:
        visited = {}
        for node_id in node_ids:
            if node_id not in self.graph:
                continue
            subgraph_nodes = nx.ego_graph(self.graph, node_id, radius=depth).nodes(data=True)
            for nid, attrs in subgraph_nodes:
                if nid not in visited:
                    visited[nid] = attrs
        return visited

    def find_entrypoints(self, keywords: List[str]) -> List[str]:
        matched = []
        for node, attrs in self.graph.nodes(data=True):
            name = attrs.get("name", "").lower()
            tags = attrs.get("tags", [])
            if any(kw.lower() in name for kw in keywords) or any(kw.lower() in tags for kw in keywords):
                matched.append(node)
        return matched