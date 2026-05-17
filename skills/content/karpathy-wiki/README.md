# karpathy-wiki

A three-skill stack for building and maintaining a personal knowledge base in Obsidian, powered by LLMs. Based on Andrej Karpathy's wiki pattern: the LLM writes and maintains the wiki; the human reads and asks questions.

---

## Skills

| Layer | Skill | Responsibility |
|-------|-------|----------------|
| 1 · Infrastructure | [`obsidian-vault-builder`](obsidian-vault-builder/) | Create and configure the Obsidian vault (`.obsidian/` JSON files) without opening the app |
| 2 · Content | [`karpathy-llm-wiki`](karpathy-llm-wiki/) | Ingest sources, compile wiki articles, query knowledge, lint consistency |
| 3 · Visual | [`obsidian-graph-colors`](obsidian-graph-colors/) | Manage Graph view color groups in `graph.json` |

---

## How they fit together

```
obsidian-vault-builder  ──►  karpathy-llm-wiki  ──►  obsidian-graph-colors
  create .obsidian/            populate raw/ wiki/       color the graph nodes
```

Each skill owns a distinct layer and delegates the others explicitly:

- **obsidian-vault-builder** handles the 5 `.obsidian/` files (`app.json`, `appearance.json`, `core-plugins.json`, `graph.json`, `workspace.json`). It generates `workspace.json` with fresh UUIDs via `build_workspace.py` and applies plugin/layout templates. Once the vault exists, it hands off to the other two.
- **karpathy-llm-wiki** never touches `.obsidian/`. It works entirely in `raw/` (immutable sources) and `wiki/` (compiled articles). Three operations: **ingest** (fetch → compile → cascade updates → update index), **query** (search and synthesize from the wiki), **lint** (auto-fix broken links and index inconsistencies).
- **obsidian-graph-colors** never touches `raw/` or `wiki/`. It reads and writes only `graph.json`. Always starts by running `audit.py` to show the current color state before making any change.

Each skill can run independently as long as its layer's prerequisites exist.

---

## Typical workflow

### 1. Bootstrap a new vault

```
obsidian-vault-builder: bootstrap vault
```

Prompts for plugin profile (`minimal` | `full` | `bayesiano`), graph template, and layout. Writes all 5 `.obsidian/` files.

### 2. Ingest a source

```
karpathy-llm-wiki: ingest <URL or paste>
```

Saves to `raw/<topic>/YYYY-MM-DD-slug.md`, compiles or merges into `wiki/<topic>/<article>.md`, cascades updates to related articles, and refreshes `wiki/index.md` and `wiki/log.md`.

### 3. Query the wiki

```
karpathy-llm-wiki: what do I know about <topic>?
```

Reads `wiki/index.md`, loads relevant articles, and synthesizes an answer with citations.

### 4. Color the graph

```
obsidian-graph-colors: esquema de colores por tier
```

Runs `audit.py` to show current state, then applies or adjusts color groups in `graph.json`.

---

## File layout

```
karpathy-wiki/
├── README.md                          ← this file
├── karpathy-llm-wiki/
│   └── SKILL.md
├── obsidian-graph-colors/
│   ├── SKILL.md
│   └── audit.py                       ← color audit script
└── obsidian-vault-builder/
    ├── SKILL.md
    ├── build_workspace.py             ← generates workspace.json with fresh UUIDs
    └── templates/
        ├── core-plugins-minimal.json
        ├── core-plugins-full.json
        ├── core-plugins-bayesiano.json
        └── graph-bayesiano.json
```

---

## Critical constraint shared by all three skills

**Obsidian must be closed before any write to `.obsidian/`.** Obsidian overwrites its config files on interaction; an external write while it is open will be silently reverted. All three skills warn and wait for confirmation before touching any `.obsidian/` file.
