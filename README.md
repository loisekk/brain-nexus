# brain-nexus 🧠🔗

**Interactive knowledge graph visualizer** — Sigma.js WebGL renderer with ForceAtlas2/Tree/Circle layouts for exploring codebases at scale.

Powered by [GitNexus](https://github.com/abhigyanpatwari/GitNexus) — the zero-server code intelligence engine.

## Features

- **76,539 nodes · 269,962 edges** merged across 67 projects
- **Sigma.js WebGL rendering** — smooth 60fps on large graphs
- **3 view modes**: Force-directed (FA2), Tree (hierarchical), Circles (concentric)
- **⌘K instant search** — type-ahead autocomplete across all nodes
- **Left sidebar**: File tree + node type/edge type filters + depth filter
- **Right panel**: AI Graph RAG chat + process flow explorer
- **Node inspection**: click any node for details, neighbors, file references
- **Cypher query console**: run graph queries interactively
- **Community clustering**: Leiden algorithm + community-based coloring
- **Responsive design**: dark theme, collapsible panels, mobile-ready

## Quick Start

```bash
npm install
npm run dev
```

Opens at `http://localhost:5173`.

Load your knowledge graph by passing a `?data=` URL param:

```
http://localhost:5173/?data=https://example.com/your-graph.json
```

## Data Format

The app loads a JSON knowledge graph with this structure:

```json
{
  "nodes": [
    { "id": "...", "label": "main.py", "type": "file", "project": "my-project", "source_file": "..." }
  ],
  "edges": [
    { "source": "...", "target": "...", "relation": "imports", "confidence": "EXTRACTED" }
  ]
}
```

## Credits

Built on [GitNexus](https://github.com/abhigyanpatwari/GitNexus) by [Abhigyan Patwari](https://github.com/abhigyanpatwari). The Sigma.js graph rendering, FA2 layout, file tree, Graph RAG agent, and Cypher console are all from the GitNexus project.
