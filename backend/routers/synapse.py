import logging

from fastapi import APIRouter
from pydantic import BaseModel

from backend.database import graph_store

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/synapse", tags=["Synapse"])

SYNAPSE_HELP = """
# Synapse Query Language

Query the knowledge graph using these operations:

## Operations
- **get_node**: Get a node by its ID
  - params: { "node_id": "<id>" }
- **search**: Search nodes by name or label
  - params: { "query": "<text>", "limit": 20 }
- **neighbors**: Find neighbors of a node
  - params: { "node_id": "<id>", "depth": 1, "limit": 50 }
- **path**: Find the shortest path between two nodes
  - params: { "source": "<id>", "target": "<id>" }
- **community**: List nodes in a community
  - params: { "community_id": "<id>", "limit": 100 }
- **project**: List nodes in a project
  - params: { "project": "<name>", "limit": 100 }
- **stats**: Get knowledge graph statistics
  - params: {}
"""


class SynapseRequest(BaseModel):
    type: str
    params: dict = {}


class SynapseResponse(BaseModel):
    result: list | dict | None = None
    error: str | None = None


@router.post("")
async def execute_synapse(request: SynapseRequest):
    response = graph_store.execute_synapse(request.type, request.params)
    return response


@router.get("/help")
async def synapse_help():
    return {"help": SYNAPSE_HELP}