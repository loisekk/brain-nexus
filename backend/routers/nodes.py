import logging

from fastapi import APIRouter, HTTPException, Query

from backend.database import graph_store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/node", tags=["Nodes"])


@router.get("/{node_id}")
async def get_node(node_id: str):
    node = graph_store.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    neighbors = graph_store.get_neighbors(node_id)
    return {"node": node, "neighbors": neighbors, "neighbor_count": len(neighbors)}


@router.get("/{node_id}/neighbors")
async def get_node_neighbors(
    node_id: str,
    depth: int = Query(1, ge=1, le=5),
    limit: int = Query(50, ge=1, le=500)
):
    node = graph_store.get_node(node_id)
    if not node:
        raise HTTPException(status_code=404, detail="Node not found")
    neighbors = graph_store.get_neighbors(node_id, max_depth=depth, limit=limit)
    return {"node": node, "neighbors": neighbors, "count": len(neighbors)}


@router.get("/{node_id}/path")
async def find_path(node_id: str, target: str = Query(..., description="Target node ID")):
    path = graph_store.find_path(node_id, target)
    if not path:
        raise HTTPException(status_code=404, detail="No path found")
    return {"source": node_id, "target": target, "path": path, "length": len(path)}