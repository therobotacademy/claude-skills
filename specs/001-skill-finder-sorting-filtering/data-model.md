# Data Model: Skill Finder Sorting and Category Filtering

**Feature**: `specs/001-skill-finder-sorting-filtering`  
**Date**: 2026-09-10

## 1. Entities & Schemas

### 1.1 `Skill`
Represents an individual skill definition stored within the `SKILLS` catalog dictionary in `skill-finder.html`.

| Attribute | Type | Required | Constraints | Description |
| :--- | :--- | :--- | :--- | :--- |
| `name` | `string` | Yes | Kebab-case, unique key matching directory name | Canonical skill identifier (e.g. `"quick-skill-md"`). |
| `category` | `string` | Yes | Enum: `"Content"`, `"Dev"`, `"Agentic"`, `"Code"` | High-level taxonomy category. |
| `icon` | `string` | Yes | Key in `ICONS` object | Visual icon key (e.g. `"wrench"`, `"robot"`). |
| `desc` | `string` | Yes | Non-empty string | Purpose, triggers, and summary description. |
| `path` | `string` | Yes | Relative path ending with `/` | Repository path (e.g. `"skills/dev/quick-skill-md/"`). |
| `date` | `string` | Yes | Format `YYYY-MM-DD` | Creation or latest major update date. |

#### JSON Schema representation:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Skill",
  "type": "object",
  "required": ["name", "category", "icon", "desc", "path", "date"],
  "properties": {
    "name": { "type": "string", "pattern": "^[a-z0-9]+(-[a-z0-9]+)*$" },
    "category": { "type": "string", "enum": ["Content", "Dev", "Agentic", "Code"] },
    "icon": { "type": "string" },
    "desc": { "type": "string", "minLength": 10 },
    "path": { "type": "string", "pattern": "^skills/[a-z]+/[a-z0-9-]+/$" },
    "date": { "type": "string", "pattern": "^\\d{4}-\\d{2}-\\d{2}$" }
  },
  "additionalProperties": false
}
```

---

### 1.2 `CatalogState`
Represents the runtime UI state for filtering, searching, and layout mode.

| Field | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `viewLayout` | `enum ("flat", "grouped")` | `"flat"` | Current browse presentation mode. Default is flat chronological. |
| `categoryFilter` | `string` | `"all"` | Active category filter (`"all"` or one of the valid categories). |
| `searchQuery` | `string` | `""` | User-entered search substring (case-insensitive). |
| `activeMode` | `enum ("browse", "tree")` | `"browse"` | Top-level application mode (Browse vs. Guided Tree). |

---

## 2. State Transitions & Lifecycle

```mermaid
stateDiagram-v2
    [*] --> InitialState: Page Load
    state InitialState {
        viewLayout: flat
        categoryFilter: all
        searchQuery: ""
    }

    InitialState --> FilteredState: User selects Category Filter
    InitialState --> SearchedState: User types in Search Input
    InitialState --> GroupedState: User clicks "Grouped View" toggle

    state FilteredState {
        categoryFilter: Content | Dev | Agentic | Code
    }

    state GroupedState {
        viewLayout: grouped
    }

    GroupedState --> FlatState: User clicks "Flat View" toggle
    state FlatState {
        viewLayout: flat
    }

    FilteredState --> CombinedState: Search text added
    SearchedState --> CombinedState: Category filter clicked
    GroupedState --> CombinedState: Filter or Search changed
```

---

## 3. Data Transformations & Sorting Rules

1. **Filtering**:
   $$\text{VisibleSkills} = \{ s \in \text{SKILLS} \mid (C = \text{"all"} \lor s.\text{category} = C) \land (Q = \text{""} \lor s.\text{name} \text{ contains } Q \lor s.\text{desc} \text{ contains } Q) \}$$
   Where $C$ is `categoryFilter` and $Q$ is `searchQuery.toLowerCase()`.

2. **Chronological Sorting**:
   - Primary: $s_b.\text{date} > s_a.\text{date}$ (descending).
   - Secondary: $s_a.\text{name} < s_b.\text{name}$ (lexicographical ascending for ties).

3. **Grouped Partitioning**:
   - For each category $K \in [\text{"Content"}, \text{"Dev"}, \text{"Agentic"}, \text{"Code"}]$:
     - Subset: $S_K = \{ s \in \text{VisibleSkills} \mid s.\text{category} = K \}$, sorted chronologically.
     - Section rendered only if $|S_K| > 0$.
