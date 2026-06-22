# brain-nexus — ROADMAP

> Goal: Beat GitNexus. Build the definitive knowledge graph engine — 76K+ nodes, 67 repos, custom AI, and a backend that smokes theirs.

---

## Architecture

```
Frontend (brain-nexus)          Backend (FastAPI)           Database
┌─────────────────────┐      ┌──────────────────┐      ┌──────────────┐
│ Sigma.js + React 19 │─────▶│ /api/chat        │─────▶│ Neo4j        │
│ ⌘K Search           │      │ /api/synapse     │      │ 76,539 nodes │
│ 3 Layout Modes      │      │ /api/search      │      │ 269,962 edges│
│ File Tree           │      │ /api/node/:id    │      │ Full-text idx│
│ Synapse Query FAB   │      │ /api/embed       │      │ Vector index │
│ Loisekk AI Chat     │─────▶│ Loisekk Agent    │      └──────────────┘
└─────────────────────┘      └──────────────────┘
```

---

## Data Sources (76,539 total nodes)

| Source | Nodes | Content |
|--------|-------|---------|
| **GitNexus** (reused) | 45,077 | Code structure — functions, classes, imports, call graphs, file hierarchies from 67 Desktop repos |
| **Galaxy** (yours) | 28,943 | Project metadata, file relationships, concepts, keywords, project hierarchies |
| **Graphify** (yours) | 2,519 | Conversations, memories, session context, development rationale |

---

## Phase 1 — Frontend Cleanup

### 1.1 Fix GitNexus Branding → brain-nexus / Loisekk AI

| Current | Replace With | Files |
|---------|-------------|-------|
| "GitNexus" logo/name | "brain-nexus" branding | Header.tsx, App.tsx, index.html |
| "Nexus AI" chat button | "Loisekk AI" chat button | Header.tsx, RightPanel.tsx, locales/en/*.json |
| "GitNexus" favicon | Custom brain-nexus favicon | public/favicon.ico |
| Purple brain icon | Custom Loisekk brain icon | Header.tsx |
| Powered by GitNexus | Already added ✓ | StatusBar.tsx |

### 1.2 Fix Connection Errors

| Issue | Fix | Files |
|-------|-----|-------|
| "Server connection lost" bar | Disable heartbeat SSE in local mode | App.tsx |
| "Failed - Retry" button | Hide when no backend configured | Header.tsx |
| DropZone onboarding | Auto-load `/knowledge-graph.json` on startup | App.tsx |

### 1.3 Rename Cypher → Synapse Query

| Current | Replace With | Files |
|---------|-------------|-------|
| "Cypher Query" | "Synapse Query" | QueryFAB.tsx, locales |
| Cypher examples | Synapse examples | QueryFAB.tsx |
| "MATCH ... RETURN" | Keep syntax, rename branding | QueryFAB.tsx |

### 1.4 English Only

| Action | Files |
|--------|-------|
| Delete zh-CN locale files | `src/locales/zh-CN/*` |
| Remove language switcher from header | Header.tsx, LanguageSwitcher.tsx |
| Remove i18n detection | i18n/index.ts |

---

## Phase 2 — Backend (FastAPI)

### 2.1 Scaffold

```
backend/
├── requirements.txt          # fastapi, uvicorn, neo4j, langchain, langgraph, sentence-transformers
├── main.py                   # FastAPI app, CORS, routes
├── config.py                 # Neo4j connection, env vars
├── routes/
│   ├── chat.py               # POST /api/chat (Loisekk AI agent)
│   ├── synapse.py            # POST /api/synapse (Synapse Query execution)
│   ├── search.py             # GET /api/search?q= (semantic search)
│   ├── node.py               # GET /api/node/:id (node details)
│   └── stats.py              # GET /api/stats (graph statistics)
├── agent/
│   ├── loisekk_agent.py      # LangChain agent definition
│   ├── tools.py              # Custom tools: synapse_query, search, get_node, find_path
│   ├── prompt.py             # System prompt builder with all 67 project context
│   └── memory.py             # Conversation history + graph context persistence
├── db/
│   ├── neo4j_client.py       # Neo4j connection handler
│   ├── import_graph.py       # Import knowledge-graph.json → Neo4j
│   └── embeddings.py         # Generate vector embeddings for all nodes
└── utils/
    └── graph_loader.py       # Parse knowledge-graph.json
```

### 2.2 Neo4j Import

```python
# Import all 76K nodes + 270K edges from knowledge-graph.json
# Create indexes: node type, project, full-text search
# Create constraints: unique node IDs
```

### 2.3 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/chat` | POST | Loisekk AI streaming chat (SSE) |
| `/api/synapse` | POST | Execute Synapse Query |
| `/api/search?q=` | GET | Semantic search across all nodes |
| `/api/node/:id` | GET | Full node metadata + neighbors |
| `/api/stats` | GET | Graph statistics |
| `/api/projects` | GET | List all 67 projects with stats |

---

## Phase 3 — Loisekk AI Agent

### 3.1 Agent Architecture

```
User Message → Loisekk Agent → LLM (OpenAI/Gemini/Anthropic/DeepSeek)
                    │
                    ├── System Prompt (built with all 67 project context)
                    │
                    ├── Tools
                    │   ├── synapse_query  → Neo4j (graph queries)
                    │   ├── semantic_search → Vector DB
                    │   ├── get_node       → Neo4j (node details)
                    │   ├── find_path      → Neo4j (BFS/DFS traversal)
                    │   ├── list_projects  → Neo4j
                    │   └── project_overview → Neo4j (aggregated stats)
                    │
                    └── Memory
                        ├── Conversation history
                        └── Graph context cache
```

### 3.2 System Prompt

```
You are Loisekk AI, the knowledge graph assistant for brain-nexus.

You have access to a unified knowledge graph with:
- 76,539 nodes across 67 projects
- 269,962 edges representing code relationships

Your three data sources:
1. Code Intelligence (GitNexus) — 45,077 nodes
   - Full AST analysis: functions, classes, methods, imports, call graphs
   - File hierarchies and directory structures
   - Cross-file relationships (imports, calls, defines)

2. Project Graph (Galaxy) — 28,943 nodes
   - Project-level metadata: names, descriptions, keywords, concepts
   - File-level relationships: dependencies, groupings
   - Cross-project connections and patterns

3. Session Context (Graphify) — 2,519 nodes
   - Development history: decisions, changes, rationale
   - Session logs: conversations, memories, learned patterns
   - Claude interaction history and knowledge base

You can answer questions about:
- "Which projects use FastAPI?"
- "Show me all ML projects and their dependencies"
- "What functions call pandas.read_csv?"
- "Show the architecture of the aethera project"
- "What's the most complex project in my codebase?"
- "Find connections between worldmonitor and opencode-second-brain"
```

### 3.3 Tools Implementation

```python
# Synapse Query tool — execute graph queries
def synapse_query(query: str) -> dict:
    """Run a Synapse Query (graph query) against the knowledge graph.
    Similar to Cypher/GraphQL. Use for structured graph exploration."""
    return neo4j.run(query)

# Semantic search tool
def semantic_search(query: str, top_k: int = 10) -> list:
    """Search all 76K nodes by meaning, not just name.
    Returns most relevant nodes with scores."""
    embedding = embed_model.encode(query)
    return vector_search(embedding, top_k)

# Node details tool
def get_node(node_id: str) -> dict:
    """Get full details about a node: name, type, project,
    properties, relationships, neighbors."""
    return neo4j.get_node_with_neighbors(node_id)

# Path finding tool
def find_path(source: str, target: str, max_depth: int = 5) -> list:
    """Find all paths between two nodes in the knowledge graph.
    Returns shortest paths first."""
    return neo4j.find_paths(source, target, max_depth)
```

### 3.4 Why Loisekk AI Beats Nexus AI

| Feature | Nexus AI (GitNexus) | Loisekk AI |
|---------|--------------------|------------|
| Data scope | 1 repo at a time | All 67 repos simultaneously |
| Knowledge types | Code only | Code + metadata + session history |
| Memory | Per-session | Persistent, cross-session |
| Embeddings | Built per-request | Pre-computed for all 76K nodes |
| Cross-project | No | Yes — cross-project path finding |
| System prompt | Generic codebase | Custom with all 67 project context |
| Max nodes | 50K (chat-only cutoff) | Full 76K always available |

---

## Phase 4 — Embeddings & Vector Search

### 4.1 Generate Embeddings

```python
# Using sentence-transformers
model = SentenceTransformer('all-MiniLM-L6-v2')

for node in all_nodes:
    # Combine: name + type + project + description
    text = f"{node.name} ({node.type}) in {node.project}"
    if node.description:
        text += f": {node.description}"

    embedding = model.encode(text)
    store_embedding(node.id, embedding)
```

### 4.2 Vector Index in Neo4j

```cypher
CREATE VECTOR INDEX node_embeddings
FOR (n:Node)
ON n.embedding
OPTIONS {indexConfig: {
    `vector.dimensions`: 384,
    `vector.similarity_function`: 'cosine'
}}
```

---

## Phase 5 — Polish & Ship

- [ ] Remove all remaining GitNexus references
- [ ] Add 67 project cards/project selector
- [ ] Synapse Query syntax highlighting + autocomplete
- [ ] Mobile responsive
- [ ] Vercel deployment
- [ ] GitHub Actions CI/CD
- [ ] API documentation (Swagger via FastAPI)

---

## Timeline

| Phase | Est. Time | Status |
|-------|-----------|--------|
| Phase 1: Frontend Cleanup | 2-3 hours | ✅ Complete |
| Phase 2: FastAPI Backend | 3-4 hours | 🔜 Pending |
| Phase 3: Loisekk AI Agent | 4-5 hours | 🔜 Pending |
| Phase 4: Embeddings | 2-3 hours | 🔜 Pending |
| Phase 5: Polish & Ship | 2-3 hours | 🔜 Pending |
| **Total** | **13-18 hours** | |

---

## Key Decisions

- **Database**: Neo4j (native graph DB, Cypher/Synapse compatible, vector search via apoc)
- **Backend**: FastAPI (async Python, best performance for AI workloads)
- **AI Framework**: LangChain + LangGraph (reuses GitNexus infra, custom tools)
- **Embeddings**: sentence-transformers all-MiniLM-L6-v2 (lightweight, good quality)
- **Rendering**: Sigma.js + graphology (keep GitNexus WebGL renderer — it's the best part)
- **Query Language**: "Synapse Query" (rebranded Cypher — same syntax, our branding)

---

## Credits

Visualizer engine built on [GitNexus](https://github.com/abhigyanpatwari/GitNexus) by Abhigyan Patwari.