# Contributing to bernardo-skills

Thanks for your interest. This document explains how to add or improve a skill.

---

## Skill structure

Every skill lives in its own folder:

```
skills/<category>/<skill-name>/
├── SKILL.md                  # Required. Contains YAML frontmatter + instructions.
├── references/               # Optional. Files loaded into context on demand.
│   ├── some-reference.md
│   └── ...
├── scripts/                  # Optional. Executable code for deterministic tasks.
└── assets/                   # Optional. Templates, fonts, icons used in output.
```

### SKILL.md frontmatter

```yaml
---
name: skill-name              # kebab-case, matches folder name
description: >                # When to trigger + what it does. Be specific.
  One paragraph. Include trigger phrases. Err toward over-describing.
---
```

### Categories

| Folder | For skills that... |
|--------|-------------------|
| `skills/dev/` | Operate on code, repos, or technical artifacts |
| `skills/content/` | Produce or validate written content |
| `skills/agentic/` | Orchestrate multi-step workflows or agent pipelines |
| `skills/code/` | Generate SVG diagrams explaining code or structured text visually |

---

## Adding a skill

1. Fork the repo.
2. Create `skills/<category>/<skill-name>/SKILL.md`.
3. Add any supporting files under `references/`, `scripts/`, or `assets/`.
4. Update the table in `README.md`.
5. Open a PR. Include one example input/output in the PR description.

---

## Skill quality checklist

- [ ] `SKILL.md` has valid YAML frontmatter with `name` and `description`
- [ ] Description includes specific trigger phrases
- [ ] Instructions are unambiguous — no "use your judgment" without criteria
- [ ] `SKILL.md` body is under 500 lines (use `references/` for overflow)
- [ ] Supporting files are referenced explicitly from `SKILL.md`
- [ ] Tested against at least 2 real inputs before submitting

---

## Packaging a skill for release

```bash
python scripts/package_skill.py skills/<category>/<skill-name> [--output dist/]
```

This produces `<skill-name>.skill` in the output directory (default: `dist/`), ready to upload as a GitHub Release asset.
