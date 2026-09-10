# UI Interface Contract: Skill Finder

**Feature**: `specs/001-skill-finder-sorting-filtering`  
**Date**: 2026-09-10

## 1. DOM Hierarchy & Component Structure

```html
<!-- Browse View Section -->
<section class="view active" id="view-browse">
  <!-- Search Input -->
  <div class="search-row">
    <input id="search" type="text" placeholder="Search skills by name or keyword…" autocomplete="off" />
  </div>

  <!-- Browse Controls Bar -->
  <div class="browse-controls">
    <!-- View Mode Segmented Controls -->
    <div class="view-layout-toggle" role="group" aria-label="Layout view">
      <button class="layout-btn active" data-layout="flat" title="List sorted by newest first">
        <!-- clock/calendar SVG icon -->
        <span>Recientes</span>
      </button>
      <button class="layout-btn" data-layout="grouped" title="Grouped by category">
        <!-- folder/grid SVG icon -->
        <span>Por Categoría</span>
      </button>
    </div>

    <!-- Category Filter Pills -->
    <div class="category-filters" role="group" aria-label="Category filter">
      <button class="cat-filter-btn active" data-category="all">Todas</button>
      <button class="cat-filter-btn" data-category="Content">Content</button>
      <button class="cat-filter-btn" data-category="Dev">Dev</button>
      <button class="cat-filter-btn" data-category="Agentic">Agentic</button>
      <button class="cat-filter-btn" data-category="Code">Code</button>
    </div>
  </div>

  <!-- Results Container -->
  <div id="skills-container">
    <!-- Rendered dynamically by renderBrowse() -->
  </div>
</section>
```

---

## 2. Skill Card Markup Contract

Each rendered skill card in both flat and grouped layouts must conform to this markup structure:

```html
<div class="skill-card" data-category="Dev" data-date="2026-09-10">
  <div class="card-meta">
    <span class="badge badge-cat badge-dev">Dev</span>
    <span class="badge badge-date">2026-09-10</span>
  </div>
  <h3>quick-skill-md</h3>
  <p>Generates or updates an ultra-dense operational cheat sheet...</p>
  <code class="path">skills/dev/quick-skill-md/</code>
</div>
```

---

## 3. JavaScript API Contract

### Functions & Signature

```javascript
/**
 * Main render function for the Browse view.
 * Reads runtime state (currentSearchQuery, currentCategoryFilter, currentViewLayout)
 * and mutates the #skills-container DOM element.
 */
function renderBrowse(): void;

/**
 * Updates the active layout ('flat' | 'grouped') and re-renders.
 * @param {string} layout - 'flat' or 'grouped'
 */
function setViewLayout(layout: "flat" | "grouped"): void;

/**
 * Updates the active category filter ('all' | 'Content' | 'Dev' | 'Agentic' | 'Code') and re-renders.
 * @param {string} cat - Category string
 */
function setCategoryFilter(cat: string): void;

/**
 * Compares two skills in descending chronological order with secondary title sort.
 * @param {Skill} a
 * @param {Skill} b
 * @returns {number}
 */
function sortChronological(a: Skill, b: Skill): number;
```

---

## 4. Accessibility & Styling Contract

- **Contrast & Theme Support**:
  - All badges, text, and buttons must use CSS variables (`--bg`, `--panel`, `--text`, `--muted`, `--border`, `--accent`, `--accent-text`, `--code-bg`).
  - Dark mode (`prefers-color-scheme: dark`) support is preserved automatically.
- **Keyboard & Focus**:
  - All interactive buttons (`.layout-btn`, `.cat-filter-btn`) must be keyboard-focusable with visible focus rings.
- **Responsive Layout**:
  - `.browse-controls` must flex-wrap gracefully on mobile viewports (< 600px).
