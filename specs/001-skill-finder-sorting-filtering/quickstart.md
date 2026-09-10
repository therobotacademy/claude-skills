# Quickstart: Validation & Verification Guide

**Feature**: `specs/001-skill-finder-sorting-filtering` (Skill Finder Sorting and Category Filtering)  
**Date**: 2026-09-10

## 1. Prerequisites

- Any modern web browser (Edge, Chrome, Firefox, Safari).
- Repository cloned locally.

---

## 2. Test Scenarios

### Scenario 1: Default Flat Chronological View & Card Badges (P1)

1. Open `skill-finder.html` in your browser:
   ```powershell
   Start-Process .\skill-finder.html
   ```
2. **Observe initial rendering**:
   - The view layout is a single unified list (no category partition headers).
   - The "Recientes" button is visually active.
   - The skills at the very top of the list are dated `2026-09-10` (`quick-skill-md`, `claude-to-agents-md`), followed by `setup-opencode-local` (`2026-09-02`).
   - The oldest skills (`fitz-agent-auditor`, `repo-reconciler`) appear at the bottom of the list.
3. **Inspect cards**:
   - Every card has a visible top-level category badge (e.g. `Dev`, `Agentic`, `Content`, `Code`).
   - Every card has a visible creation/update date string (`YYYY-MM-DD`).

---

### Scenario 2: Toggle to Grouped-by-Category View (P2)

1. With `skill-finder.html` open in Browse mode, click the **"Por Categoría"** button.
2. **Verify grouping**:
   - The list transitions to 4 category blocks with icons and titles: *Content*, *Dev*, *Agentic*, *Code*.
3. **Verify internal ordering**:
   - Under **Dev**, verify the first card is `quick-skill-md` (`2026-09-10`), followed by `pdf-TOC-bookmarker` (`2026-08-24`).
   - Under **Agentic**, verify the first card is `claude-to-agents-md` (`2026-09-10`), followed by `setup-opencode-local` (`2026-09-02`).
   - Under **Content**, verify the first cards are `lab-doc-pipeline` and `md-guide-builder` (`2026-08-23`).
   - Under **Code**, verify the first cards are `text-to-diagram` and `code-diagram-explainer` (`2026-08-22`).
4. Click **"Recientes"** to toggle back:
   - The view returns seamlessly to the unified flat list.

---

### Scenario 3: Category Filtering (P3)

1. In flat view, click the **"Agentic"** filter pill.
2. **Verify**:
   - Only skills with the `Agentic` badge are visible (`claude-to-agents-md`, `setup-opencode-local`, `flow`, `setup-minimax`, `registro-sesion-claude`, `session-cot`).
   - No `Dev`, `Content`, or `Code` skills are shown.
3. Switch to **"Por Categoría"** view while "Agentic" filter is active:
   - Only the *Agentic* category block is rendered. Other category blocks are hidden.
4. Click the **"Todas"** filter pill:
   - All category blocks re-appear.

---

### Scenario 4: Combined Search and Category Filter

1. Select the **"Dev"** category filter pill.
2. In the search box, type: `karpathy`
3. **Verify**:
   - Only `karpathy-guidelines` and `karpathy-llm-wiki` appear.
   - Clear the search box: all Dev skills re-appear.

---

### Scenario 5: Non-Regression Check on Guided Tree

1. Click **"Guided decision tree"** in the top navigation bar.
2. Navigate through the decision prompts:
   - Click *Publish or refine written content* → Click *Check if an article sounds human enough*.
   - Verify the leaf result card displays `authorship-validator` with direct link and copy prompt buttons.
3. Click **"Browse all skills"**:
   - Verify state is intact and Browse view functions normally.
