# Agent Skills Research

> Research compiled on 2026-06-28 | For second-brain integration

## Currently Installed

### Matt Pocock Skills (148k ⭐)
- **Repo:** github.com/mattpocock/skills
- **Skills:** grill-me, grill-with-docs, tdd, diagnosing-bugs, triage, improve-codebase-architecture, setup-matt-pocock-skills, to-prd, to-issues, handoff, teach, codebase-design, domain-modeling, prototype, writing-great-skills
- **Status:** ✅ Installed

### Grill-Me-Codex (287 ⭐)
- **Repo:** github.com/chaseai-yt/grill-me-codex
- **Skills:** grill-me-codex, grill-with-docs-codex, codex-review
- **Status:** ✅ Installed

---

## Recommended for Installation

### 🔥 High Priority

#### 1. Superpowers (240k ⭐)
- **Repo:** github.com/obra/superpowers
- **Description:** Agentic skills framework & software development methodology
- **Why:** Most popular skills framework, comprehensive methodology

#### 2. Anthropic Official Skills (156k ⭐)
- **Repo:** github.com/anthropics/skills
- **Description:** Official agent skills from Anthropic
- **Why:** Official, maintained, reliable

#### 3. Agent Skills by Addy Osmani (67k ⭐)
- **Repo:** github.com/addyosmani/agent-skills
- **Description:** Production-grade engineering skills for AI coding agents
- **Why:** Production-ready, engineering-focused

### 🛠️ Useful Tools

#### 4. Caveman (77k ⭐)
- **Repo:** github.com/JuliusBrussee/caveman
- **Description:** Cuts 65% of tokens by talking like caveman
- **Why:** Token efficiency, saves money

#### 5. Last30Days Skill (47k ⭐)
- **Repo:** github.com/mvanhorn/last30days-skill
- **Description:** Research any topic across Reddit, X, YouTube, HN, Polymarket
- **Why:** Real-time research capability

#### 6. Obsidian Skills (39k ⭐)
- **Repo:** github.com/kepano/obsidian-skills
- **Description:** Agent skills for Obsidian CLI
- **Why:** If using Obsidian for second brain

### 🎨 Specialized

#### 7. UI/UX Pro Max (97k ⭐)
- **Repo:** github.com/nextlevelbuilder/ui-ux-pro-max-skill
- **Description:** Design intelligence for UI/UX
- **Why:** For web app development

#### 8. Trail of Bits Skills (5.9k ⭐)
- **Repo:** github.com/trailofbits/skills
- **Description:** Security research, vulnerability detection, audit workflows
- **Why:** Security auditing

#### 9. Scientific Agent Skills (29k ⭐)
- **Repo:** github.com/K-Dense-AI/scientific-agent-skills
- **Description:** 140+ skills for science, biology, chemistry, medicine
- **Why:** If doing research work

### 🌐 Browser Automation

#### 10. Browser-Use (101k ⭐)
- **Repo:** github.com/browser-use/browser-use
- **Description:** AI-powered browser automation — let agents control real browsers
- **Features:** Fill forms, click, navigate, extract data, CLI, cloud version with stealth/proxy
- **Quickstart:** `uv add "browser-use[core]"`
- **Claude Code Skill:** Available in `skills/browser-use/`
- **Why:** Best browser automation for AI agents, handles captchas, proxies, complex web tasks

### 📚 Learning

#### 11. Book to Skill (6.9k ⭐)
- **Repo:** github.com/virgiliojr94/book-to-skill
- **Description:** Turn any technical book PDF into a Claude Code skill
- **Why:** Learn from books interactively

#### 11. Codebase to Course (5k ⭐)
- **Repo:** github.com/zarazhangrui/codebase-to-course
- **Description:** Turn codebase into interactive HTML course
- **Why:** Understand codebases visually

---

## Install Commands

```bash
# Superpowers
git clone https://github.com/obra/superpowers.git "$env:TEMP\superpowers"
Copy-Item -Recurse -Force "$env:TEMP\superpowers\skills\*" "$env:USERPROFILE\.claude\skills\"

# Anthropic Skills
git clone https://github.com/anthropics/skills.git "$env:TEMP\anthropic-skills"
Copy-Item -Recurse -Force "$env:TEMP\anthropic-skills\skills\*" "$env:USERPROFILE\.claude\skills\"

# Agent Skills (Addy Osmani)
git clone https://github.com/addyosmani/agent-skills.git "$env:TEMP\agent-skills"
Copy-Item -Recurse -Force "$env:TEMP\agent-skills\skills\*" "$env:USERPROFILE\.claude\skills\"

# Caveman
git clone https://github.com/JuliusBrussee/caveman.git "$env:TEMP\caveman"
Copy-Item -Recurse -Force "$env:TEMP\caveman\skills\*" "$env:USERPROFILE\.claude\skills\"

# Last30Days
git clone https://github.com/mvanhorn/last30days-skill.git "$env:TEMP\last30days"
Copy-Item -Recurse -Force "$env:TEMP\last30days\skills\*" "$env:USERPROFILE\.claude\skills\"

# Browser-Use
uv add "browser-use[core]"
# Claude Code skill:
mkdir -p ~/.claude/skills/browser-use
curl -o ~/.claude/skills/browser-use/SKILL.md https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

---

## Notes

- All skills go to `~/.claude/skills/` (opencode reads from here)
- Skills are model-agnostic (work with any LLM)
- Some skills need specific tools (e.g., Obsidian skills need Obsidian)
- Token-efficient skills (caveman) save money on API calls
