import logging
from typing import Optional, Dict, Any, List

from neo4j import GraphDatabase, Driver

from backend.config import settings

logger = logging.getLogger(__name__)


class Neo4jClient:
    def __init__(self):
        self._driver: Optional[Driver] = None
        self._connected = False

    @property
    def connected(self) -> bool:
        return self._connected

    def connect(self) -> bool:
        try:
            self._driver = GraphDatabase.driver(
                settings.neo4j_uri,
                auth=(settings.neo4j_user, settings.neo4j_password),
                max_connection_lifetime=3600,
                max_connection_pool_size=50,
                connection_acquisition_timeout=10,
            )
            self._driver.verify_connectivity()
            self._connected = True
            logger.info(f"Connected to Neo4j at {settings.neo4j_uri}")
            self._ensure_schema()
            return True
        except Exception as e:
            logger.warning(f"Neo4j not available: {e}")
            self._connected = False
            return False

    def _ensure_schema(self) -> None:
        queries = [
            "CREATE CONSTRAINT nid IF NOT EXISTS FOR (n:Node) REQUIRE n.id IS UNIQUE",
        ]
        try:
            with self._driver.session() as session:
                for q in queries:
                    try:
                        session.run(q)
                    except Exception:
                        pass
        except Exception:
            pass

    def close(self) -> None:
        if self._driver:
            self._driver.close()
            self._connected = False

    def run(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        if not self._driver:
            return []
        with self._driver.session() as session:
            result = session.run(query, params or {})
            return [dict(record) for record in result]

    def import_nodes_batch(self, nodes: List[Dict[str, Any]], batch_size: int = 5000) -> int:
        if not self._driver:
            return 0
        total = 0
        with self._driver.session() as session:
            for i in range(0, len(nodes), batch_size):
                batch = nodes[i:i + batch_size]
                query = """
                UNWIND $batch AS node
                MERGE (n:Node {id: node.id})
                SET n.label = node.label,
                    n.type = node.type,
                    n.project = node.project,
                    n.source_file = node.source_file,
                    n.degree = node.degree
                """
                session.run(query, {"batch": batch})
                total += len(batch)
                if total % 20000 == 0:
                    logger.info(f"Imported {total} nodes...")
        return total

    def import_edges_batch(self, edges: List[Dict[str, Any]], batch_size: int = 5000) -> int:
        if not self._driver:
            return 0
        total = 0
        with self._driver.session() as session:
            for i in range(0, len(edges), batch_size):
                batch = edges[i:i + batch_size]
                query = """
                UNWIND $batch AS edge
                MATCH (a:Node {id: edge.source})
                MATCH (b:Node {id: edge.target})
                MERGE (a)-[r:RELATES {type: edge.relation}]->(b)
                SET r.confidence = edge.confidence
                """
                session.run(query, {"batch": batch})
                total += len(batch)
                if total % 20000 == 0:
                    logger.info(f"Imported {total} edges...")
        return total

    def create_indexes(self) -> None:
        if not self._driver:
            return
        indexes = [
            "CREATE FULLTEXT INDEX node_text IF NOT EXISTS FOR (n:Node) ON EACH [n.id, n.label, n.project, n.source_file]",
            "CREATE INDEX node_type IF NOT EXISTS FOR (n:Node) ON (n.type)",
            "CREATE INDEX node_project IF NOT EXISTS FOR (n:Node) ON (n.project)",
            "CREATE VECTOR INDEX node_vec IF NOT EXISTS FOR (n:Node) ON (n.embedding) OPTIONS {indexConfig: {`vector.dimensions`: 384, `vector.similarity_function`: 'cosine'}}",
        ]
        with self._driver.session() as session:
            for q in indexes:
                try:
                    session.run(q)
                except Exception:
                    pass
            logger.info("Indexes created/verified")


neo4j_client = Neo4jClient()