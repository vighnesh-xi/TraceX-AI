from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    response = client.get("/api/v1/docs")
    assert response.status_code == 200

def test_query_without_index():
    response = client.post("/api/v1/query", json={"query": "how does auth work?"})
    assert response.status_code == 400