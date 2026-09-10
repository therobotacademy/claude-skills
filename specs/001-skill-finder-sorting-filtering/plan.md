# Implementation Plan: Skill Finder Sorting and Category Filtering

**Branch**: `001-skill-finder-sorting-filtering` | **Date**: 2026-09-10 | **Spec**: [spec.md](spec.md)

**Input**: Feature specification from `specs/001-skill-finder-sorting-filtering/spec.md`

## Summary

Enhance `skill-finder.html` with:
1. Default flat chronological view ordering skills by date descending (newest first).
2. Card metadata badges displaying creation/update date (`YYYY-MM-DD`) and top-level category on each skill card.
3. View layout toggle switching between flat chronological view and grouped-by-category view (where skills inside each category group are ordered chronologically descending).
4. Category filter pills (`Todas`, `Content`, `Dev`, `Agentic`, `Code`) filtering skills across both view modes in real time.
5. All functionality contained within the standalone, zero-dependency `skill-finder.html` file.

---

## Technical Context

**Language/Version**: HTML5, CSS3, JavaScript (ES6+)  
**Primary Dependencies**: None (Vanilla client-side web technologies; zero external dependencies or CDNs)  
**Storage**: In-memory JavaScript data structures (`SKILLS` object) within `skill-finder.html`  
**Testing**: Manual validation in browser via `quickstart.md` verification scenarios; automated DOM validation script  
**Target Platform**: Any modern desktop or mobile browser (Chrome, Edge, Firefox, Safari) running via `file://` or HTTP server  
**Project Type**: Standalone Single-Page Application (SPA) / Interactive Documentation  
**Performance Goals**: < 10ms for sort, filter, and DOM re-render operations (< 50ms perceptible response)  
**Constraints**: Fully offline-capable, zero external assets, no build step required, strict backwards compatibility with existing decision tree and search functionality  
**Scale/Scope**: ~30 skills, 4 primary categories, 1 single HTML file (`skill-finder.html`)

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- [x] **Zero Build Overhead**: Preserves single-file HTML/CSS/JS delivery without node/npm/bundler steps.
- [x] **Offline Independence**: No external fonts, icons, or scripts injected via external CDNs.
- [x] **Non-Destructive Enhancement**: Preserves all existing skill descriptions, paths, decision tree structure, and CSS theme variables.
- [x] **Simplicity & Surgical Edits**: Only updates `skill-finder.html` and its specification/planning artifacts.

---

## Project Structure

### Documentation (this feature)

```text
specs/001-skill-finder-sorting-filtering/
├── spec.md              # Feature specification
├── plan.md              # This implementation plan
├── research.md          # Phase 0: Technical decisions and dates resolution
├── data-model.md        # Phase 1: Entity schemas and state machine
├── contracts/
│   └── ui-contract.md   # Phase 1: DOM hierarchy and JS signatures
├── quickstart.md        # Phase 1: Verification scenarios
└── checklists/
    └── requirements.md  # Quality validation checklist
```

### Source Code (repository root)

```text
skill-finder.html        # Interactive skill catalog containing HTML, CSS, and JS
```

**Structure Decision**: Single-file update. All markup, CSS styles, catalog data attributes, and JavaScript rendering logic reside in `skill-finder.html`.

---

## Planned Implementation Steps

1. **Catalog Schema Update**:
   - Add `date: "YYYY-MM-DD"` property to each skill in `const SKILLS` in `skill-finder.html`.
   - Ensure all skills have explicit `category` assigned.

2. **CSS Styling Additions**:
   - `.browse-controls`: Flex container for toolbar with responsive wrap.
   - `.view-layout-toggle`, `.layout-btn`: Segmented toggle buttons matching `.mode-btn`.
   - `.category-filters`, `.cat-filter-btn`: Category filter pill buttons with active state.
   - `.card-meta`, `.badge`: Metadata row with `.badge-cat` and `.badge-date`.

3. **JavaScript Engine Refactoring**:
   - Introduce state variables: `currentViewLayout = "flat"`, `currentCategoryFilter = "all"`, `currentSearchQuery = ""`.
   - Implement `sortChronological(a, b)` sorting by date descending with secondary name tiebreaker.
   - Refactor rendering into `renderBrowse()` handling both `flat` and `grouped` layouts, empty state messages, and category filters.
   - Wire event listeners for layout toggle buttons and category filter pills.

4. **Verification**:
   - Execute test scenarios outlined in `quickstart.md`.
