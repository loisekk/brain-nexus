import logging

from fastapi import APIRouter

from backend.database import graph_store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/stats", tags=["Stats"])


@router.get("")
async def get_stats():
    stats = graph_store.get_stats()
    top_projects = dict(sorted(graph_store.projects.items(), key=lambda x: x[1], reverse=True)[:20])
    top_communities = dict(sorted(graph_store.communities.items(), key=lambda x: x[1], reverse=True)[:20])
    stats["top_projects"] = top_projects
    stats["top_communities"] = top_communities
    return stats