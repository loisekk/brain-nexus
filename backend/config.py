from pydantic_settings import BaseSettings
from pathlib import Path
from typing import List


class Settings(BaseSettings):
    app_name: str = "Loisekk AI — Second Brain"
    app_version: str = "1.0.0"
    debug: bool = False

    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""
    use_neo4j: bool = True

    data_dir: Path = Path(__file__).parent.parent / "graphify-out"
    nodes_file: str = "graphify_nodes.json"
    edges_file: str = "graphify_edges.json"
    knowledge_graph_file: str = "public/knowledge-graph.json"

    embed_model: str = "all-MiniLM-L6-v2"
    embed_dim: int = 384
    top_k_search: int = 20
    top_k_vector: int = 100

    openai_api_key: str = ""
    groq_api_key: str = ""
    llm_provider: str = "groq"
    llm_model: str = "llama-3.3-70b-versatile"

    cors_origins: List[str] = ["http://localhost:5173", "http://localhost:4173", "http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()