# bernardo-skills

A curated collection of Claude skills for development, content creation, agentic workflows, and a few cross-repo tools.

Skills are self-contained instructions that extend Claude's capabilities for specific recurring tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting resources.

---

## Quick guide: pick a skill by task

Skim this first if you're not sure which skill applies — it's keyed by what you're trying to do, not by category. Full descriptions are in the tables below.

> ⚡ **Operaciones rápidas:** Consulta [`quick-skill.md`](quick-skill.md) para una chuleta operativa sin preámbulos: qué pedir, qué dar de entrada, qué genera el agente y las reglas no negociables del repositorio.

| I want to...                                                            | Use                                                                              |
| ------------------------------------------------------------------------ | --------------------------------------------------------------------------------- |
| Check if an article sounds human enough before publishing              | [`authorship-validator`](skills/content/authorship-validator/)                  |
| Fix an article until it passes that check                              | [`voice-refiner`](skills/content/voice-refiner/) (depends on `authorship-validator`) |
| Triage a batch of articles for authorship + substance at a glance      | [`atlas-slop-ai`](skills/content/atlas-slop-ai/)                                 |
| Edit a LaTeX paper as Markdown and regenerate the `.tex` for submission | [`latex-md-roundtrip`](skills/content/latex-md-roundtrip/)                      |
| Export a Markdown doc to PDF (with math formulas)                      | [`pdf-export`](skills/content/pdf-export/)                                      |
| Generate a themed Word/PDF/HTML document                               | [`word-template-gen`](skills/content/word-template-gen/)                        |
| Generate a corporate Word doc/proposal preserving layout & fonts (RPA)  | [`md-to-docx-rpa`](skills/content/md-to-docx-rpa/)                              |
| Add navigable bookmarks to a PDF that only has a printed index         | [`pdf-TOC-bookmarker`](skills/content/pdf-TOC-bookmarker/)                      |
| Set up or extend a personal Obsidian knowledge base                    | [`karpathy-llm-wiki`](skills/content/karpathy-wiki/karpathy-llm-wiki/) group — see note below |
| Turn a topic or raw notes into a `.md` + `.svg` practical guide         | [`md-guide-builder`](skills/content/md-guide-builder/)                          |
| Turn a solved Jupyter lab into class materials (HTML/Word/PPTX)        | [`lab-doc-pipeline`](skills/content/lab-doc-pipeline/)                          |
| Audit whether an AI agent's output is trustworthy                      | [`fitz-agent-auditor`](skills/dev/fitz-agent-auditor/)                          |
| Check that a repo's docs still match its code                          | [`repo-reconciler`](skills/dev/repo-reconciler/)                                |
| Avoid common LLM coding mistakes (scope creep, silent assumptions)     | [`karpathy-guidelines`](skills/dev/karpathy-guidelines/)                        |
| Force a design checkpoint before Claude writes real code                | [`pseudocode-ladder`](skills/code/pseudocode-ladder/)                        |
| Reverse-engineer an existing repo into a design/decision audit          | [`pseudocode-ladder`](skills/code/pseudocode-ladder/) (INVERSO mode)         |
| Keep a running log of every prompt/response this session               | [`log-turn`](skills/dev/log-turn/)                                              |
| Tame overly long Opus 5 responses                                       | [`opus5-optim`](skills/dev/opus5-optim/)                                        |
| Save a structured record of a Claude Code session (`/usage`, scope)     | [`registro-sesion-claude`](skills/agentic/registro-sesion-claude/)              |
| Write up the reasoning trace of a long session, not just its output    | [`session-cot`](skills/agentic/cot-session/)                                    |
| Switch Claude Code to MiniMax as the model provider                    | [`setup-minimax`](skills/agentic/setup-minimax/)                                |
| Configure a free, offline local coding agent (opencode + llama.cpp) on GPU | [`setup-opencode-local`](skills/agentic/setup-opencode-local/)              |
| Explain a code fragment (function, n8n node, pipeline) as an SVG diagram | [`code-diagram-explainer`](skills/code/code-diagram-explainer/)                |
| Turn a section of prose (methodology, architecture, process) into a diagram | [`text-to-diagram`](skills/code/text-to-diagram/)                          |
| Keep Claude from breaking my creative flow during writing/design/build sessions | [`flow`](skills/agentic/flow/)                                             |
| Migrate or adapt a repo's `CLAUDE.md` to `AGENTS.md` for Antigravity & multi-agent setups | [`claude-to-agents-md`](skills/agentic/claude-to-agents-md/) |
| Audit a repo's rules/skills and generate an operational cheat sheet (`quick-skill.md`) | [`quick-skill-md`](skills/dev/quick-skill-md/) |

---

## Skills

### 🛠️ Dev


| Skill                                                    | Description                                                                                                                                                                                                                                                            |
| ---------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| [`repo-reconciler`](skills/dev/repo-reconciler/)         | Audits a repository for inconsistencies between code and documentation — detects undocumented features, stale README sections, broken examples, and version drift. Generates ready-to-apply patches.                                                                  |
| [`fitz-agent-auditor`](skills/dev/fitz-agent-auditor/)   | Forensic analysis of AI agent outputs using the FITZ taxonomy (SALUDABLE / ALUCINACIÓN / INYECCIÓN / DRIFT). Detects hallucination, prompt injection, and role drift. Produces a verdict, detected signals, and an operational recommendation to prevent recurrence. |
| [`log-turn`](skills/dev/log-turn/)                       | Automatically appends every conversation turn to`sessions/today-LOG.md` in a structured `## Prompt N: <Title>` / `## Response N` format. Always active by default; switches to on-demand mode only if the user explicitly requests it in the current session.          |
| [`karpathy-guidelines`](skills/dev/karpathy-guidelines/) | Behavioral guidelines to reduce common LLM coding mistakes, derived from Andrej Karpathy's observations — surface assumptions, keep changes minimal and surgical, and define verifiable success criteria before looping.                                              |
| [`opus5-optim`](skills/dev/opus5-optim/)                 | Applies Anthropic's official Opus 5 prompting guidance on response length — keeps direct answers concise and high-level unless depth is requested, and inserts a`<tone_preference>` reminder near the end of long system prompts.                                     |
| [`quick-skill-md`](skills/dev/quick-skill-md/)           | Generates or updates an ultra-dense operational cheat sheet (`quick-skill.md`) at the repository root by dynamically discovering agent directives, local skills, workflows, and non-negotiable invariants.                                                            |

### ✍️ Content


| Skill                                                                            | Description                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| ---------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`authorship-validator`](skills/content/authorship-validator/)                   | Validates human authorship of an article before publishing using the VIDAL framework (VIVO / INTERVENIDO / DELEGADO / GHOST). Detects friction signals vs. LLM homogeneity and produces specific rewrite recommendations. Requires personal calibration with your own reference texts.                                                                                                                                                                                               |
| [`voice-refiner`](skills/content/voice-refiner/)                                 | Iteratively refines an article until it reaches ≥85% human authorship confidence and ≤2 AI-flagged phrases. Operates in autonomous mode (Model A) or author-reviewed mode (Model B). Depends on`authorship-validator`.                                                                                                                                                                                                                                                             |
| [`atlas-slop-ai`](skills/content/atlas-slop-ai/)                                 | Classifies editorial articles in a 2×2 matrix crossing two independent axes — authorship (human vs AI-produced) and substance (own thesis vs slop) — to produce a diagnostic content quality map. Supports digest mode (batch classification with table output) and solo mode (single article). Outputs text/JSON classification or an interactive HTML atlas.                                                                                                                    |
| [`latex-md-roundtrip`](skills/content/latex-md-roundtrip/)                       | Round-trip-safe pipeline for editing a LaTeX paper in Markdown and regenerating the LaTeX target ready for upload (Overleaf / arXiv / journal). Pandoc isn't bijective, so the skill freezes the preamble as a template, curates a baseline MD with raw-LaTeX blocks for constructs Pandoc loses, and generates a check script + per-cycle regen script (canonical templates in`assets/`, paths substituted per project). Output filenames are content-driven, not version-numbered. |
| [`pdf-export`](skills/content/pdf-export/)                                       | Exports Markdown documents to PDF via a verified Pandoc (KaTeX) → Chrome headless pipeline. Handles inline and block LaTeX formulas, YAML frontmatter metadata, custom CSS styling, and multi-file concatenation. No LaTeX installation required.                                                                                                                                                                                                                                   |
| [`word-template-gen`](skills/content/word-template-gen/)                         | Generates Word (.docx) templates and PDF/HTML renders from a theme catalog (JSON). Each theme is the single source of design — fonts, palette, sizes — that simultaneously drives the CSS pipeline and the Word reference-doc, ensuring visual consistency between PDF and Word outputs. Includes themes`academico-brj`, `neutro`, and `moderno`.                                                                                                                                  |
| [`md-to-docx-rpa`](skills/content/md-to-docx-rpa/)                               | Emulates an RPA operator to generate or update corporate Word (.docx) documents and proposals from templates, preserving exact typography (Verdana, Poppins, Segoe UI, Calibri), headers, cover design, and modular tables without falling back to Times New Roman.                                                      |
| [`karpathy-llm-wiki`](skills/content/karpathy-wiki/karpathy-llm-wiki/)           | Builds and maintains a personal LLM-powered knowledge base with two directories:`raw/` (immutable sources) and `wiki/` (compiled articles). Supports ingest (fetch → compile → cascade updates), query (search and synthesize), and lint (auto-fix broken links and index inconsistencies). Based on Karpathy's wiki pattern.                                                                                                                                                      |
| [`obsidian-graph-colors`](skills/content/karpathy-wiki/obsidian-graph-colors/)   | Manages color groups in Obsidian's Graph view by reading and writing`graph.json`. Runs an audit script to show current state, detect orphan/missing groups, and flag duplicate hex values. Supports add, change, delete, and bulk color-scheme operations.                                                                                                                                                                                                                           |
| [`obsidian-vault-builder`](skills/content/karpathy-wiki/obsidian-vault-builder/) | Creates and configures a complete Obsidian vault (5`.obsidian/` JSON files) without opening Obsidian. Supports bootstrap from templates (minimal / full / bayesiano), plugin toggling, layout regeneration via `build_workspace.py`, and vault inspection/audit.                                                                                                                                                                                                                     |
| [`pdf-TOC-bookmarker`](skills/content/pdf-TOC-bookmarker/)                       | Generates PDF bookmarks (outline) from a printed table of contents when the PDF has no embedded outline. Extracts and re-joins the TOC text, parses the Part/Chapter/Section hierarchy via regex, computes the printed-page → real-PDF-index offset empirically, and writes nested bookmarks with `pypdf`. Includes a mandatory verification step (node count, tree sanity check, spot-checking a few entries against actual page content).                                       |
| [`md-guide-builder`](skills/content/md-guide-builder/)                           | Converts a topic or raw notes into a practical guide: a house-style `.md` (`NN-TIPO-tema.md` with a guiding idea, numbered sections, summary table, numbered rules, command cheat sheet) paired with a self-explanatory SVG diagram (COIIAOC palette, V2 typography). In-repo mode numbers and files into `guides/` with the SVG mandatory; anywhere mode writes to the current directory with the SVG offered, not imposed. Can also emit a portable prompt template for using the same house style outside this repo.                                                          |
| [`lab-doc-pipeline`](skills/content/lab-doc-pipeline/)                           | Four-phase pipeline that turns a solved Jupyter lab notebook into class materials: (1) an interactive HTML for in-class projection with live sliders, (2) a self-contained Word study document, (3) a theoretical Word covering conceptual foundations, and (4) a PPTX presentation with presenter notes. The notebook is the canonical source for every numeric value; phases are independent and can be run individually or chained, reusing figures generated by earlier phases.                                                                                            |

> **karpathy-wiki group** — the three skills above form a layered stack with non-overlapping responsibilities:
>
>
> | Layer               | Skill                    | When to use                                                       |
> | --------------------- | -------------------------- | ------------------------------------------------------------------- |
> | 1 · Infrastructure | `obsidian-vault-builder` | Create or reconfigure`.obsidian/` (bootstrap, layout, plugin set) |
> | 2 · Content        | `karpathy-llm-wiki`      | Ingest sources, query the wiki, lint broken links and index       |
> | 3 · Visual         | `obsidian-graph-colors`  | Add, change, or audit Graph view color groups in`graph.json`      |
>
> Typical order: `obsidian-vault-builder` → `karpathy-llm-wiki` → `obsidian-graph-colors`. Each skill can also run independently once its layer's prerequisites exist.

**NOTE**: Refer to `skills\content\karpathy-wiki\README.md` for the details

### 🤖 Agentic


| Skill                                                              | Description                                                                                                                                                                                                                                                                                                                                                                   |
| -------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`registro-sesion-claude`](skills/agentic/registro-sesion-claude/) | Captures metrics and scope of a Claude Code session into a structured Markdown file (`USAGE.md` or `sessions/{date}-{slug}.md`). Triggered by phrases like "registra la sesión", "documenta esta sesión", or pasting `/usage` output.                                                                                                                                       |
| [`session-cot`](skills/agentic/cot-session/)                       | Reconstructs the reasoning trace of a complex session as a Chain of Thought document — numbered steps with Input / Reasoning / Key inference, plus recurring reasoning patterns. Triggered by "escribe el CoT", "documenta el razonamiento de la sesión", or at the close of long design/architecture sessions. Not a summary of output — a trace of the thinking process. |
| [`setup-minimax`](skills/agentic/setup-minimax/)                   | Walks a non-technical user through configuring Claude Code to use MiniMax as the model provider — one question at a time, verifies each step, creates the launcher`.bat` and the MCP config for web search. Triggered by "configurar Claude Code con MiniMax", "quiero usar MiniMax", "cambiar a MiniMax-M3".                                                                |
| [`setup-opencode-local`](skills/agentic/setup-opencode-local/)     | Walks a non-technical user through configuring a local LLM (Qwen2.5-Coder via llama.cpp) with the `opencode` coding-agent CLI — 100% offline, free, and tuned for modest GPUs (e.g., RTX 2060 with 6–8 GB VRAM). Detects VRAM, guides installation, configures `opencode.json`, and verifies execution with dual editing tests.                                      |
| [`flow`](skills/agentic/flow/)                                     | Always-on interaction contract for creative work sessions (writing, design, composition, app-building) — detects TOOL / STUCK / WORKSHOP mode each turn and constrains response length, register, and what Claude produces, to protect the human's flow state and sense of authorship. Consulted every turn of a creative session, not just when flow/focus is mentioned; `/flow` re-arms, `/flow off` suspends for the session. |
| [`claude-to-agents-md`](skills/agentic/claude-to-agents-md/)       | Migrates and adapts a project's instructions from `CLAUDE.md` to a canonical, Antigravity-optimized `AGENTS.md` following standard multi-agent execution conventions, tool definitions, invariants, and Definition of Done. |

### 📊 Code

| Skill                                                            | Description                                                                                                                                                                                                                     |
| ------------------------------------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| [`code-diagram-explainer`](skills/code/code-diagram-explainer/) | Generates inline SVG diagrams explaining a code fragment — n8n nodes, functions, pipelines, classes — with literal pseudo-code extracted from source, control flow with ✓/✗ branches, and didactic click-to-ask annotations. |
| [`text-to-diagram`](skills/code/text-to-diagram/)               | Converts a section of structured text (methodology, process, architecture, conceptual framework) into an SVG diagram meant to replace the text, not decorate it — readable without going back to the original prose.        |
| [`pseudocode-ladder`](skills/code/pseudocode-ladder/)           | 4-level protocol (general logic → classes → function pseudo-code → optional near-Python) inserted before real code, marking each decision as delegable or non-delegable and requiring explicit author sign-off before advancing a level. FORWARD mode plans a new module and persists an Obsidian vault (`docs/design/`) synced with each approved level. INVERSE mode reconstructs the ladder from an existing repo, auditing for undocumented implicit decisions, missing invariants, and boundary violations, with a cheap inventory pass before any deep per-module audit. |

`code-diagram-explainer` and `text-to-diagram` share the COIIAOC v1.1 palette and the `sendPrompt` click-to-ask pattern; `pseudocode-ladder` is a design-checkpoint protocol, not a diagram generator — see [`skills/code/README.md`](skills/code/README.md) for how to pick between all three.

---

## How to install a skill

1. Download the `.skill` file from [Releases](../../releases).
2. In Claude.ai, go to **Settings → Skills** and upload the file.
3. The skill will be available in all future conversations.

Alternatively, for Claude Code CLI users: copy the skill folder into `~/.claude/skills/`. Each skill folder (`skills/<category>/<skill-name>/`) installs as `~/.claude/skills/<skill-name>/`. Claude Code discovers skills automatically from that directory.

---

## Skill categories


| Category                     | What goes here                                                                                         |
| ------------------------------ | -------------------------------------------------------------------------------------------------------- |
| `skills/dev/`                | Code auditors, linters, generators, repo tools                                                         |
| `skills/content/`            | Post writers, doc builders, voice refiners, validators                                                 |
| `skills/agentic/`            | Multi-step workflows, agent orchestrators, automation pipelines                                        |
| `skills/code/`               | SVG diagram generators explaining code or structured text visually                                     |
| `skills/<name>/` (top-level) | Cross-repo / standalone skills with their own conventions — these don't belong to dev/content/agentic |

---

## Linked skill collections (submodules)

This repo tracks external skill collections as Git submodules:


| Folder                               | Source                                                            | Description                          |
| -------------------------------------- | ------------------------------------------------------------------- | -------------------------------------- |
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
