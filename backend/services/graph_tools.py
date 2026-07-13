from typing import Optional, Dict, Any, List

from backend.database import graph_store


def tool_get_node(node_id: str) -> str:
    node = graph_store.get_node(node_id)
    if not node:
        return f"Node '{node_id}' not found."

    label = node.get("label", node.get("name", "unknown"))
    nid = node.get("id", "")
    community = node.get("community", node.get("_table", "N/A"))
    project = node.get("project", "N/A")
    source = node.get("source_file", node.get("filePath", "N/A"))

    parts = [f"Node: {label} (id={nid})"]
    if community != "N/A":
        parts.append(f"| Community: {community}")
    if project != "N/A":
        parts.append(f"| Project: {project}")
    if source != "N/A":
        parts.append(f"| Source: {source}")
    return " ".join(parts)


def tool_search_nodes(query: str, limit: int = 10) -> str:
    results = graph_store.search_nodes(query, limit)
    if not results:
        return "No nodes found."

    lines = [f"Found {len(results)} nodes:"]
    for n in results:
        label = n.get("label", n.get("name", "?"))
        nid = n.get("id", "?")
        lines.append(f"  • {label} ({nid})")
    return "\n".join(lines)


def tool_get_neighbors(node_id: str, depth: int = 1) -> str:
    node = graph_store.get_node(node_id)
    name = node.get("label", node_id) if node else node_id
    neighbors = graph_store.get_neighbors(node_id, max_depth=depth, limit=100)
    if not neighbors:
        return f"No neighbors found for '{name}'."

    lines = [f"Neighbors of {name} ({len(neighbors)} found):"]
    for n in neighbors[:25]:
        label = n.get("label", n.get("name", "?"))
        nid = n.get("id", "?")
        lines.append(f"  • {label} ({nid})")
    if len(neighbors) > 25:
        lines.append(f"  ... and {len(neighbors) - 25} more")
    return "\n".join(lines)


def tool_find_path(source: str, target: str) -> str:
    paths = graph_store.find_path(source, target)
    if not paths:
        return f"No path found between '{source}' and '{target}'."

    lines = [f"Found {len(paths)} path(s):"]
    path_labels = []
    for nid in paths:
        node = graph_store.get_node(nid)
        path_labels.append(node.get("label", nid) if node else nid)
    lines.append("  Path 1: " + " → ".join(path_labels))
    return "\n".join(lines)


def tool_community(community_id: str, limit: int = 50) -> str:
    node_ids = graph_store.get_community_nodes(community_id, limit)
    if not node_ids:
        return f"No nodes found in community '{community_id}'."

    lines = [f"Community '{community_id}': {len(node_ids)} nodes"]
    for nid in node_ids[:20]:
        node = graph_store.get_node(nid)
        label = node.get("label", nid) if node else nid
        lines.append(f"  • {label}")
    if len(node_ids) > 20:
        lines.append(f"  ... and {len(node_ids) - 20} more")
    return "\n".join(lines)


def tool_project(name: str, limit: int = 50) -> str:
    node_ids = graph_store.get_project_nodes(name, limit)
    if not node_ids:
        return f"No nodes found in project '{name}'."

    lines = [f"Project '{name}': {len(node_ids)} nodes"]
    for nid in node_ids[:20]:
        node = graph_store.get_node(nid)
        label = node.get("label", nid) if node else nid
        lines.append(f"  • {label}")
    if len(node_ids) > 20:
        lines.append(f"  ... and {len(node_ids) - 20} more")
    return "\n".join(lines)


def tool_stats() -> str:
    stats = graph_store.get_stats()
    return (
        f"Knowledge Graph Statistics:\n"
        f"  Total Nodes: {stats['total_nodes']:,}\n"
        f"  Total Edges: {stats['total_edges']:,}\n"
        f"  Projects: {stats['total_projects']}\n"
        f"  Communities: {stats['total_communities']}"
    )


ALL_TOOLS = {
    "get_node": {
        "function": tool_get_node,
        "description": "Get details of a specific node by its ID. The ID is a unique identifier for a code entity.",
        "parameters": {"node_id": "string"}
    },
    "search_nodes": {
        "function": tool_search_nodes,
        "description": "Search for nodes by label or name. Returns matching nodes.",
        "parameters": {"query": "string", "limit": "int (optional, default 10)"}
    },
    "get_neighbors": {
        "function": tool_get_neighbors,
        "description": "Find neighboring nodes connected to a given node. Use this to explore relationships.",
        "parameters": {"node_id": "string", "depth": "int (optional, default 1)"}
    },
    "find_path": {
        "function": tool_find_path,
        "description": "Find connection paths between two nodes. Use this to understand how entities relate.",
        "parameters": {"source": "string", "target": "string"}
    },
    "community": {
        "function": tool_community,
        "description": "List nodes in a community by community ID.",
        "parameters": {"community_id": "string", "limit": "int"}
    },
    "project": {
        "function": tool_project,
        "description": "List nodes belonging to a specific project.",
        "parameters": {"name": "string", "limit": "int"}
    },
    "stats": {
        "function": tool_stats,
        "description": "Get overall knowledge graph statistics.",
        "parameters": {}
    }
}


def run_tool(name: str, **kwargs) -> str:
    tool = ALL_TOOLS.get(name)
    if not tool:
        return f"Unknown tool: {name}"
    return tool["function"](**kwargs)