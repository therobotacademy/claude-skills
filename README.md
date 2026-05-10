# bernardo-skills

A curated collection of Claude skills for development, content creation, and agentic workflows.

Skills are self-contained instructions that extend Claude's capabilities for specific recurring tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting resources.

---

## Skills

### 🛠️ Dev

| Skill | Description |
|-------|-------------|
| [`repo-reconciler`](skills/dev/repo-reconciler/) | Audits a repository for inconsistencies between code and documentation — detects undocumented features, stale README sections, broken examples, and version drift. Generates ready-to-apply patches. |
| [`fitz-agent-auditor`](skills/dev/fitz-agent-auditor/) | Forensic analysis of AI agent outputs using the FITZ taxonomy (SALUDABLE / ALUCINACIÓN / INYECCIÓN / DRIFT). Detects hallucination, prompt injection, and role drift. Produces a verdict, detected signals, and an operational recommendation to prevent recurrence. |
| [`log-turn`](skills/dev/log-turn/) | Automatically appends every conversation turn to `sessions/today-LOG.md` in a structured `## Prompt N: <Title>` / `## Response N` format. Always active by default; switches to on-demand mode only if the user explicitly requests it in the current session. |

### ✍️ Content

| Skill | Description |
|-------|-------------|
| [`authorship-validator`](skills/content/authorship-validator/) | Validates human authorship of an article before publishing using the VIDAL framework (VIVO / INTERVENIDO / DELEGADO / GHOST). Detects friction signals vs. LLM homogeneity and produces specific rewrite recommendations. Requires personal calibration with your own reference texts. |
| [`voice-refiner`](skills/content/voice-refiner/) | Iteratively refines an article until it reaches ≥85% human authorship confidence and ≤2 AI-flagged phrases. Operates in autonomous mode (Model A) or author-reviewed mode (Model B). Depends on `authorship-validator`. |
| [`atlas-slop-ai`](skills/content/atlas-slop-ai/) | Classifies editorial articles in a 2×2 matrix crossing two independent axes — authorship (human vs AI-produced) and substance (own thesis vs slop) — to produce a diagnostic content quality map. Supports digest mode (batch classification with table output) and solo mode (single article). Outputs text/JSON classification or an interactive HTML atlas. |
| [`latex-md-roundtrip`](skills/content/latex-md-roundtrip/) | Round-trip-safe pipeline for editing a LaTeX paper in Markdown and regenerating the LaTeX target ready for upload (Overleaf / arXiv / journal). Pandoc isn't bijective, so the skill freezes the preamble as a template, curates a baseline MD with raw-LaTeX blocks for constructs Pandoc loses, and generates a check script + per-cycle regen script (canonical templates in `assets/`, paths substituted per project). Output filenames are content-driven, not version-numbered. |

### 🤖 Agentic

| Skill | Description |
|-------|-------------|
| [`registro-sesion-claude`](skills/agentic/registro-sesion-claude/) | Captures metrics and scope of a Claude Code session into a structured Markdown file (`USAGE.md`). Triggered by phrases like "registra la sesión", "documenta esta sesión", or pasting `/usage` output. |

---

## How to install a skill

1. Download the `.skill` file from [Releases](../../releases).
2. In Claude.ai, go to **Settings → Skills** and upload the file.
3. The skill will be available in all future conversations.

Alternatively, clone this repo and point your Claude Code setup to the `skills/` directory.

---

## Skill categories

| Category | What goes here |
|----------|---------------|
| `skills/dev/` | Code auditors, linters, generators, repo tools |
| `skills/content/` | Post writers, doc builders, voice refiners, validators |
| `skills/agentic/` | Multi-step workflows, agent orchestrators, automation pipelines |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Each skill must follow the standard structure and include a `SKILL.md` with YAML frontmatter. Run the included skill validator before opening a PR.

---

## License

MIT — see [LICENSE](LICENSE).
