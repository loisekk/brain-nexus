import { Database, Connection } from "C:/Users/yashb/AppData/Roaming/npm/node_modules/gitnexus/node_modules/@ladybugdb/core/index.mjs";
import { readFileSync, writeFileSync, existsSync } from "fs";
import { join } from "path";

const DESKTOP = "C:/Users/yashb/OneDrive/Desktop";
const MAX_DB_SIZE = 16n * 1024n ** 3n; // 16 GiB

// All node tables from GitNexus schema
const NODE_TABLES = [
  "File", "Folder", "Function", "Class", "Interface", "Method", "CodeElement",
  "Community", "Process", "Section", "Route", "Tool", "BasicBlock",
  "Struct", "Enum", "Macro", "Typedef", "Union", "Namespace", "Trait",
  "Impl", "TypeAlias", "Const", "Static", "Variable", "Record",
  "Delegate", "Annotation", "Constructor", "Template", "Module", "Property"
];

const REL_QUERY = `MATCH (a)-[r:CodeRelation]->(b) RETURN a.id AS sourceId, b.id AS targetId, r.type AS type, r.confidence AS confidence, r.reason AS reason, r.step AS step`;

async function openDb(lbugPath) {
  if (!existsSync(lbugPath)) return null;
  const db = new Database(lbugPath, 0n, false, true, MAX_DB_SIZE, true, 67108864n, false, true);
  const conn = new Connection(db);
  return { db, conn };
}

async function queryNodes(conn, table) {
  const label = `\`${table}\``;
  const cypher = `MATCH (n:${label}) RETURN n.id AS id, n.name AS name, n.filePath AS filePath, n.startLine AS startLine, n.endLine AS endLine, n.label AS label, n.heuristicLabel AS heuristicLabel, n.content AS content, n.description AS description`;
  try {
    const stmt = await conn.prepare(cypher);
    const result = await conn.execute(stmt, {});
    const rows = [];
    while (await result.hasNext()) {
      const row = await result.getNext();
      rows.push({
        id: row.id, name: row.name, filePath: row.filePath,
        startLine: row.startLine, endLine: row.endLine,
        label: row.label, heuristicLabel: row.heuristicLabel,
        content: row.content, description: row.description
      });
    }
    return rows;
  } catch {
    return [];
  }
}

async function queryRelationships(conn) {
  try {
    const stmt = await conn.prepare(REL_QUERY);
    const result = await conn.execute(stmt, {});
    const rows = [];
    while (await result.hasNext()) {
      const row = await result.getNext();
      rows.push({
        sourceId: row.sourceId, targetId: row.targetId,
        type: row.type, confidence: row.confidence,
        reason: row.reason, step: row.step
      });
    }
    return rows;
  } catch { return []; }
}

function getRepos() {
  const entries = readFileSync(join(DESKTOP, "opencode-second-brain", ".gitnexus", "registry.json"), "utf-8");
  const registry = JSON.parse(entries);
  return registry.repositories || registry || [];
}

async function main() {
  const repos = [];
  const desktopDirs = (await import("fs")).readdirSync(DESKTOP, { withFileTypes: true })
    .filter(d => d.isDirectory())
    .map(d => d.name);

  for (const dir of desktopDirs) {
    const lbugPath = join(DESKTOP, dir, ".gitnexus", "lbug");
    const metaPath = join(DESKTOP, dir, ".gitnexus", "meta.json");
    if (existsSync(lbugPath) && existsSync(metaPath)) {
      const meta = JSON.parse(readFileSync(metaPath, "utf-8"));
      repos.push({ name: dir, lbugPath, meta: meta.stats || meta });
    }
  }

  let allNodes = [];
  let allEdges = [];
  let totalRepoNodes = 0;

  for (const repo of repos) {
    process.stdout.write(`Extracting ${repo.name}... `);
    const handle = await openDb(repo.lbugPath);
    if (!handle) { console.log("SKIP (no db)"); continue; }
    const { conn } = handle;

    try {
      for (const table of NODE_TABLES) {
        const rows = await queryNodes(conn, table);
        const prefixed = rows.map(r => ({
          ...r,
          id: `${repo.name}::${table}::${r.id}`,
          _repo: repo.name,
          _table: table
        }));
        allNodes.push(...prefixed);
      }
      const edges = await queryRelationships(conn);
      const prefixedEdges = edges.map(e => ({
        ...e,
        sourceId: `${repo.name}::${e.sourceId}`,
        targetId: `${repo.name}::${e.targetId}`,
        _repo: repo.name
      }));
      allEdges.push(...prefixedEdges);
      console.log(`${allNodes.length - totalRepoNodes} nodes, ${prefixedEdges.length} edges`);
      totalRepoNodes = allNodes.length;
    } catch (err) {
      console.log(`ERROR: ${err.message}`);
    } finally {
      try { await conn.close(); } catch {}
      try { await handle.db.close(); } catch {}
    }
  }

  const output = { nodes: allNodes, edges: allEdges, _meta: { repoCount: repos.length } };
  writeFileSync("gitnexus-export.json", JSON.stringify(output));
  console.log(`\nDONE: ${allNodes.length} nodes, ${allEdges.length} edges from ${repos.length} repos`);
}

main().catch(console.error);
