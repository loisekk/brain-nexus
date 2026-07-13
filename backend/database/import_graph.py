import json
import logging
from pathlib import Path
from typing import Dict, Any, List

from backend.config import settings
from backend.database.graph_store import graph_store

logger = logging.getLogger(__name__)


def load_graph_json(path: str = "knowledge-graph.json") -> Dict[str, Any]:
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = Path(__file__).parent.parent.parent / file_path

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


def import_to_neo4j(data: Dict[str, Any]) -> None:
    from backend.database.neo4j_client import neo4j_client

    if not neo4j_client.connected:
        logger.info("Connecting to Neo4j...")
        if not neo4j_client.connect():
            logger.error("Neo4j not connected, cannot import")
            return

    nodes = data.get("nodes", [])
    edges = data.get("edges", [])

    logger.info(f"Starting Neo4j import: {len(nodes)} nodes, {len(edges)} edges")
    nc = neo4j_client.import_nodes_batch(nodes)
    ec = neo4j_client.import_edges_batch(edges)
    neo4j_client.create_indexes()
    logger.info(f"Neo4j import complete: {nc} nodes, {ec} edges")


def import_knowledge_graph() -> None:
    data = load_graph_json(settings.knowledge_graph_file)
    import_to_neo4j(data)