<div align="center">

  <h1>brain-nexus 🧠🔗</h1>

  <p><strong>Interactive knowledge graph visualizer</strong> — Sigma.js WebGL renderer with ForceAtlas2/Tree/Circle layouts for exploring multi-project codebase graphs at scale.</p>

  <p><strong>76,539 nodes · 269,962 edges</strong> — merged across 67 projects from three data sources.</p>

  <a href="https://github.com/loisekk/brain-nexus">
    <img src="https://img.shields.io/github/stars/loisekk/brain-nexus?style=social" alt="GitHub stars"/>
  </a>
  <a href="https://github.com/loisekk/brain-nexus">
    <img src="https://img.shields.io/github/forks/loisekk/brain-nexus?style=social" alt="GitHub forks"/>
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT"/>
  </a>
  <a href="https://github.com/loisekk/brain-nexus/issues">
    <img src="https://img.shields.io/github/issues/loisekk/brain-nexus" alt="GitHub issues"/>
  </a>

</div>

---

> _Like DeepWiki, but deeper._ DeepWiki helps you _understand_ code. brain-nexus lets you _analyze_ it — because a knowledge graph tracks every relationship, not just descriptions.

**TL;DR:** Drop in a `knowledge-graph.json` and get instant graph exploration across **76,539 nodes · 269,962 edges** merged across 67 projects — plus a built-in AI assistant (Loisekk AI) and rebranded Cypher console (Synapse Query).

Built on [GitNexus](https://github.com/abhigyanpatwari/GitNexus) — the zero-server code intelligence engine — with **custom data sources** (Galaxy + Graphify) and unique branding.

https://github.com/user-attachments/assets/172685ba-8e54-4ea7-9ad1-e31a3398da72
---

## Features

| | |
|-|-|
| 🎨 **Sigma.js WebGL rendering** — smooth 60fps at scale | 🔍 **⌘K instant search** — type-ahead across all nodes |
| 🗺️ **3 view modes** — Force-directed (FA2), Tree, Circles | 📂 **Left sidebar** — file tree + node/edge type + depth filters |
| 🤖 **Loisekk AI chat** — LangChain agent with 7 Graph RAG tools | 🔬 **Node inspection** — click for details, neighbors, references |
| ⚡ **Synapse Query console** — rebranded Cypher with examples | 🎨 **Community clustering** — Leiden + coloring |
| 🌙 **Dark theme** — responsive, collapsible panels, mobile-ready | 🔌 **Local backend support** — auto-connect to `gitnexus serve` |

---


## Two Ways to Use

| | **Static JSON** | **Local Backend** |
|---|---|---|
| **What** | Built-in `knowledge-graph.json` with 76K+ nodes | Connect to `gitnexus serve` running locally |
| **For** | Immediate exploration, demos, pre-built graphs | Live analysis of your own repos |
| **Scale** | 76,539 nodes · 269,962 edges (pre-merged) | Full repos, any size |
| **Setup** | `npm install && npm run dev` | `npx gitnexus serve` + open UI |
| **Privacy** | Everything in-browser, no server | Everything local, no network |

---

## Data Sources

The bundled graph aggregates **three sources** into one unified knowledge base:

| Source | Nodes | What it contains |
|--------|-------|-----------------|
| **GitNexus** (code intelligence) | 45,077 | Functions, classes, imports, call graphs, file hierarchies from 67 repos |
| **Galaxy** *(custom)* | 28,943 | Project metadata, file relationships, concepts, keywords, cross-project structure |
| **Graphify** *(custom)* | 2,519 | Session memories, conversations, development rationale, context |

> The Galaxy and Graphify datasets are **your own custom additions** — they don't exist in upstream GitNexus.

---

## Quick Start

```bash
# Clone
git clone https://github.com/loisekk/brain-nexus.git
cd brain-nexus

# Install & run
npm install
npm run dev
```

Opens at `http://localhost:5173` with the full knowledge graph pre-loaded.

### Load a different graph

```bash
# Via URL param
http://localhost:5173/?data=https://example.com/your-graph.json

# Or connect to local GitNexus backend
npx gitnexus serve   # in any indexed repo
# UI auto-detects the server
```

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

## Loisekk AI

The built-in AI assistant — rebranded from GitNexus's "Nexus AI" — has access to all three data sources:

- **Code intelligence** – functions, classes, imports, call graphs
- **Project metadata** – file relationships, concepts, cross-project connections
- **Session context** – development history, decisions, rationale

Powered by LangChain with 7 Graph RAG tools. Supports **any OpenAI-compatible provider** — configure your API key in Settings (OpenAI, Anthropic, Gemini, DeepSeek, Ollama, and more).

### Example queries

```
"Which projects use FastAPI?"
"Show me all ML projects and their dependencies"
"What functions call pandas.read_csv?"
"Show the architecture of the worldmonitor project"
"Find connections between worldmonitor and opencode-second-brain"
"What's the most complex project in my codebase?"
```

---

## Synapse Query

Rebranded Cypher console — same graph query syntax, Loisekk branding. Run structured queries against the knowledge graph:

```cypher
MATCH (c:Community {heuristicLabel: 'Authentication'})<-[:CodeRelation {type: 'MEMBER_OF'}]-(fn)
MATCH (caller)-[r:CodeRelation {type: 'CALLS'}]->(fn)
WHERE r.confidence > 0.8
RETURN caller.name, fn.name, r.confidence
ORDER BY r.confidence DESC
```

---

## How It Works

brain-nexus is a **browser-first** knowledge graph visualizer built on the GitNexus engine. The frontend handles everything client-side:

1. **Load** — reads JSON knowledge graph from file, URL param, or local backend
2. **Render** — Sigma.js WebGL renders 76K+ nodes at 60fps
3. **Explore** — three layout modes, ⌘K search, file tree, filters
4. **Analyze** — click nodes, inspect neighbors, traverse relationships
5. **Chat** — Loisekk AI agent with Graph RAG across all data sources
6. **Query** — Synapse Query console for custom graph exploration

### Architecture

```
Frontend (brain-nexus)           Backend (FastAPI — planned)
┌─────────────────────┐        ┌──────────────────┐
│ Sigma.js + React 19 │────────▶ /api/chat        |
│ ⌘K Search          │        │ /api/synapse     │
│ 3 Layout Modes      │        │ /api/search      │
│ File Tree           │        │ /api/node/:id    │
│ Synapse Query FAB   │        │ /api/embed       │
│ Loisekk AI Chat     │────────▶ Loisekk Agent    │
└─────────────────────┘        └──────────────────┘
```

> The FastAPI backend + Neo4j integration are **not yet built** — currently everything runs in-browser. See [roadmap](#roadmap).

---

## Roadmap

### ✅ Phase 1 — Frontend Cleanup *(complete)*
- [x] Rebrand GitNexus → brain-nexus, Nexus AI → Loisekk AI, Cypher → Synapse Query
- [x] English-only localization (removed zh-CN)
- [x] Auto-load `knowledge-graph.json` on startup
- [x] Fix heartbeat SSE to avoid false "connection lost" errors
- [x] Custom Galaxy dataset (28,943 nodes) — project metadata
- [x] Custom Graphify dataset (2,519 nodes) — session context

### 🔄 Phase 2 — FastAPI Backend *(pending)*
- [x] FastAPI scaffold with routes: chat, synapse, search, node, stats
- [x] Neo4j database: import all 76K nodes + 270K edges
- [x] Full-text and vector indexes

### 🔄 Phase 3 — Loisekk AI Agent *(pending)*
- [ ] Server-side LangChain agent with persistent cross-session memory
- [ ] Custom tools: synapse_query, semantic_search, get_node, find_path
- [ ] Custom system prompt with all 67 project context

### 🔄 Phase 4 — Embeddings *(pending)*
- [ ] Pre-compute embeddings for all 76K nodes via sentence-transformers
- [ ] Vector index in Neo4j for semantic search across all projects

### 🔄 Phase 5 — Polish *(pending)*
- [ ] Synapse Query autocomplete + syntax highlighting
- [ ] Mobile responsive polish
- [ ] Vercel deployment + GitHub Actions CI/CD
- [ ] API documentation (Swagger)

---

## Tech Stack

| Layer | Tech |
|-------|------|
| **Rendering** | Sigma.js v3 + Graphology (WebGL) |
| **Frontend** | React 19, TypeScript 5, Vite 8, Tailwind v4 |
| **AI Agent** | LangChain ReAct (client-side, 7 tools) |
| **LLM Providers** | OpenAI, Anthropic, Gemini, DeepSeek, Ollama, Azure, OpenRouter, MiniMax, GLM |
| **Clustering** | Graphology (Leiden algorithm) |
| **Search** | GitNexus hybrid (BM25 + semantic + RRF) |
| **State** | React Context + custom hooks |
| **Testing** | Vitest + Playwright E2E |
| **i18n** | English only |
| **Planned DB** | Neo4j (Cypher/Synapse compatible) |

---

## What's Custom vs. Upstream

| Component | Source |
|-----------|--------|
| Sigma.js renderer, 3 layouts, file tree, filters | GitNexus (upstream) |
| LangChain agent, 7 Graph RAG tools, LLM providers | GitNexus (upstream) |
| **Galaxy data** (28,943 nodes across 67 projects) | **Custom** |
| **Graphify data** (2,519 nodes of session context) | **Custom** |
| brain-nexus branding, Loisekk AI, Synapse Query | **Custom** |
| English-only locale, auto-load, heartbeat fix | **Custom** |
| FastAPI backend + Neo4j | **Planned** |

---

## Security & Privacy

- **Static mode**: Everything runs in your browser. No code uploaded. No server needed.
- **Backend mode**: Connect to a local `gitnexus serve` instance. All data stays on your machine.
- API keys stored in `localStorage` only (never sent to any server other than the LLM provider you configure).

---

## Credits

**Visualizer engine** built on [GitNexus](https://github.com/abhigyanpatwari/GitNexus) by [Abhigyan Patwari](https://github.com/abhigyanpatwari). Sigma.js graph rendering, ForceAtlas2 layout, file tree, Graph RAG agent, and Cypher console are all from the GitNexus project.

**Custom data sources** (Galaxy, Graphify) and **branding** (brain-nexus, Loisekk AI, Synapse Query) by [Yash Brahmankar](https://github.com/loisekk).

| Library | Purpose |
|---------|---------|
| [Sigma.js](https://www.sigmajs.org/) | WebGL graph rendering |
| [Graphology](https://graphology.github.io/) | Graph data structures + algorithms |
| [LangChain](https://www.langchain.com/) | AI agent framework |
| [React](https://react.dev/) | UI framework |
| [Tailwind CSS](https://tailwindcss.com/) | Styling |
| [Vite](https://vitejs.dev/) | Build tool |
| [Tree-sitter](https://tree-sitter.github.io/) | AST parsing (via GitNexus) |
