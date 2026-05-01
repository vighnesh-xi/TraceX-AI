from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    OPENAI_API_KEY: str = ""
    LLM_MODEL: str = "gpt-4o"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    FAISS_INDEX_PATH: str = "./data/faiss_index"
    BM25_INDEX_PATH: str = "./data/bm25_index.pkl"
    GRAPH_PATH: str = "./data/dependency_graph.pkl"
    GROQ_API_KEY: str = ""
    APP_HOST: str = "0.0.0.0"
    APP_PORT: int = 8000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"

settings = Settings()