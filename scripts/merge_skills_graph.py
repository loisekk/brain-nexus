"""Merge 54 opencode skills into galaxy graph-data.json with Obsidian-style Smart Connections."""
import json, re, os, math
from collections import Counter
from pathlib import Path

SKILLS_META = Path("skills-metadata-compiled.json")
GALAXY_GRAPH = Path("galaxy/graph-data.json")
GALAXY_REACT_GRAPH = Path("galaxy-react/public/graph-data.json")
PUBLIC_GRAPH = Path("public/knowledge-graph.json")
OUT_GRAPH = Path("galaxy/graph-data.json")

with open(SKILLS_META) as f: skills = json.load(f)
with open(GALAXY_GRAPH) as f: graph = json.load(f)

existing_ids = {n["id"] for n in graph["nodes"]}
existing_edge_set = set()
for e in graph["edges"]:
    existing_edge_set.add((e["source"], e["target"], e.get("relation","")))

registry = {}
new_nodes = []
new_edges = {}

def tokenise(text: str) -> set[str]:
    words = re.findall(r"[a-zA-Z][a-z0-9]{2,}", text.lower())
    stopwords = {"the","and","for","with","from","this","that","use","using","used","when","can","are","not","all","its","their","them","these","those","such","each","also","but","has","had","have","been","being","both","each","more","most","other","some","into","over","than","very","just","about","should","would","could","after","before","between","through","during","without","within","across","among","under","above","part","create","creating","built","build","based","need","needs","needed","support","supports","supported","including","includes","include","like","well","much","many","still","even","way","ways","using","used","also","already"}
    return {w for w in words if w not in stopwords and len(w) > 2}

def name_tokens(text: str) -> set[str]:
    parts = re.split(r"[-_\s/]+", text.lower())
    return {p for p in parts if len(p) > 1}

CONFIDENCE_HIGH = "HIGH"
CONFIDENCE_MEDIUM = "MEDIUM"

# build skill nodes
skill_keywords = {}
for s in skills:
    raw_sid = f"skill__{s['category'].lower()}__{s['name']}"
    raw_sid = re.sub(r"[^a-z0-9_]", "_", raw_sid)
    raw_sid = re.sub(r"_+", "_", raw_sid).strip("_")

    sid = raw_sid
    if sid in existing_ids:
        n = 2
        while f"{raw_sid}_{n}" in existing_ids: n += 1
        sid = f"{raw_sid}_{n}"

    existing_ids.add(sid)
    registry[sid] = s
    label = s["name"].replace("-", " ").replace("_", " ").title()
    cat = s["category"]

    node = {
        "id": sid,
        "label": label,
        "type": "skill",
        "project": f"opencode-{cat.lower()}",
        "source_file": s["path"],
        "degree": 0,
        "description": s["description"],
        "triggers": ", ".join(s.get("triggers", [])),
        "tags": ", ".join(s.get("tags", [])),
    }
    new_nodes.append(node)

    kw = tokenise(s["description"])
    for t in s.get("triggers", []): kw |= tokenise(t)
    for t in s.get("tags", []): kw |= tokenise(t)
    kw |= name_tokens(s["name"])
    kw.add(cat.lower().replace("-", ""))
    skill_keywords[sid] = kw

print(f"[OK] Created {len(new_nodes)} skill nodes")

# build text index for existing nodes
node_text_index = {}
for n in graph["nodes"]:
    text = f"{n.get('label','')} {n.get('type','')} {n.get('project','')} {n.get('source_file','')} {n.get('description','')}"
    node_text_index[n["id"]] = tokenise(text)

match_high = 0
match_medium = 0

for sid, skill_kw in skill_keywords.items():
    scored = []
    for nid, node_kw in node_text_index.items():
        overlap = skill_kw & node_kw
        if not overlap: continue
        union = skill_kw | node_kw
        jaccard = len(overlap) / len(union) if union else 0
        if jaccard < 0.03: continue
        scored.append((nid, jaccard, list(overlap)[:8]))

    scored.sort(key=lambda x: -x[1])
    high = [(nid, j, ov) for nid, j, ov in scored if j >= 0.15]
    medium = [(nid, j, ov) for nid, j, ov in scored if 0.05 <= j < 0.15]

    created = 0
    for nid, j, ov in high[:6]:
        ekey = (sid, nid, "teaches")
        if ekey not in existing_edge_set:
            key = f"{sid}->{nid} teaches"
            new_edges[key] = {
                "source": sid, "target": nid, "relation": "teaches",
                "confidence": CONFIDENCE_HIGH, "score": round(j, 3),
                "match_terms": ov
            }
            match_high += 1
            created += 1

    for nid, j, ov in medium[:10]:
        if created >= 14: break
        ekey = (sid, nid, "relates_to")
        if ekey not in existing_edge_set:
            key = f"{sid}->{nid} relates_to"
            new_edges[key] = {
                "source": sid, "target": nid, "relation": "relates_to",
                "confidence": CONFIDENCE_MEDIUM, "score": round(j, 3),
                "match_terms": ov
            }
            match_medium += 1
            created += 1

print(f"[OK] Smart Connections: {match_high} high + {match_medium} medium edges")

# inter-skill connections
inter_count = 0
registries = list(registry.items())
for i, (sid_a, s_a) in enumerate(registries):
    for sid_b, s_b in registries[i+1:]:
        ekey = (sid_a, sid_b, "same_category")
        if ekey not in existing_edge_set and s_a["category"] == s_b["category"]:
            key = f"{sid_a}->{sid_b} sibling_skill"
            new_edges[key] = {
                "source": sid_a, "target": sid_b, "relation": "sibling_skill",
                "confidence": CONFIDENCE_HIGH, "score": 0.8,
                "match_terms": [s_a["category"]]
            }
            inter_count += 1

        kw_a = skill_keywords[sid_a]
        kw_b = skill_keywords[sid_b]
        overlap = kw_a & kw_b
        if len(overlap) >= 3:
            j = len(overlap) / len(kw_a | kw_b)
            if j > 0.1:
                ekey = (sid_a, sid_b, "complements")
                if ekey not in existing_edge_set:
                    key = f"{sid_a}->{sid_b} complements"
                    new_edges[key] = {
                        "source": sid_a, "target": sid_b, "relation": "complements",
                        "confidence": CONFIDENCE_MEDIUM, "score": round(j, 3),
                        "match_terms": list(overlap)[:5]
                    }
                    inter_count += 1

print(f"[OK] Inter-skill connections: {inter_count}")

# merge
graph["nodes"].extend(new_nodes)
for v in new_edges.values():
    graph["edges"].append(v)

# update skill node degrees
skill_node_ids = {n["id"] for n in new_nodes}
for n in graph["nodes"]:
    if n["id"] in skill_node_ids:
        n["degree"] = sum(1 for e in graph["edges"]
                         if e["source"] == n["id"] or e["target"] == n["id"])

print(f"\n-- Merge Complete --")
print(f"Total nodes: {len(graph['nodes'])}")
print(f"Total edges: {len(graph['edges'])}")
print(f"Skills added: {len(new_nodes)}")
print(f"Edges added: {len(new_edges)}")

# save
with open(OUT_GRAPH, "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
print(f"[OK] Saved: {OUT_GRAPH}")

if GALAXY_REACT_GRAPH.parent.exists():
    with open(GALAXY_REACT_GRAPH, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)
    print(f"[OK] Saved: {GALAXY_REACT_GRAPH}")

PUBLIC_GRAPH.parent.mkdir(parents=True, exist_ok=True)
with open(PUBLIC_GRAPH, "w", encoding="utf-8") as f:
    json.dump(graph, f, ensure_ascii=False, indent=2)
print(f"[OK] Saved: {PUBLIC_GRAPH}")

# stats
types = Counter(n["type"] for n in graph["nodes"])
print(f"\n-- Graph Summary --")
print(f"Node types: {dict(types.most_common())}")
projects = Counter(n.get("project", "unknown") for n in graph["nodes"])
print(f"Projects: {len(projects)}")
file_size = os.path.getsize(OUT_GRAPH) / (1024*1024)
print(f"File size: {file_size:.1f} MB")
