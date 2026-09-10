# Tasks: Skill Finder Sorting and Category Filtering

**Branch**: `001-skill-finder-sorting-filtering` | **Spec**: [spec.md](spec.md) | **Plan**: [plan.md](plan.md)

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Verify baseline state and add shared CSS styling for controls and badges

- [x] T001 Inspect current markup and DOM structure in `skill-finder.html`
- [x] T002 Add CSS layout and styling for toolbar controls (`.browse-controls`, `.view-layout-toggle`, `.layout-btn`, `.category-filters`, `.cat-filter-btn`, `.card-meta`, `.badge`, `.badge-cat`, `.badge-date`, `.empty-state`) in `skill-finder.html`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core catalog schema expansion and state management prerequisites

- [x] T003 Update `const SKILLS` catalog dictionary by adding verified `date: "YYYY-MM-DD"` property to all 27 skill entries in `skill-finder.html`
- [x] T004 Define runtime state variables (`currentViewLayout`, `currentCategoryFilter`, `currentSearchQuery`) and the chronological comparator function `sortChronological(a, b)` in `skill-finder.html`

**Checkpoint**: Catalog data and state management ready — user story implementation can begin.

---

## Phase 3: User Story 1 - Default Chronological Browse View with Card Metadata (Priority: P1) 🎯 MVP

**Goal**: Display all skills by default in a single flat list sorted chronologically (newest first), with category and date badges visible on every card.

**Independent Test**: Open `skill-finder.html` in browser; verify skills appear in a single unified list ordered by date descending (newest skills `quick-skill-md` and `claude-to-agents-md` at the top), with category and date tags on each card.

- [x] T005 [US1] Implement skill card HTML generator rendering category badge (`.badge-cat`) and creation/update date badge (`.badge-date`) alongside title, description, and path in `skill-finder.html`
- [x] T006 [US1] Implement flat chronological rendering logic in `renderBrowse()` sorting all matching skills descending by date in `skill-finder.html`
- [x] T007 [US1] Connect live search input `#search` to filter cards in real time within the default flat chronological view in `skill-finder.html`

**Checkpoint**: User Story 1 (MVP) is fully functional and testable independently.

---

## Phase 4: User Story 2 - Toggle to Grouped-by-Category View (Priority: P2)

**Goal**: Provide a view layout toggle allowing users to switch between the flat chronological list and the category-grouped list, with skills within each category sorted chronologically descending.

**Independent Test**: Click "Por Categoría" toggle; verify skills are partitioned under category headers (*Content*, *Dev*, *Agentic*, *Code*) and sorted newest first within each section. Click "Recientes" toggle to return to flat view.

- [x] T008 [US2] Add view layout toggle buttons markup (`.view-layout-toggle` with "Recientes" and "Por Categoría") inside `.browse-controls` in `skill-finder.html`
- [x] T009 [US2] Implement category-grouped rendering branch in `renderBrowse()` sorting skills descending by date within each category block in `skill-finder.html`
- [x] T010 [US2] Wire click event listeners on `.layout-btn` to update `currentViewLayout`, update active button state, and re-render view in `skill-finder.html`

**Checkpoint**: User Stories 1 and 2 both function independently and integrate seamlessly.

---

## Phase 5: User Story 3 - Category Filtering across Views (Priority: P3)

**Goal**: Provide category filter pills allowing users to isolate skills belonging to a single category (or all) across both flat and grouped layouts, combined with text search.

**Independent Test**: Click "Agentic" filter pill; verify only Agentic skills are visible in both flat and grouped views. Combine with search to filter within that category. Click "Todas" to reset filter.

- [x] T011 [US3] Add category filter pills markup (`.category-filters` with buttons: "Todas", "Content", "Dev", "Agentic", "Code") inside `.browse-controls` in `skill-finder.html`
- [x] T012 [US3] Implement category filtering logic in `getFilteredSkills()` combining `currentCategoryFilter` and `currentSearchQuery` in `skill-finder.html`
- [x] T013 [US3] Wire click event listeners on `.cat-filter-btn` to update `currentCategoryFilter`, toggle active pill styling, and re-render view in `skill-finder.html`

**Checkpoint**: All three user stories are complete, functional, and testable independently.

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Visual polish, empty states, responsiveness, and non-regression verification

- [x] T014 Add empty state container displaying friendly "No skills found matching your filters" message when search or category filter matches zero skills in `skill-finder.html`
- [x] T015 Verify responsive mobile wrap for toolbar controls and dark/light color contrast of metadata badges in `skill-finder.html`
- [x] T016 Execute all 5 verification scenarios from `specs/001-skill-finder-sorting-filtering/quickstart.md` and confirm non-regression of the guided decision tree in `skill-finder.html`

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately.
- **Foundational (Phase 2)**: Depends on Phase 1 — blocks all user stories.
- **User Story 1 (Phase 3 - P1 MVP)**: Depends on Phase 2. Can be deployed/tested independently.
- **User Story 2 (Phase 4 - P2)**: Depends on Phase 3 completion.
- **User Story 3 (Phase 5 - P3)**: Depends on Phase 3 and integrates with Phase 4.
- **Polish (Phase 6)**: Depends on all user story phases completion.

### Parallel Opportunities

- Within Phase 1: CSS additions (T002) can proceed alongside initial structure inspection (T001).
- Within Phase 2: Updating schema dates (T003) and state management setup (T004) can be developed together.
- Within Phase 6: Empty state messaging (T014) and mobile responsiveness check (T015) can run in parallel before final quickstart validation (T016).

---

## Implementation Strategy

### MVP First (User Story 1 Only)
1. Complete Phase 1: Setup (`T001`, `T002`)
2. Complete Phase 2: Foundational (`T003`, `T004`)
3. Complete Phase 3: User Story 1 (`T005`, `T006`, `T007`)
4. **Validate MVP**: Open `skill-finder.html` to confirm chronological flat view and card badges.

### Incremental Delivery
1. Add User Story 2 (`T008`, `T009`, `T010`): Validate view toggling between flat and grouped layouts.
2. Add User Story 3 (`T011`, `T012`, `T013`): Validate category filtering across both layouts.
3. Complete Polish (`T014`, `T015`, `T016`): Verify empty states and full `quickstart.md` matrix.
