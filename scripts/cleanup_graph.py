import json, os

fn = 'galaxy/graph-data.json'
with open(fn, encoding='utf-8') as f: g = json.load(f)

bad_ids = {n['id'] for n in g['nodes'] if n.get('type') == 'skill' and n.get('label') == '---'}
print(f'Bad nodes to remove ({len(bad_ids)}): {bad_ids}')

old_nodes = len(g['nodes'])
g['nodes'] = [n for n in g['nodes'] if n['id'] not in bad_ids]

old_edges = len(g['edges'])
g['edges'] = [e for e in g['edges'] if e['source'] not in bad_ids and e['target'] not in bad_ids]

print(f'Removed {old_nodes - len(g["nodes"])} nodes, {old_edges - len(g["edges"])} edges')
print(f'Final: {len(g["nodes"])} nodes, {len(g["edges"])} edges')

skill_ids = {n['id'] for n in g['nodes'] if n.get('type') == 'skill'}
for n in g['nodes']:
    if n['id'] in skill_ids:
        n['degree'] = sum(1 for e in g['edges'] if e['source'] == n['id'] or e['target'] == n['id'])

for path in ['galaxy/graph-data.json', 'galaxy-react/public/graph-data.json', 'public/knowledge-graph.json']:
    d = os.path.dirname(path)
    if d: os.makedirs(d, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(g, f, ensure_ascii=False, indent=2)
    print(f'[OK] {path}')

types = {}
for n in g['nodes']:
    t = n.get('type', 'unknown')
    types[t] = types.get(t, 0) + 1
print(f'Skill nodes after cleanup: {types.get("skill", 0)}')
print(f'File size: {os.path.getsize(path) / (1024*1024):.1f} MB')
