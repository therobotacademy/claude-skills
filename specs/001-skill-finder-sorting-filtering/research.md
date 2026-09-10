# Phase 0: Research & Technical Decisions

**Feature**: `specs/001-skill-finder-sorting-filtering` (Skill Finder Sorting and Category Filtering)  
**Date**: 2026-09-10

## 1. Skill Date Resolution and Data Model

### Context
`skill-finder.html` is a standalone HTML file containing an in-memory `SKILLS` catalog. To support chronological sorting, each skill entry requires a creation/update date.

### Decision
Extend the existing `SKILLS` dictionary in `skill-finder.html` by adding an ISO-formatted `date: "YYYY-MM-DD"` property to all 27 skill entries. The dates are derived from repository commit history and file creation records:

| Skill | Category | Date | Basis |
| :--- | :--- | :--- | :--- |
| `quick-skill-md` | Dev | 2026-09-10 | Added in commit `c825a98` |
| `claude-to-agents-md` | Agentic | 2026-09-10 | Added in commit `d47a637` |
| `setup-opencode-local` | Agentic | 2026-09-02 | Added in commit `c275d2d` |
| `pdf-TOC-bookmarker` | Dev | 2026-08-24 | Added in commit `aa73bc9` |
| `lab-doc-pipeline` | Content | 2026-08-23 | Added in commit `623939e` |
| `md-guide-builder` | Content | 2026-08-23 | Added in commit `c5337c6` |
| `flow` | Agentic | 2026-08-23 | Added in commit `e033df7` |
| `text-to-diagram` | Code | 2026-08-22 | Added in commit `1525b77` |
| `code-diagram-explainer` | Code | 2026-08-22 | Added in commit `ca8c412` |
| `pseudocode-ladder` | Code | 2026-08-20 | Added in commit `cb2dfc8` |
| `opus5-optim` | Dev | 2026-08-15 | Added in commit `1e9e1d7` |
| `karpathy-guidelines` | Dev | 2026-08-10 | Added in commit `234aeeb` |
| `setup-minimax` | Agentic | 2026-08-05 | Added in commit `59a543f` |
| `log-turn` | Dev | 2026-06-29 | Added in commit `1caa3df` |
| `registro-sesion-claude` | Agentic | 2026-06-20 | Added in commit `ecbabfb` |
| `session-cot` | Agentic | 2026-06-20 | Added in commit `ecbabfb` |
| `word-template-gen` | Content | 2026-06-15 | Added in commit `d5dcd7e` |
| `pdf-export` | Content | 2026-05-23 | Added in commit `a733a19` |
| `karpathy-llm-wiki` | Dev | 2026-05-20 | Repository commit history |
| `obsidian-graph-colors` | Dev | 2026-05-20 | Repository commit history |
| `obsidian-vault-builder` | Dev | 2026-05-20 | Repository commit history |
| `authorship-validator` | Content | 2026-05-15 | Repository commit history |
| `voice-refiner` | Content | 2026-05-15 | Repository commit history |
| `atlas-slop-ai` | Content | 2026-05-10 | Repository commit history |
| `latex-md-roundtrip` | Content | 2026-05-01 | Repository commit history |
| `repo-reconciler` | Dev | 2026-04-20 | Repository commit history |
| `fitz-agent-auditor` | Dev | 2026-04-15 | Repository commit history |

### Rationale
- Zero runtime overhead and zero network dependencies.
- ISO strings (`YYYY-MM-DD`) allow reliable lexicographical string comparison via `b.date.localeCompare(a.date)`.
- Eliminates CORS issues that would arise if loading external JSON files via `file://`.

### Alternatives Considered
- **Dynamic Git query via local server**: Rejected because `skill-finder.html` must remain a 100% self-contained, serverless document executable directly by double-clicking the file.
- **Timestamp integer timestamps**: Rejected because human-readable ISO dates (`2026-09-10`) are directly renderable in UI cards without conversion functions.

---

## 2. UI Controls & Component Architecture

### Context
Users require:
1. Default chronological flat view.
2. Ability to toggle between flat chronological view and grouped-by-category view.
3. Ability to filter skills by category across both views.
4. Seamless integration with text search and dark/light mode.

### Decision
Place a dedicated control bar (`.browse-controls`) beneath `#search`:
1. **View Layout Toggle Buttons**:
   - `[🕒 Recientes (Plano)]` (active by default)
   - `[📁 Por Categoría]`
2. **Category Filter Pills**:
   - `[Todas]` (active by default), `[Content]`, `[Dev]`, `[Agentic]`, `[Code]`
   - Each pill displays an icon or label corresponding to the category.
3. **Skill Card Metadata Layout**:
   - Inside `.skill-card`, render a header row containing:
     - Skill title `<h3>`
     - Metadata badges container with:
       - Category badge (`.badge.category-badge`), e.g., `<span class="badge-cat">Dev</span>`
       - Date badge (`.badge.date-badge`), e.g., `<span class="badge-date">2026-09-10</span>`
   - Preserves description paragraph and relative path code block.

### Rationale
- Pill buttons match the existing `.mode-btn` design language already established in `skill-finder.html`.
- CSS custom properties (`--panel`, `--border`, `--accent`, `--muted`, `--code-bg`) automatically support both light and dark modes without new palette dependencies.
- Keeping controls in the Browse view avoids polluting the Guided Decision Tree view.

### Alternatives Considered
- **HTML `<select>` Dropdown for Category**: Rejected in favor of pill buttons because pills show all available categories simultaneously, require 1 click instead of 2 (open + select), and are more touchscreen-friendly.

---

## 3. Sorting and Filtering Engine

### Context
The catalog must handle search keywords, category filtering, and sorting simultaneously with zero perceptible lag.

### Decision
Implement a single reactive pipeline:
```javascript
let currentViewLayout = "flat"; // "flat" | "grouped"
let currentCategoryFilter = "all"; // "all" | "Content" | "Dev" | "Agentic" | "Code"
let currentSearchQuery = "";

function sortChronological(a, b) {
  return b.date.localeCompare(a.date) || a.name.localeCompare(b.name);
}

function getFilteredSkills() {
  const q = currentSearchQuery.trim().toLowerCase();
  return Object.values(SKILLS).filter(skill => {
    const matchesCat = currentCategoryFilter === "all" || skill.category === currentCategoryFilter;
    const matchesSearch = !q || skill.name.toLowerCase().includes(q) || skill.desc.toLowerCase().includes(q);
    return matchesCat && matchesSearch;
  });
}
```

- When `currentViewLayout === "flat"`:
  - Sort the filtered skills array using `sortChronological`.
  - Render directly into `#skills-container`.
  - If array is empty, render a helpful empty state notice.
- When `currentViewLayout === "grouped"`:
  - For each category in `CATEGORY_ORDER`:
    - Filter skills where `s.category === cat`.
    - If empty, omit the category section.
    - If not empty, sort using `sortChronological` and render inside the category block with title and icon.

### Rationale
- Computational complexity is $O(N \log N)$ where $N \le 50$, executing in under 1 millisecond.
- Deterministic secondary sort on `a.name` ensures stable ordering when dates match.
- Empty states are handled gracefully in both modes.

---

## 4. Summary of Technical Decisions

| Aspect | Selected Choice | Rejected Alternatives |
| :--- | :--- | :--- |
| **Catalog Date Format** | ISO 8601 string `YYYY-MM-DD` in `SKILLS` | Unix timestamp, Git API |
| **Layout Controls** | Pill button group with active state styling | Dropdown select, checkbox filters |
| **Default Mode** | Flat list sorted chronologically descending | Grouped category view (legacy) |
| **Grouping Behavior** | Grouped by category with descending date sort within each category | Alphabetical grouping |
| **Card Metadata** | Distinct badges for category and date | Hover tooltip, unstyled plain text |
| **Dependencies** | Pure Vanilla HTML5/CSS3/ES6 | React, Vue, jQuery, Tailwind |
