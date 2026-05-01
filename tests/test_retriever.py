from indexing.bm25_index import BM25Index

def test_bm25_search():
    index = BM25Index()
    chunks = [
        {"chunk_id": "a::login", "content": "def login user authenticate token", "file_type": "code"},
        {"chunk_id": "b::register", "content": "def register new user account", "file_type": "code"},
    ]
    index.build(chunks)
    results = index.search("login user", top_k=2)
    assert len(results) > 0
    assert results[0]["chunk_id"] == "a::login"