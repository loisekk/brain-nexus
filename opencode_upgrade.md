# OpenCode Upgrade Guide - Full Migration

## All MCP Servers (16 total)

| MCP | Type | Package/URL |
|-----|------|-------------|
| **magic** | local | `npx @21st-dev/magic@latest` |
| **supabase** | remote | `https://mcp.supabase.com/mcp?project_ref=hojbpxkrwjeiksxsirqi` |
| **github** | remote | `https://api.githubcopilot.com/mcp/` |
| **context7** | remote | `https://mcp.context7.com/mcp` |
| **vercel** | remote | `https://mcp.vercel.com` |
| **render** | remote | `https://mcp.render.com/mcp` |
| **netlify** | local | `npx @netlify/mcp` |
| **threejs-devtools** | local | `npx threejs-devtools-mcp` |
| **chrome-devtools** | local | `npx chrome-devtools-mcp@latest` |
| **n8n** | remote | `http://localhost:5678/mcp/6418e0de-3f3e-4d5c-81ae-f12ff3174110` (local) |
| **kaggle** | local | `npx @iflow-mcp/dishant27-kaggle-mcp` |
| **huggingface** | local | `npx huggingface-mcp-server` |
| **playwright** | local | `npx @playwright/mcp@latest` |
| **sequential-thinking** | local | `npx @modelcontextprotocol/server-sequential-thinking` |
| **n8nworkflows-docs** | remote | `https://gitmcp.io/nusquama/n8nworkflows.xyz` |
| **openspace** | local | `openspace-mcp` |
| **obsidian** | remote | `http://127.0.0.1:27200/mcp` (local) |

---

## Custom Skills (.config/opencode/skills/) - 36 skills

bb-methodology, brandkit, brutalist-skill, bug-bounty, cicd-security, credential-attack, gpt-tasteskill, graphify, graphql-audit, gsap-core, gsap-frameworks, gsap-performance, gsap-plugins, gsap-react, gsap-scrolltrigger, gsap-timeline, gsap-utils, image-to-code-skill, imagegen-frontend-mobile, imagegen-frontend-web, meme-coin-audit, minimalist-skill, mobile-pentest, n8n-workflow, output-skill, redesign-skill, report-writing, security-arsenal, soft-skill, stitch-skill, taste-skill, taste-skill-v1, triage-validation, web2-recon, web2-vuln-classes, web3-audit

---

## Claude Skills (.claude/skills/) - 50 skills

agent-reach, agenttrace-session-audit, api-endpoint-builder, ask-matt, ax-extract-workflow, brooks-lint, browser-use, bug-hunter, caveman, codebase-audit-pre-push, codebase-design, codex-review, delegate-task, diagnosing-bugs, domain-modeling, ecl-harness-engineer, git-guardrails-claude-code, global-chat-agent-discovery, grill-me, grill-me-codex, grill-with-docs, grill-with-docs-codex, grilling, handoff, hono, implement, improve-codebase-architecture, jq, logic-lens, migrate-to-shoehorn, performance-optimizer, prototype, python-pptx-generator, rayden-code, resolving-merge-conflicts, scaffold-exercises, setup-matt-pocock-skills, setup-pre-commit, skill-check, skill-discovery, squirrel, tdd, teach, technical-change-tracker, tmux, to-issues, to-prd, triage, ui-ux-pro-max, watch, writing-great-skills

---

## Agent Skills (.agents/skills/) - 36 skills

agent-reach, ask-matt, codebase-design, codex-review, context7-mcp, diagnosing-bugs, domain-modeling, git-guardrails-claude-code, grill-me, grill-me-codex, grill-with-docs, grill-with-docs-codex, grilling, handoff, implement, improve-codebase-architecture, migrate-to-shoehorn, prototype, resolving-merge-conflicts, scaffold-exercises, setup-matt-pocock-skills, setup-pre-commit, tdd, teach, to-issues, to-prd, triage, understand, understand-chat, understand-dashboard, understand-diff, understand-domain, understand-explain, understand-knowledge, understand-onboard, writing-great-skills

---

## Plugins

| Plugin | Location |
|--------|----------|
| `crg-plugin.ts` | `.config/opencode/plugins/` |
| `evolver.js` | `.opencode/plugins/` |
| `graphify.js` | `.opencode/plugins/` |

---

## Complete Installation Commands

### Step 1: Install Node.js dependencies
```bash
npm install -g @21st-dev/magic@latest @netlify/mcp chrome-devtools-mcp@latest @playwright/mcp@latest @modelcontextprotocol/server-sequential-thinking threejs-devtools-mcp @iflow-mcp/dishant27-kaggle-mcp huggingface-mcp-server openspace-mcp @opencode-ai/plugin
```

### Step 2: Install opencode
```bash
npm install -g opencode
```

### Step 3: Clone your second-brain repo
```bash
git clone https://github.com/YOUR_USERNAME/opencode-second-brain.git
```

### Step 4: Create directory structure
```bash
mkdir -p ~/.config/opencode/skills
mkdir -p ~/.config/opencode/plugins
mkdir -p ~/.config/opencode/agents
mkdir -p ~/.config/opencode/commands
mkdir -p ~/.opencode/plugins
mkdir -p ~/.opencode/bin
mkdir -p ~/.claude/skills
mkdir -p ~/.agents/skills
```

### Step 5: Copy config files
```bash
# Main config
cp opencode.jsonc ~/.config/opencode/

# Secondary config
cp config.json ~/.config/opencode/

# Plugins
cp crg-plugin.ts ~/.config/opencode/plugins/
cp evolver.js ~/.opencode/plugins/
cp graphify.js ~/.opencode/plugins/

# AGENTS.md
cp AGENTS.md ~/.config/opencode/
```

### Step 6: Copy all skills
```bash
# Custom skills
cp -r .config/opencode/skills/* ~/.config/opencode/skills/

# Claude skills
cp -r .claude/skills/* ~/.claude/skills/

# Agent skills
cp -r .agents/skills/* ~/.agents/skills/
```

---

## Re-Authentication Required

You need to re-generate these tokens on the new device:

| Service | Where to get token |
|---------|-------------------|
| **GitHub PAT** | https://github.com/settings/tokens |
| **Supabase** | Update `project_ref` in opencode.jsonc |
| **Context7** | https://context7.com |
| **Render** | https://dashboard.render.com/account |
| **Netlify** | https://app.netlify.com/user/applications#personal-access-tokens |
| **Kaggle** | Set `KAGGLE_USERNAME` and `KAGGLE_KEY` env vars |
| **HuggingFace** | Set `HUGGINGFACE_API_KEY` env var |
| **Obsidian** | Requires local Obsidian running on port 27200 |
| **N8N** | Requires local N8N instance running on port 5678 |

---

## Quick One-Liner (copy entire config)

```bash
# Run on new device after cloning repo:
cd opencode-second-brain && \
mkdir -p ~/.config/opencode/{skills,plugins,agents,commands} ~/.opencode/{plugins,bin} ~/.claude/skills ~/.agents/skills && \
cp .config/opencode/opencode.jsonc ~/.config/opencode/ && \
cp .config/opencode/config.json ~/.config/opencode/ && \
cp .config/opencode/AGENTS.md ~/.config/opencode/ && \
cp .config/opencode/plugins/crg-plugin.ts ~/.config/opencode/plugins/ && \
cp .opencode/plugins/evolver.js ~/.opencode/plugins/ && \
cp .opencode/plugins/graphify.js ~/.opencode/plugins/ && \
cp -r .config/opencode/skills/* ~/.config/opencode/skills/ && \
cp -r .claude/skills/* ~/.claude/skills/ && \
cp -r .agents/skills/* ~/.agents/skills/
```
