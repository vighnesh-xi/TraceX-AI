from graph.dependency_graph import DependencyGraph

def test_graph_build_and_usages():
    graph = DependencyGraph()
    chunks = [
        {"chunk_id": "a::login", "name": "login", "type": "function", "file_path": "a.py", "tags": [], "calls": ["validate"], "imports": []},
        {"chunk_id": "b::validate", "name": "validate", "type": "function", "file_path": "b.py", "tags": [], "calls": [], "imports": []},
    ]
    graph.build(chunks)
    assert graph.graph.number_of_nodes() == 2
    usages = graph.find_usages("validate")
    assert "a::login" in usages