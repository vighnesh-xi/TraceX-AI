from pydantic import BaseModel
from typing import Optional, Any

class IndexRequest(BaseModel):
    repo_path: Optional[str] = None
    github_url: Optional[str] = None

class QueryRequest(BaseModel):
    query: str
    query_type: str = "explain"
    top_k: int = 5

class QueryResponse(BaseModel):
    query_type: str
    answer: str
    sections: Any = []
    references: Any = []
    navigation_hints: Any = []
    usages: Any = []