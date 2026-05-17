---
name: karpathy-llm-wiki
description: Use when building or maintaining a personal LLM-powered knowledge base. Triggers: ingesting sources into a wiki, querying wiki knowledge, linting wiki quality, 'add to wiki', 'what do I know about', or any mention of 'LLM wiki' or 'Karpathy wiki'.
---

# Karpathy LLM Wiki

Build and maintain a personal knowledge base using LLMs. You manage two directories: `raw/` (immutable source material) and `wiki/` (compiled knowledge articles). Sources go into raw/, you compile them into wiki articles, and the wiki compounds over time.

Core ideas from Karpathy:

* "The LLM writes and maintains the wiki; the human reads and asks questions."
* "The wiki is a persistent, compounding artifact."

## Architecture

Three layers, all under the user's project root:

**raw/** — Immutable source material. You read, never modify. Organized by topic subdirectories (e.g., `raw/machine-learning/`).

**wiki/** — Compiled knowledge articles. You have full ownership. Organized by topic subdirectories, one level only: `wiki/<topic>/<article>.md`. Contains two special files:

* `wiki/index.md` — Global index. One row per article, grouped by topic, with link + summary + Updated date.
* `wiki/log.md` — Append-only operation log.

**SKILL.md** (this file) — Schema layer. Defines structure and workflow rules.

---

## Ingest

Fetch a source into raw/, then compile it into wiki/. Always both steps, no exceptions.

### Fetch (raw/)

1. Get the source content using whatever web or file tools your environment provides. If nothing can reach the source, ask the user to paste it directly.
2. Pick a topic directory. Check existing `raw/` subdirectories first; reuse one if the topic is close enough. Create a new subdirectory only for genuinely distinct topics.
3. Save as `raw/<topic>/YYYY-MM-DD-descriptive-slug.md`.
   * Slug from source title, kebab-case, max 60 characters.
   * Published date unknown → omit date prefix. Metadata Published field = `Unknown`.
   * If file with same name exists, append numeric suffix.
   * Include metadata header: source URL, collected date, published date.
   * Preserve original text. Clean formatting noise. Do not rewrite opinions.

### Compile (wiki/)

Determine where the new content belongs:

* **Same core thesis as existing article** → Merge into that article. Add the new source to Sources/Raw. Update affected sections.
* **New concept** → Create a new article in the most relevant topic directory. Name the file after the concept, not the raw file.
* **Spans multiple topics** → Place in the most relevant directory. Add See Also cross-references.

If the new source contradicts existing content, annotate the disagreement with source attribution.

**Article format:**

```markdown
---
title: [Concept Name]
topic: [directory name]
sources: [Author/Org, Date; Author/Org, Date]
raw: [../../raw/topic/file.md]
updated: YYYY-MM-DD
---

# [Concept Name]

## Summary
[2-3 sentence overview]

## [Section]
[Content]

## See Also
- [Related Article](../topic/article.md)
```

### Cascade Updates

After the primary article, check for ripple effects in related articles. Update every article whose content is materially affected. Refresh their Updated date.

### Post-Ingest

Update `wiki/index.md`: add or update entries for every touched article.

Index row format:
```
| [Article Title](topic/article.md) | [One-line summary] | YYYY-MM-DD |
```

Append to `wiki/log.md`:
```
## [YYYY-MM-DD] ingest | <primary article title>
- Updated: <cascade-updated article title>
```

---

## Query

Search the wiki and answer questions. Triggers: "What do I know about X?", "Summarize everything related to Y", "Compare A and B based on my wiki".

### Steps

1. Read `wiki/index.md` to locate relevant articles.
2. Read those articles and synthesize an answer.
3. Prefer wiki content over training knowledge. Cite sources: `[Article Title](wiki/topic/article.md)`.
4. Output in conversation. Do not write files unless asked.

### Archiving

When user asks to archive the answer:

1. Write as new wiki page in the most relevant topic directory.
2. Update `wiki/index.md` with `[Archived]` prefix in summary.
3. Append to `wiki/log.md`:
   ```
   ## [YYYY-MM-DD] query | Archived: <page title>
   ```

---

## Lint

Quality checks. Two categories.

### Deterministic (auto-fix)

* **Index consistency** — file exists but missing from index → add entry. Index entry points to nonexistent file → mark `[MISSING]`.
* **Internal links** — broken link → search wiki/ for same filename. One match → fix. Zero/multiple → report.
* **Raw references** — broken Raw field link → search raw/ for same filename. One match → fix. Zero/multiple → report.
* **See Also** — add obvious missing cross-references. Remove links to deleted files.

### Heuristic (report only)

* Factual contradictions across articles
* Outdated claims superseded by newer sources
* Orphan pages with no inbound links
* Concepts frequently mentioned but lacking a dedicated page

### Post-Lint

```
## [YYYY-MM-DD] lint | <N> issues found, <M> auto-fixed
```

---

## Conventions

* Standard markdown with relative links.
* `wiki/` supports one level of topic subdirectories only. No deeper nesting.
* Inside wiki/ files: paths relative to current file. In conversation output: project-root-relative paths.
* Ingest updates both `wiki/index.md` and `wiki/log.md`. Plain queries do not write files.

---

*Source: https://github.com/Astro-Han/karpathy-llm-wiki — MIT License*
*Installed: 2026-04-30*
