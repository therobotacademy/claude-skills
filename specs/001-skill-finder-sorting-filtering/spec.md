# Feature Specification: Skill Finder Sorting and Category Filtering

**Feature Branch**: `001-skill-finder-sorting-filtering`

**Created**: 2026-09-10

**Status**: Draft

**Input**: User description: "Add to skill-finder.html the default option that the skills are sorted by date of creation/update, and include in its card. The top level category will also be shown in the card. If toggle, change the view to show by categories (as it is now) but ordering by descending date within each category. Also add a filter for the category."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Default Chronological Browse View with Card Metadata (Priority: P1)

As a user exploring the skills catalog, I want the skills to be presented by default as a single flat list sorted chronologically (newest first), with each skill card displaying its top-level category and creation or update date, so that I immediately see recent additions and key metadata without navigating through multiple sections.

**Why this priority**: Solves the primary user need of quickly discovering what skills were recently added or modified, providing immediate context on each card (date and category).

**Independent Test**: Load the catalog. Verify that skills appear in a single unified list sorted from newest to oldest date, and verify each card visibly displays its creation/update date and category tag.

**Acceptance Scenarios**:

1. **Given** the user opens the catalog in Browse mode, **When** the page finishes loading, **Then** all skills are displayed sorted chronologically from newest to oldest date.
2. **Given** a rendered skill card, **When** the user inspects the card, **Then** the card shows the skill name, description, relative path, top-level category, and creation/update date.
3. **Given** two skills with different dates (e.g., 2026-09-10 and 2026-04-15), **When** browsing the default view, **Then** the skill with the more recent date appears ahead of the older skill.

---

### User Story 2 - Toggle to Grouped-by-Category View with Chronological Ordering (Priority: P2)

As a user seeking skills related to a specific workflow area, I want to toggle the catalog display to group skills by category (Dev, Content, Agentic, Code), while still maintaining descending date order within each category group, so that I can explore domain-specific skills chronologically.

**Why this priority**: Preserves the structured domain view familiar to existing users while enhancing it with chronological ordering per category.

**Independent Test**: Click the view toggle button to switch from flat view to category-grouped view. Verify skills are partitioned under category headers and that skills within each header are ordered chronologically (newest first).

**Acceptance Scenarios**:

1. **Given** the catalog is in the default chronological view, **When** the user activates the view layout toggle, **Then** the catalog reorganizes skills under distinct category sections.
2. **Given** the catalog is in category-grouped view, **When** viewing the skills within any category block, **Then** the skills inside that category are ordered from newest to oldest date.
3. **Given** the catalog is in category-grouped view, **When** the user activates the toggle again, **Then** the catalog reverts to the unified flat chronological view.

---

### User Story 3 - Category Filtering across Views (Priority: P3)

As a user focused exclusively on one domain, I want to filter the visible skills by a specific category (or reset to all categories) across both the flat and grouped views, so that I can reduce visual clutter and isolate relevant skills.

**Why this priority**: Provides targeted focus for users who already know which functional category they need, working seamlessly with both layout modes and the search bar.

**Independent Test**: Select a category filter (e.g., "Agentic"). Verify that only skills belonging to "Agentic" remain visible, in both the flat view and the category-grouped view. Verify that combining with search filters only within that category.

**Acceptance Scenarios**:

1. **Given** any view mode with all skills displayed, **When** the user selects a specific category filter, **Then** only skills belonging to that category are shown.
2. **Given** a category filter is active, **When** the user types text into the search input, **Then** the displayed results match both the category filter and the search keywords.
3. **Given** an active category filter, **When** the user selects "All Categories", **Then** skills from all categories are restored according to the current view mode and search filter.

---

### Edge Cases

- **Skills with identical dates**: When two or more skills have the exact same creation/update date, the system must apply a stable secondary sort (alphabetical by skill name) to ensure deterministic rendering order.
- **No matching results**: If a combination of category filter and search query yields zero matching skills, a clear empty state message must be displayed instead of a blank screen.
- **Switching views with active filters**: When toggling between the flat view and the category-grouped view, the active category filter, search query, and scroll stability must be preserved.
- **Empty category under filter in grouped view**: In category-grouped view, if a category has no matching skills (or is filtered out), its header block must not be displayed.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display skills ordered by creation/update date in descending order (newest first) by default upon initial load.
- **FR-002**: System MUST display the creation/update date clearly on every skill card.
- **FR-003**: System MUST display the top-level category clearly on every skill card.
- **FR-004**: System MUST provide a view layout toggle control allowing users to switch between a flat chronological list and a category-grouped list.
- **FR-005**: In category-grouped view, system MUST sort skills within each category group chronologically from newest to oldest.
- **FR-006**: System MUST provide a category filter control offering an "All" option and an option for each available top-level category.
- **FR-007**: System MUST immediately filter visible skill cards when a category filter option is selected.
- **FR-008**: System MUST combine category filtering with keyword search, displaying only skills that satisfy both criteria.
- **FR-009**: System MUST preserve existing search capabilities, live filtering responsiveness, and the guided decision tree view without regression.

### Key Entities *(include if feature involves data)*

- **Skill Entry**: Represents a single skill in the catalog. Key attributes include identifier, name, top-level category (e.g., Dev, Content, Agentic, Code), creation/update date (standard date format `YYYY-MM-DD`), description, repository path, and topic icon.
- **Catalog View Mode**: Represents the active layout presentation mode:
  - `flat`: Unified chronological list ordered by date descending.
  - `grouped`: Categorized sections ordered by canonical category order, with skills within each section sorted by date descending.
- **Filter State**: Represents the active display criteria, comprising a selected category filter (`all` or specific category) and an optional textual search query.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users navigating to the catalog can see the most recent skill within the first viewport height without scrolling on standard desktop displays.
- **SC-002**: 100% of rendered skill cards display accurate category badges and creation/update dates.
- **SC-003**: View toggling and category filter switches apply instantaneously (under 50ms perceptible response) with zero network requests or full page reloads.
- **SC-004**: When searching or filtering, 100% of matching skills are displayed and 0% of non-matching skills are displayed.
- **SC-005**: All existing functionality (text search, guided decision tree, copy/navigation actions) remains 100% functional with zero regressions.

## Assumptions

- Skill dates are derived from repository history (initial commit or latest major skill update) and expressed as ISO date strings (`YYYY-MM-DD`).
- The canonical list of top-level categories remains: `Content`, `Dev`, `Agentic`, and `Code`.
- The interface remains a self-contained, standalone single-file document capable of operating fully offline with zero external build tools, servers, or CDN dependencies.
- The view toggle and category filter controls will be intuitive and responsive on both mobile and desktop viewports.
