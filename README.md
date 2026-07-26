# bernardo-skills

A curated collection of Claude skills for development, content creation, agentic workflows, and a few cross-repo tools.

Skills are self-contained instructions that extend Claude's capabilities for specific recurring tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting resources.

---

## Skills

### 🛠️ Dev

| Skill                                                 | Description                                                                                                                                                                                                                                                            |
| ----------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`repo-reconciler`](skills/dev/repo-reconciler/)       | Audits a repository for inconsistencies between code and documentation — detects undocumented features, stale README sections, broken examples, and version drift. Generates ready-to-apply patches.                                                                  |
| [`fitz-agent-auditor`](skills/dev/fitz-agent-auditor/) | Forensic analysis of AI agent outputs using the FITZ taxonomy (SALUDABLE / ALUCINACIÓN / INYECCIÓN / DRIFT). Detects hallucination, prompt injection, and role drift. Produces a verdict, detected signals, and an operational recommendation to prevent recurrence. |
| [`log-turn`](skills/dev/log-turn/)                     | Automatically appends every conversation turn to `sessions/today-LOG.md` in a structured `## Prompt N: <Title>` / `## Response N` format. Always active by default; switches to on-demand mode only if the user explicitly requests it in the current session.   |
| [`karpathy-guidelines`](skills/dev/karpathy-guidelines/) | Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations — surface assumptions, keep changes minimal and surgical, and define verifiable success criteria before looping.                                          |
| [`opus5-optim`](skills/dev/opus5-optim/)               | Applies Anthropic's official Opus 5 prompting guidance on response length — keeps direct answers concise and high-level unless depth is requested, and inserts a `<tone_preference>` reminder near the end of long system prompts.                                |

### ✍️ Content

| Skill                                                                           | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`authorship-validator`](skills/content/authorship-validator/)                   | Validates human authorship of an article before publishing using the VIDAL framework (VIVO / INTERVENIDO / DELEGADO / GHOST). Detects friction signals vs. LLM homogeneity and produces specific rewrite recommendations. Requires personal calibration with your own reference texts.                                                                                                                                                                                                  |
| [`voice-refiner`](skills/content/voice-refiner/)                                 | Iteratively refines an article until it reaches ≥85% human authorship confidence and ≤2 AI-flagged phrases. Operates in autonomous mode (Model A) or author-reviewed mode (Model B). Depends on `authorship-validator`.                                                                                                                                                                                                                                                             |
| [`atlas-slop-ai`](skills/content/atlas-slop-ai/)                                 | Classifies editorial articles in a 2×2 matrix crossing two independent axes — authorship (human vs AI-produced) and substance (own thesis vs slop) — to produce a diagnostic content quality map. Supports digest mode (batch classification with table output) and solo mode (single article). Outputs text/JSON classification or an interactive HTML atlas.                                                                                                                       |
| [`latex-md-roundtrip`](skills/content/latex-md-roundtrip/)                       | Round-trip-safe pipeline for editing a LaTeX paper in Markdown and regenerating the LaTeX target ready for upload (Overleaf / arXiv / journal). Pandoc isn't bijective, so the skill freezes the preamble as a template, curates a baseline MD with raw-LaTeX blocks for constructs Pandoc loses, and generates a check script + per-cycle regen script (canonical templates in `assets/`, paths substituted per project). Output filenames are content-driven, not version-numbered. |
| [`pdf-export`](skills/content/pdf-export/)                                       | Exports Markdown documents to PDF via a verified Pandoc (KaTeX) → Chrome headless pipeline. Handles inline and block LaTeX formulas, YAML frontmatter metadata, custom CSS styling, and multi-file concatenation. No LaTeX installation required.                                                                                                                                                                                                                                    |
| [`word-template-gen`](skills/content/word-template-gen/)                         | Generates Word (.docx) templates and PDF/HTML renders from a theme catalog (JSON). Each theme is the single source of design — fonts, palette, sizes — that simultaneously drives the CSS pipeline and the Word reference-doc, ensuring visual consistency between PDF and Word outputs. Includes themes `academico-brj`, `neutro`, and `moderno`.                                                                                                                                   |
| [`karpathy-llm-wiki`](skills/content/karpathy-wiki/karpathy-llm-wiki/)           | Builds and maintains a personal LLM-powered knowledge base with two directories:`raw/` (immutable sources) and `wiki/` (compiled articles). Supports ingest (fetch → compile → cascade updates), query (search and synthesize), and lint (auto-fix broken links and index inconsistencies). Based on Karpathy's wiki pattern.                                                                                                                                                     |
| [`obsidian-graph-colors`](skills/content/karpathy-wiki/obsidian-graph-colors/)   | Manages color groups in Obsidian's Graph view by reading and writing `graph.json`. Runs an audit script to show current state, detect orphan/missing groups, and flag duplicate hex values. Supports add, change, delete, and bulk color-scheme operations.                                                                                                                                                                                                                           |
| [`obsidian-vault-builder`](skills/content/karpathy-wiki/obsidian-vault-builder/) | Creates and configures a complete Obsidian vault (5 `.obsidian/` JSON files) without opening Obsidian. Supports bootstrap from templates (minimal / full / bayesiano), plugin toggling, layout regeneration via `build_workspace.py`, and vault inspection/audit.                                                                                                                                                                                                                   |

> **karpathy-wiki group** — the three skills above form a layered stack with non-overlapping responsibilities:
>
> | Layer               | Skill                      | When to use                                                          |
> | ------------------- | -------------------------- | -------------------------------------------------------------------- |
> | 1 · Infrastructure | `obsidian-vault-builder` | Create or reconfigure `.obsidian/` (bootstrap, layout, plugin set) |
> | 2 · Content        | `karpathy-llm-wiki`      | Ingest sources, query the wiki, lint broken links and index          |
> | 3 · Visual         | `obsidian-graph-colors`  | Add, change, or audit Graph view color groups in `graph.json`      |
>
> Typical order: `obsidian-vault-builder` → `karpathy-llm-wiki` → `obsidian-graph-colors`. Each skill can also run independently once its layer's prerequisites exist.

**NOTE**: Refer to `skills\content\karpathy-wiki\README.md` for the details

### 🤖 Agentic

| Skill                                                             | Description                                                                                                                                                                                                  |
| ----------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`registro-sesion-claude`](skills/agentic/registro-sesion-claude/) | Captures metrics and scope of a Claude Code session into a structured Markdown file (`USAGE.md` or `sessions/{date}-{slug}.md`). Triggered by phrases like "registra la sesión", "documenta esta sesión", or pasting `/usage` output. |
| [`session-cot`](skills/agentic/cot-session/)                       | Reconstructs the reasoning trace of a complex session as a Chain of Thought document — numbered steps with Input / Reasoning / Key inference, plus recurring reasoning patterns. Triggered by "escribe el CoT", "documenta el razonamiento de la sesión", or at the close of long design/architecture sessions. Not a summary of output — a trace of the thinking process. |
| [`setup-minimax`](skills/agentic/setup-minimax/)                   | Walks a non-technical user through configuring Claude Code to use MiniMax as the model provider — one question at a time, verifies each step, creates the launcher `.bat` and the MCP config for web search. Triggered by "configurar Claude Code con MiniMax", "quiero usar MiniMax", "cambiar a MiniMax-M3". |

### 🧰 Standalone (cross-repo)

These skills don't fit the dev/content/agentic taxonomy — they live directly under `skills/` because they encode conventions for a different repository (`core-human-knowledge`).

| Skill                                | Description                                                                                                                                                                                                                                                                                                                                                                              |
| ------------------------------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`md-guide-builder`](skills/md-guide-builder/) | Produces a practical Markdown guide (`NN-TIPO-tema.md`) in the style of `core-human-knowledge`, paired with an explanatory SVG (COIIAOC palette · V2 typography). Two modes: **in-repo** (numerates, places in `guides/`, SVG mandatory) and **anywhere** (writes the `.md` to the current folder, SVG offered). Distinguishable from `text-to-diagram` and `code-diagram-explainer` — both start from finished code/prose; this one starts from a topic or raw notes. |

---

## How to install a skill

1. Download the `.skill` file from [Releases](../../releases).
2. In Claude.ai, go to **Settings → Skills** and upload the file.
3. The skill will be available in all future conversations.

Alternatively, for Claude Code CLI users: copy the skill folder into `~/.claude/skills/`. Each skill folder (`skills/<category>/<skill-name>/`) installs as `~/.claude/skills/<skill-name>/`. Claude Code discovers skills automatically from that directory.

---

## Skill categories

| Category                              | What goes here                                                     |
| ------------------------------------- | ------------------------------------------------------------------ |
| `skills/dev/`                       | Code auditors, linters, generators, repo tools                     |
| `skills/content/`                   | Post writers, doc builders, voice refiners, validators             |
| `skills/agentic/`                   | Multi-step workflows, agent orchestrators, automation pipelines    |
| `skills/<name>/` (top-level)         | Cross-repo / standalone skills with their own conventions — these don't belong to dev/content/agentic |

---

## Linked skill collections (submodules)

This repo tracks external skill collections as Git submodules:

| Folder | Source | Description |
| ------ | ------ | ----------- |
| [`skills-lurio84/`](skills-lurio84/) | [lurio84/claude-skills](https://github.com/lurio84/claude-skills) | External skill collection by lurio84 |

### Common submodule operations

**Clone this repo including all submodules:**
```bash
git clone --recurse-submodules https://github.com/therobotacademy/claude-skills.git
```

**If you already cloned without submodules, initialize them:**
```bash
git submodule update --init --recursive
```

**Pull latest changes from a submodule's upstream:**
```bash
git submodule update --remote skills-lurio84
```

**Pull all submodules' latest upstream at once:**
```bash
git submodule update --remote --merge
```

**Check status of all submodules:**
```bash
git submodule status
```

After `--remote` updates, commit the updated pointer in the parent repo:
```bash
git add skills-lurio84
git commit -m "chore: update skills-lurio84 submodule to latest"
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Each skill must follow the standard structure and include a `SKILL.md` with YAML frontmatter. Run the included skill validator before opening a PR.

---

## License

MIT — see [LICENSE](LICENSE).
