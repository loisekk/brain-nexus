# brain-nexus — Build Plan

> 138,327 nodes | 319,091 edges | 120 projects | 0 broken edges

---

## Phase 1 — Frontend Cleanup + Data Merge ✅ 100%

### 1.1 Branding (40%)
- [x] Header: "brain-nexus" branding
- [x] Chat: "Loisekk AI" button
- [x] StatusBar: "Powered by GitNexus" removed
- [ ] Favicon: Custom brain-nexus icon
- [ ] LanguageSwitcher: Remove from Header
- [ ] locales/zh-CN: Delete Chinese locale
- [ ] i18n detection: Remove auto-detect

### 1.2 Data Merge (100%)
- [x] Galaxy graph: 28,943 nodes (Claude conversations, memories, project metadata)
- [x] Skills: 54 OpenCode skills with Smart Connections (1,030 edges)
- [x] GitNexus: 46,262 nodes from 67 Desktop repos extracted via LadybugDB
- [x] Graphify: 63,122 nodes from 2,023 AST files + 16 semantic files
- [x] All sources merged → galaxy/graph-data.json, public/knowledge-graph.json

### 1.3 Connection Fixes
- [ ] Disable heartbeat SSE in local mode → hide "Server connection lost"
- [ ] Hide "Failed - Retry" button when no backend
- [ ] Auto-load `/knowledge-graph.json` on startup (no DropZone need)

### 1.4 Rename Cypher → Synapse
- [ ] "Cypher Query" → "Synapse Query" in QueryFAB.tsx, locales
- [ ] Cypher examples → Synapse examples

---

## Phase 2 — FastAPI Backend 🔨 IN PROGRESS

### 2.0 Recover Source from .pyc
- [ ] Decompile 15 `.pyc` files → restore original `.py` source
- [ ] Recover: main.py, config.py, routers/*, services/*, database/*
- [ ] Preserve best features: FAISS + graph_store abstraction + LangChain agent pattern

### 2.1 Neo4j Setup
- [ ] Create `docker-compose.yml` (Neo4j 5, ports 7687/7474)
- [ ] Create `backend/requirements.txt`
- [ ] Start Neo4j container, verify connection

### 2.2 Database Layer
- [ ] `database/neo4j_client.py` — driver pool, connection retry, constraints
- [ ] `database/import_graph.py` — batch import 138K nodes + 319K edges
- [ ] `database/embeddings.py` — FAISS vector index (recover from .pyc)
- [ ] `database/graph_store.py` — abstract graph operations (recover from .pyc)
- [ ] Create full-text index on node labels
- [ ] Create vector index for embeddings

### 2.3 API Routes
- [ ] `routers/stats.py` — GET /api/stats (node/edge counts, type breakdown, top projects)
- [ ] `routers/nodes.py` — GET /api/node/:id (node + neighbors + relationships)
- [ ] `routers/search.py` — GET /api/search?q= (hybrid: FAISS vector + Neo4j full-text)
- [ ] `routers/synapse.py` — POST /api/synapse (read-only Cypher proxy)
- [ ] `routers/chat.py` — POST /api/chat (Loisekk AI streaming SSE)

### 2.4 FastAPI App
- [ ] `main.py` — FastAPI app, CORS, mount routers, startup graph check
- [ ] `config.py` — Neo4j URI, credentials, model name, FAISS path
- [ ] `__init__.py`, `utils/graph_loader.py` — Shared JSON parsing

### 2.5 Connect Frontend
- [ ] Update `VITE_BACKEND_URL` to `http://localhost:8000`
- [ ] Test all endpoints end-to-end

---

## Phase 3 — Loisekk AI Agent

### 3.1 Agent Core
- [ ] `services/agent.py` — LangChain agent with Graph RAG tools
- [ ] `services/prompt.py` — System prompt with all 120 project context
- [ ] `services/graph_tools.py` — Neo4j-optimized path finding, neighbor expansion
- [ ] `services/memory.py` — Conversation history + graph context persistence

### 3.2 LLM Integration
- [ ] Support OpenAI, Gemini, Anthropic, DeepSeek providers
- [ ] Streaming via SSE (Server-Sent Events)
- [ ] Token counting + context window management

### 3.3 Agent Tools
- [ ] `synapse_query` — Execute graph queries against Neo4j
- [ ] `semantic_search` — Vector search across all nodes
- [ ] `get_node` — Node detail with all relationships
- [ ] `find_path` — BFS/DFS shortest path between nodes
- [ ] `list_projects` — Project inventory with stats
- [ ] `project_overview` — Aggregated per-project summary

---

## Phase 4 — Embeddings & Vector Search

### 4.1 Generate Embeddings
- [ ] Use `sentence-transformers/all-MiniLM-L6-v2` (384-dim)
- [ ] Encode all 138K nodes: concatenate name + type + project + description
- [ ] Store embeddings in Neo4j vector index
- [ ] Also maintain FAISS index for fast approximate search

### 4.2 Hybrid Search
- [ ] Combine Neo4j full-text (BM25) + FAISS vector (cosine)
- [ ] Rank fusion: reciprocal rank fusion
- [ ] Return top 20 results with scores

### 4.3 Semantic Index
- [ ] Periodic re-index on graph updates
- [ ] Cache warm embeddings in FAISS at startup

---

## Phase 5 — Polish & Ship

### 5.1 Frontend Polish
- [ ] Synapse Query syntax highlighting + autocomplete
- [ ] 120 project cards / project selector
- [ ] Mobile-responsive layout
- [ ] Loading states + error boundaries
- [ ] Dark/light mode toggle

### 5.2 Backend Polish
- [ ] API documentation (Swagger UI at /docs)
- [ ] Rate limiting
- [ ] Request validation (Pydantic)
- [ ] Error handling + logging (structlog)
- [ ] Health check endpoint: GET /api/health

### 5.3 Deployment
- [ ] Vercel deployment for frontend
- [ ] Docker Compose for backend + Neo4j
- [ ] GitHub Actions CI/CD
- [ ] Environment variable documentation
- [ ] README.md with setup instructions

---

## File Tree (target)

```
opencode-second-brain/
├── plan.md                    # This file
├── ROADMAP.md                 # Original roadmap (updated)
├── public/
│   └── knowledge-graph.json   # 138K nodes merged graph (96 MB)
├── galaxy/
│   └── graph-data.json        # Same merged graph
├── galaxy-react/
│   ├── dist/                  # Built frontend
│   └── src/                   # Frontend source (React + Sigma.js)
├── backend/                   # FastAPI backend
│   ├── main.py
│   ├── config.py
│   ├── requirements.txt
│   ├── docker-compose.yml
│   ├── __init__.py
│   ├── _test.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── nodes.py
│   │   ├── search.py
│   │   ├── stats.py
│   │   └── synapse.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── agent.py
│   │   ├── graph_tools.py
│   │   ├── prompt.py
│   │   └── memory.py
│   ├── database/
│   │   ├── __init__.py
│   │   ├── neo4j_client.py
│   │   ├── import_graph.py
│   │   ├── graph_store.py
│   │   └── embeddings.py
│   └── utils/
│       ├── __init__.py
│       └── graph_loader.py
└── scripts/
    ├── merge_skills_graph.py
    └── cleanup_graph.py
```

---

## Key Decisions

| Decision | Choice | Reason |
|----------|--------|--------|
| Database | Neo4j 5 | Native graph DB, Cypher, path-finding, full-text + vector indexes |
| Backend | FastAPI (Python) | Async, best AI/ML ecosystem, LangChain integration |
| AI Framework | LangChain + LangGraph | Reuses GitNexus infra, custom tools |
| Embeddings | sentence-transformers MiniLM-L6-v2 (384-dim) | Lightweight, good quality, fast |
| Vector Index | FAISS + Neo4j vector | FAISS for speed, Neo4j for persistence |
| Frontend | React 19 + Sigma.js + graphology | Reuses brain-nexus renderer |
| Query Language | "Synapse Query" (Cypher) | Same syntax, our branding |

---

## Timeline

| Phase | Status | Est. Time |
|-------|--------|-----------|
| Phase 1: Frontend Cleanup + Data Merge | ✅ 100% | 2-3 hours |
| Phase 2: FastAPI Backend | 🔨 In Progress | 3-4 hours |
| Phase 3: Loisekk AI Agent | 🔜 Pending | 4-5 hours |
| Phase 4: Embeddings & Vector Search | 🔜 Pending | 2-3 hours |
| Phase 5: Polish & Ship | 🔜 Pending | 2-3 hours |