# brain-nexus 🧠🔗

**Interactive knowledge graph visualizer** — Sigma.js WebGL renderer with ForceAtlas2/Tree/Circle layouts for exploring large multi-project codebase graphs at scale.

> *Fork of [GitNexus](https://github.com/abhigyanpatwari/GitNexus) — the zero-server code intelligence engine. This fork adds custom data sources, rebranded AI assistant, and plans for a standalone backend.*

---

## Features

- **76,539 nodes · 269,962 edges** merged across 67 projects
- **Sigma.js WebGL rendering** — smooth 60fps on large graphs
- **3 view modes**: Force-directed (FA2), Tree (hierarchical), Circles (concentric)
- **⌘K instant search** — type-ahead autocomplete across all nodes
- **Left sidebar**: File tree + node type/edge type filters + depth filter
- **Right panel**: Loisekk AI chat + Process Flow explorer
- **Node inspection**: click any node for details, neighbors, file references
- **Synapse Query console** (rebranded Cypher) — run graph queries interactively
- **Community clustering**: Leiden algorithm + community-based coloring
- **Responsive design**: dark theme, collapsible panels, mobile-ready

---

## Quick Start

```bash
npm install
npm run dev
```

Opens at `http://localhost:5173`.

The app auto-loads `knowledge-graph.json` from the project root on startup. To load a different graph, pass a `?data=` URL param:

```
http://localhost:5173/?data=https://example.com/your-graph.json
```

Or connect to a local [GitNexus](https://github.com/abhigyanpatwari/GitNexus) backend (run `gitnexus serve` in any repo) — the UI auto-detects it.

---

## Data Sources

The default bundled graph aggregates three sources:

| Source | Nodes | Content |
|--------|-------|---------|
| **GitNexus** (code intelligence) | 45,077 | Functions, classes, imports, call graphs, file hierarchies from 67 repos |
| **Galaxy** (yours) | 28,943 | Project metadata, file relationships, concepts, keywords, cross-project structure |
| **Graphify** (yours) | 2,519 | Session memories, conversations, development rationale |

The Galaxy and Graphify datasets are custom — they're not part of upstream GitNexus.

---

## Loisekk AI

The built-in chat assistant (rebranded from GitNexus's "Nexus AI"). Uses LangChain with 7 Graph RAG tools. Supports any OpenAI-compatible provider — configure your API key in Settings.

Example queries:
- *"Which projects use FastAPI?"*
- *"Show me all ML projects and their dependencies"*
- *"What functions call pandas.read_csv?"*
- *"Find connections between worldmonitor and opencode-second-brain"*

---

## Synapse Query

Rebranded Cypher console — same graph query syntax, Loisekk branding. Run queries like:

```cypher
MATCH (c:Community {heuristicLabel: 'Authentication'})<-[:CodeRelation {type: 'MEMBER_OF'}]-(fn)
MATCH (caller)-[r:CodeRelation {type: 'CALLS'}]->(fn)
WHERE r.confidence > 0.8
RETURN caller.name, fn.name, r.confidence
ORDER BY r.confidence DESC
```

---

## Architecture

```
Frontend (brain-nexus)           Backend (FastAPI — WIP)      Database
┌─────────────────────┐       ┌──────────────────┐      ┌──────────────┐
│ Sigma.js + React 19 │──────▶│ /api/chat        │─────▶│ Neo4j        │
│ ⌘K Search           │       │ /api/synapse     │      │ 76,539 nodes │
│ 3 Layout Modes      │       │ /api/search      │      │ 269,962 edges│
│ File Tree           │       │ /api/node/:id    │      │ Full-text idx│
│ Synapse Query FAB   │       │ /api/embed       │      │ Vector index │
│ Loisekk AI Chat     │──────▶│ Loisekk Agent    │      └──────────────┘
└─────────────────────┘       └──────────────────┘
```

The backend and Neo4j integration are **not yet built** — currently the frontend runs entirely in-browser with GitNexus WASM-backed tools. See [Phase 2 roadmap](./ROADMAP.md).

---

## Data Format

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

---

## Tech Stack

| Layer          | Tech                                              |
| -------------- | ------------------------------------------------- |
| **Rendering**  | Sigma.js + Graphology (WebGL)                     |
| **Frontend**   | React 19, TypeScript, Vite 8, Tailwind v4         |
| **AI Agent**   | LangChain ReAct (client-side)                     |
| **LLM Providers** | OpenAI, Anthropic, Gemini, DeepSeek, Ollama + 4 more |
| **Clustering** | Graphology (Leiden)                               |
| **Search**     | GitNexus hybrid (BM25 + semantic + RRF)           |
| **i18n**       | English only                                      |

---

## What's Custom vs. Upstream

| Component | Source |
|-----------|--------|
| Graph renderer, layouts, file tree, filters | GitNexus (unmodified) |
| LangChain agent, 7 Graph RAG tools | GitNexus (unmodified) |
| LLM provider system | GitNexus (unmodified) |
| **Galaxy data** (28,943 nodes) | **Custom** — project metadata across 67 repos |
| **Graphify data** (2,519 nodes) | **Custom** — session memories & context |
| **Branding**: brain-nexus, Loisekk AI, Synapse Query | **Custom** |
| **Backend** (FastAPI + Neo4j) | **Planned** — see [ROADMAP.md](./ROADMAP.md) |

---

## Roadmap

- [x] Phase 1: Frontend cleanup — rebranding, English-only, auto-load, heartbeat fix
- [ ] Phase 2: FastAPI backend + Neo4j
- [ ] Phase 3: Loisekk AI server-side agent with persistent memory
- [ ] Phase 4: Pre-computed embeddings for all 76K nodes
- [ ] Phase 5: Polish, deploy, CI/CD

See [ROADMAP.md](./ROADMAP.md) for full details.

---

## Credits

Visualizer engine built on [GitNexus](https://github.com/abhigyanpatwari/GitNexus) by [Abhigyan Patwari](https://github.com/abhigyanpatwari). Sigma.js graph rendering, FA2 layout, file tree, Graph RAG agent, and Cypher console are all from the GitNexus project.

Custom data sources and branding by [Yash Brahmankar](https://github.com/loisekk).
