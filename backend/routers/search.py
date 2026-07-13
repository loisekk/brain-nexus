import logging

from fastapi import APIRouter, Query

from backend.database import graph_store, embeddings

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/search", tags=["Search"])


@router.get("")
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = Query(20, ge=1, le=100),
    vector: bool = Query(False, description="Use vector (semantic) search")
):
    if vector and embeddings.loaded:
        vec_results = embeddings.search(q, k=limit)
        vec_node_ids = {r["node_id"] for r in vec_results}
        nodes = []
        for r in vec_results:
            node = graph_store.get_node(r["node_id"])
            if node:
                node["_score"] = r["score"]
                nodes.append(node)
        return {"query": q, "results": nodes, "count": len(nodes), "mode": "vector"}

    nodes = graph_store.search_nodes(q, limit=limit)
    return {"query": q, "results": nodes[:limit], "count": len(nodes[:limit]), "mode": "text"}