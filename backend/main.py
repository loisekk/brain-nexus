import asyncio
import json
import logging
import sys
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.config import settings
from backend.database import graph_store, embeddings
from backend.routers import chat, nodes, search, stats, synapse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)


async def _build_embeddings_background():
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, embeddings.load_model)
        await loop.run_in_executor(None, embeddings.load_index)
        if not embeddings.loaded:
            logger.info("Building FAISS vector index (background thread)...")
            await loop.run_in_executor(None, embeddings.build_index, graph_store.nodes)
            await loop.run_in_executor(None, embeddings.save_index)
            logger.info("FAISS vector index ready")
    except Exception as e:
        logger.warning(f"Embeddings not available: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting {settings.app_name} v{settings.app_version}")

    graph_store.load(settings.knowledge_graph_file)

    asyncio.create_task(_build_embeddings_background())

    if settings.use_neo4j:
        try:
            from backend.database.neo4j_client import neo4j_client
            neo4j_client.connect()
            logger.info("Neo4j connected")
        except Exception as e:
            logger.warning(f"Neo4j not available: {e}")

    app.state.graph_store = graph_store
    app.state.embeddings = embeddings

    yield

    if settings.use_neo4j:
        try:
            from backend.database.neo4j_client import neo4j_client
            if hasattr(neo4j_client, "close"):
                neo4j_client.close()
        except Exception:
            pass
    logger.info("Shutdown complete")


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins + ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(stats.router)
app.include_router(nodes.router)
app.include_router(search.router)
app.include_router(synapse.router)
app.include_router(chat.router)


@app.get("/api/health")
async def health():
    return {
        "status": "ok",
        "app": settings.app_name,
        "version": settings.app_version,
        "graph_loaded": graph_store.loaded,
        "nodes": len(graph_store.nodes),
        "edges": len(graph_store.edges)
    }


@app.get("/graph-data.json")
async def graph_data():
    nodes = []
    for n in graph_store.nodes:
        entry = {
            "id": n.get("id"),
            "label": n.get("label", n.get("name", "")),
            "type": n.get("type", n.get("_table", "unknown")),
            "project": n.get("project", n.get("_repo", "unknown")),
        }
        community = n.get("community", n.get("_table", ""))
        if community:
            entry["community"] = community
        nodes.append(entry)

    edges = []
    for e in graph_store.edges:
        edges.append({
            "source": e.get("source", e.get("sourceId")),
            "target": e.get("target", e.get("targetId")),
            "relation": e.get("relation", e.get("type", "related")),
            "confidence": e.get("confidence", "EXTRACTED")
        })

    return JSONResponse({"nodes": nodes, "edges": edges})


@app.get("/api/graph/subsample")
async def graph_subsample(
    community: str = Query(None),
    project: str = Query(None),
    limit: int = Query(1000, ge=1, le=10000)
):
    if community:
        ids = set(graph_store.get_community_nodes(community, limit))
    elif project:
        ids = set(graph_store.get_project_nodes(project, limit))
    else:
        return JSONResponse({"error": "Provide community or project"}, status_code=400)

    filtered_nodes = [n for n in graph_store.nodes if n.get("id") in ids]
    filtered_edges = [
        e for e in graph_store.edges
        if e.get("source") in ids or e.get("target") in ids
    ]
    return JSONResponse({
        "nodes": filtered_nodes[:limit],
        "edges": filtered_edges[:limit * 2],
        "total_nodes": len(filtered_nodes),
        "total_edges": len(filtered_edges)
    })


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)