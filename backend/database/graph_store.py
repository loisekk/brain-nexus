import json
import logging
from pathlib import Path
from typing import Optional, List, Dict, Any
from collections import defaultdict

from backend.config import settings

logger = logging.getLogger(__name__)


class GraphStore:
    def __init__(self):
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
        self._node_index: Dict[str, Dict[str, Any]] = {}
        self._adjacency: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._reverse_adj: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self._community_index: Dict[str, List[str]] = defaultdict(list)
        self._project_index: Dict[str, List[str]] = defaultdict(list)
        self._loaded = False

    @property
    def loaded(self) -> bool:
        return self._loaded

    @property
    def projects(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for n in self.nodes:
            p = n.get("project", "unknown")
            counts[p] = counts.get(p, 0) + 1
        return counts

    @property
    def communities(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for n in self.nodes:
            c = n.get("community", n.get("_table", "unknown"))
            counts[c] = counts.get(c, 0) + 1
        return counts

    def load(self, path: Optional[str] = None) -> None:
        file_path = Path(path) if path else Path(settings.knowledge_graph_file)
        if not file_path.is_absolute():
            file_path = Path(__file__).parent.parent.parent / file_path

        logger.info(f"Loading graph from {file_path}")
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.nodes = data.get("nodes", [])
        self.edges = data.get("edges", [])
        self._build_indexes()
        self._loaded = True
        logger.info(f"Loaded {len(self.nodes)} nodes, {len(self.edges)} edges")

    def _build_indexes(self) -> None:
        self._node_index.clear()
        self._adjacency.clear()
        self._reverse_adj.clear()
        self._community_index.clear()
        self._project_index.clear()

        for n in self.nodes:
            nid = n.get("id")
            if nid:
                self._node_index[nid] = n
                c = n.get("community", n.get("_table", "unknown"))
                self._community_index[c].append(nid)
                p = n.get("project", "unknown")
                self._project_index[p].append(nid)

        for e in self.edges:
            src = e.get("source")
            tgt = e.get("target")
            if src:
                self._adjacency[src].append(e)
            if tgt:
                self._reverse_adj[tgt].append(e)

    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        return self._node_index.get(node_id)

    def get_neighbors(self, node_id: str, max_depth: int = 1, limit: int = 50) -> List[Dict[str, Any]]:
        visited = {node_id}
        frontier = {node_id}
        results: List[Dict[str, Any]] = []

        for _ in range(max_depth):
            next_frontier = set()
            for fid in frontier:
                edges = self._adjacency.get(fid, []) + self._reverse_adj.get(fid, [])
                for e in edges:
                    target = e.get("source") if e.get("target") == fid else e.get("target")
                    if target and target not in visited:
                        visited.add(target)
                        next_frontier.add(target)
                        node = self._node_index.get(target)
                        if node:
                            results.append(node)
                    if len(results) >= limit:
                        return results[:limit]
            frontier = next_frontier
        return results[:limit]

    def find_path(self, source: str, target: str, max_depth: int = 5) -> Optional[List[str]]:
        if source not in self._node_index or target not in self._node_index:
            return None
        if source == target:
            return [source]

        from collections import deque
        queue = deque([(source, [source])])
        visited = {source}

        while queue:
            current, path = queue.popleft()
            if len(path) > max_depth:
                continue

            for e in self._adjacency.get(current, []) + self._reverse_adj.get(current, []):
                neighbor = e.get("source") if e.get("target") == current else e.get("target")
                if not neighbor:
                    continue
                if neighbor == target:
                    return path + [target]
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        return None

    def search_nodes(self, query: str, limit: int = 20) -> List[Dict[str, Any]]:
        q = query.lower()
        results = []
        for n in self.nodes:
            label = str(n.get("label", "")).lower()
            nid = str(n.get("id", "")).lower()
            project = str(n.get("project", "")).lower()
            source_file = str(n.get("source_file", "")).lower()
            if q in label or q in nid or q in project or q in source_file:
                results.append(n)
            if len(results) >= limit:
                break
        return results

    def get_community_nodes(self, community_id: str, limit: int = 100) -> List[str]:
        ids = self._community_index.get(community_id, [])
        return ids[:limit]

    def get_project_nodes(self, project: str, limit: int = 100) -> List[str]:
        matched = []
        for nid in self._project_index.get(project, []):
            matched.append(nid)
            if len(matched) >= limit:
                break
        return matched

    def get_stats(self) -> Dict[str, Any]:
        project_counts = dict(sorted(self.projects.items(), key=lambda x: x[1], reverse=True)[:30])
        community_counts = dict(sorted(self.communities.items(), key=lambda x: x[1], reverse=True)[:30])

        type_counts: Dict[str, int] = {}
        for n in self.nodes:
            t = n.get("type", "unknown")
            type_counts[t] = type_counts.get(t, 0) + 1

        return {
            "total_nodes": len(self.nodes),
            "total_edges": len(self.edges),
            "total_projects": len(self.projects),
            "total_communities": len(self.communities),
            "top_projects": project_counts,
            "top_communities": community_counts,
            "node_types": dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True))
        }

    def execute_synapse(self, query_type: str, params: Dict[str, Any]) -> Dict[str, Any]:
        if query_type == "get_node":
            node = self.get_node(params.get("node_id", ""))
            return {"result": node} if node else {"error": "Node not found"}
        elif query_type == "search":
            return {"result": self.search_nodes(params.get("query", ""), params.get("limit", 20))}
        elif query_type == "neighbors":
            return {"result": self.get_neighbors(params.get("node_id", ""), params.get("depth", 1), params.get("limit", 50))}
        elif query_type == "path":
            path = self.find_path(params.get("source", ""), params.get("target", ""))
            return {"result": path} if path else {"error": "No path found"}
        elif query_type == "community":
            return {"result": self.get_community_nodes(params.get("community_id", ""), params.get("limit", 100))}
        elif query_type == "project":
            return {"result": self.get_project_nodes(params.get("project", ""), params.get("limit", 100))}
        elif query_type == "stats":
            return {"result": self.get_stats()}
        else:
            return {"error": f"Unknown query type: {query_type}"}


graph_store = GraphStore()