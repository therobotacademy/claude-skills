# bernardo-skills

A curated collection of Claude skills for development, content creation, and agentic workflows.

Skills are self-contained instructions that extend Claude's capabilities for specific recurring tasks. Each skill lives in its own folder with a `SKILL.md` file and optional supporting resources.

---

## Skills

### 🛠️ Dev

| Skill | Description |
|-------|-------------|
| [`repo-reconciler`](skills/dev/repo-reconciler/) | Audits a repository for inconsistencies between code and documentation — detects undocumented features, stale README sections, broken examples, and version drift. Generates ready-to-apply patches. |

### ✍️ Content

*Coming soon.*

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
