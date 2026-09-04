/**
 * Adapts our Second Brain knowledge-graph.json format to GitNexus's
 * KnowledgeGraph format so the Sigma.js visualizer can render it.
 *
 * Our format: { id, label, type, project, source_file, degree, _source }
 * GitNexus:   { id, label: NodeLabel, properties: NodeProperties }
 *
 * Edges:
 * Our: { source, target, relation, confidence, _source }
 * GN:  { id, sourceId, targetId, type: RelationshipType, confidence, reason }
 */

import type { GraphNode, GraphRelationship, NodeLabel, RelationshipType } from 'gitnexus-shared';
import { createKnowledgeGraph } from '../core/graph/graph';
import type { KnowledgeGraph } from '../core/graph/types';

interface OurNode {
  id: string;
  label?: string;
  type?: string;
  project?: string;
  source_file?: string;
  degree?: number;
  _source?: string;
  community?: string;
  description?: string;
  filePath?: string;
  name?: string;
}

interface OurEdge {
  source: string;
  target: string;
  relation?: string;
  confidence?: string;
  _source?: string;
}

interface OurGraph {
  nodes: OurNode[];
  edges: OurEdge[];
  metadata?: Record<string, unknown>;
}

function guessNodeType(type?: string, label?: string): string {
  const t = (type || label || 'CodeElement').toLowerCase();
  const map: Record<string, string> = {
    project: 'Project',
    file: 'File',
    function: 'Function',
    class: 'Class',
    method: 'Method',
    variable: 'Variable',
    import: 'Import',
    parameter: 'Variable',
    interface: 'Interface',
    code: 'CodeElement',
    enum: 'Enum',
    decorator: 'Decorator',
    keyword: 'CodeElement',
    concept: 'CodeElement',
    memory: 'CodeElement',
    session: 'CodeElement',
    skill: 'CodeElement',
    conversation: 'Process',
    'claude-message': 'Process',
    'claude-conversation': 'Process',
    rationale: 'CodeElement',
    file_reference: 'File',
    function_reference: 'Function',
    external_module: 'Module',
    project_node: 'Project',
    folder: 'Folder',
    module: 'Module',
    package: 'Package',
    type: 'Type',
    struct: 'Struct',
    trait: 'Trait',
    impl: 'Impl',
    const: 'Const',
    static: 'Static',
    namespace: 'Namespace',
    macro: 'Macro',
    property: 'Property',
    record: 'Record',
    delegate: 'Delegate',
    annotation: 'Annotation',
    constructor: 'Constructor',
    template: 'Template',
    route: 'Route',
    tool: 'Tool',
    section: 'Section',
  };
  return map[t] || 'CodeElement';
}

function guessEdgeType(relation?: string): string {
  const r = (relation || 'USES').toUpperCase();
  const map: Record<string, RelationshipType> = {
    DEFINES: 'DEFINES',
    REFERENCES: 'USES',
    HAS: 'CONTAINS',
    CONTAINS: 'CONTAINS',
    NEXT_MESSAGE: 'CONTAINS',
    IMPORTS: 'IMPORTS',
    HAS_MESSAGE: 'CONTAINS',
    DISCUSSES: 'USES',
    CALLS: 'CALLS',
    INHERITS: 'EXTENDS',
    IMPLEMENTS: 'IMPLEMENTS',
    IMPORTS_FROM: 'IMPORTS',
    USES: 'USES',
    METHOD: 'HAS_METHOD',
    EXTENDS: 'EXTENDS',
    MEMBER_OF: 'MEMBER_OF',
    DECORATES: 'DECORATES',
    HANDLES_ROUTE: 'HANDLES_ROUTE',
    FETCHES: 'FETCHES',
    HANDLES_TOOL: 'HANDLES_TOOL',
    WRAPS: 'WRAPS',
    QUERIES: 'QUERIES',
    ENTRY_POINT_OF: 'ENTRY_POINT_OF',
    ACCESSES: 'ACCESSES',
  };
  return map[r] || 'USES';
}

let edgeIdCounter = 0;

function toGraphNode(node: OurNode): GraphNode {
  const nodeType = guessNodeType(node.type, node.label) as NodeLabel;
  return {
    id: node.id,
    label: nodeType,
    properties: {
      name: node.label || node.name || node.id.split('/').pop()?.split('.').shift() || node.id,
      filePath: node.source_file || node.filePath || '',
      ...(node.project ? { project: node.project } : {}),
      ...(node.degree !== undefined ? { degree: node.degree } : {}),
      ...(node.description ? { description: node.description } : {}),
      ...(node.community ? { community: node.community } : {}),
    },
  };
}

function toGraphRelationship(edge: OurEdge): GraphRelationship {
  const relType = guessEdgeType(edge.relation) as RelationshipType;
  edgeIdCounter++;
  return {
    id: `rel_${edgeIdCounter}`,
    sourceId: edge.source,
    targetId: edge.target,
    type: relType,
    confidence: edge.confidence === 'EXTRACTED' ? 1.0 : edge.confidence === 'INFERRED' ? 0.7 : 0.9,
    reason: edge.relation || relType,
  };
}

export function convertOurGraphToKnowledgeGraph(data: OurGraph): KnowledgeGraph {
  const kg = createKnowledgeGraph();

  for (const node of data.nodes) {
    kg.addNode(toGraphNode(node));
  }

  for (const edge of data.edges) {
    kg.addRelationship(toGraphRelationship(edge));
  }

  return kg;
}

export async function fetchOurGraph(url: string): Promise<KnowledgeGraph> {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`Failed to load graph: ${response.status} ${response.statusText}`);
  const data: OurGraph = await response.json();
  console.log(`Loaded ${data.nodes.length} nodes, ${data.edges.length} edges from ${url}`);
  return convertOurGraphToKnowledgeGraph(data);
}
