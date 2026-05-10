# latex-md-roundtrip

A generic skill that makes LaTeX↔Markdown editing of **any paper** round-trip-safe — so edits made in `.md` produce a `.tex` indistinguishable from edits made directly to the LaTeX source, and can be uploaded to Overleaf / arXiv / a journal portal with confidence.

The skill is project-agnostic. Source, baseline, edit-target, and output filenames are all supplied by the user at setup time and baked into the generated scripts.

## Why this skill exists

Many papers live as LaTeX on a remote platform (Overleaf, arXiv, journal submission portals), but the **edit cycle** with Claude and co-authors is faster in Markdown — diffable, review-friendly, citation-light. The natural workflow is:

> `source.tex` → convert to MD → edit MD → regenerate `target.tex` → upload

The problem: **Pandoc is not bijective.** A naïve `latex → md → latex` round-trip silently drops:

- the entire `\documentclass` preamble (packages, custom macros, geometry, hyperref setup),
- `\label{...}` anchors → cross-references break,
- `\resizebox{\textwidth}{!}{...}` wrappers → wide tables overflow,
- `\multirow` / `p{N\textwidth}` column specs → tables get rewritten as plain pipe-tables,
- captions inlined as italic prose, losing `\caption{}` semantics,
- floats, subfloats, and `minipage` layouts.

If you run that round-trip and upload the result, you ship a regression *every cycle*, and only catch it on PDF visual review. Across multiple review rounds, this compounds.

## What this skill does

It implements a **round-trip-safe pipeline**: a small piece of frozen, per-project infrastructure plus a validation gate that catches drift before it ships.

The four pieces of infrastructure, generated once per project from user-supplied paths:

1. **A frozen template** — the preamble of the source `.tex` extracted verbatim, plus a `$body$` marker. Pandoc only generates the body; the preamble is never touched.
2. **A round-trip-safe baseline MD** — a re-generated MD mirror of the source where every construct Pandoc can't represent natively (tables with `\multirow`, `\resizebox`, `\label`s, abstract environment, complex figures) lives as a raw-LaTeX block inside the MD, not as Markdown.
3. **A check script** (`check_roundtrip.sh`) — converts the baseline MD back to LaTeX with the frozen template and diffs against the source. Must be empty or whitespace/option-ordering noise. Anything else means the baseline has a leak — the baseline is fixed, not the source.
4. **A regen script** (`regen.sh`) — the per-cycle generator. Takes the edit-target MD, produces the output LaTeX file (named by content, not by version), and emits a diff against the source as the **review unit** before upload. Accepts a per-run output name as its first argument so one `regen.sh` serves many edit cycles.

**Hybrid script ownership.** The canonical script logic lives in the skill (`assets/check_roundtrip.template.sh`, `assets/regen.template.sh`); setup substitutes the user's paths and materializes per-project copies. The project's scripts ride with the repo (collaborators and CI can run them without the skill), but updates to the skill's templates can be re-substituted into existing projects on demand (`"refresh the round-trip scripts"`).

## The reversibility contract

After setup, the following must hold (and is what `check_roundtrip.sh` enforces):

> `pandoc(BASELINE_MD, template=TEMPLATE_TEX) ≡ SOURCE_TEX`
> (up to whitespace and `\usepackage{}` option ordering)

Once that holds, any edit applied to the edit-target MD becomes structurally equivalent to the same edit applied to the LaTeX source — *for any construct already covered by the baseline*. New constructs (a new kind of table, a new package) require extending the baseline first.

## What the user supplies

At setup time, the skill asks for six paths:

| Parameter | Meaning |
|---|---|
| `SOURCE_TEX` | The frozen LaTeX source (read-only). |
| `TEMPLATE_TEX` | Where to write the extracted preamble. |
| `BASELINE_MD` | Where to write the round-trip-safe MD mirror. |
| `EDIT_MD` | Where edits will happen (seeded as a copy of `BASELINE_MD`). |
| `OUTPUT_TEX` | Where regenerated LaTeX goes — filename describes the edit. |
| `BIB_PATH` *(optional)* | Path to the `.bib` file, if the paper has a bibliography. |

If these artifacts already exist on next invocation, the skill recovers them instead of re-asking.

## Output naming — content-driven, not numeric

Output filenames should describe **what changed**, not a version number.

| Good | Bad |
|---|---|
| `main-section2-rewrite.tex` | `main-v2.3.tex` |
| `main-2026-05-10-citations.tex` | `main-v3.tex` |
| `main-after-Antonio-review.tex` | `main-v2-final.tex` |
| `main-tighten-abstract.tex` | `main-new.tex` |

Numeric versioning is fragile (off-by-one mistakes, ambiguity about which version is current) and gives no information about content. Content-driven names are self-documenting and let multiple parallel edits from the same baseline coexist without confusion.

## What you get every cycle

```
edit EDIT_MD
    ↓
bash regen.sh
    ↓
OUTPUT_TEX           ← upload this
OUTPUT_TEX.diff      ← review this against the planned edits
```

Every hunk in the diff should trace to a planned change. Hunks that don't trace are either Pandoc drift (patch `OUTPUT_TEX` manually) or unplanned edits (revert in `EDIT_MD`).

## Example usage

Assume a paper at `paper/main.tex` co-authored with reviewers, currently hosted on Overleaf, with bibliography at `paper/refs.bib`.

### First invocation — set up the pipeline

```
> Set up the round-trip pipeline for paper/main.tex
```

The skill asks for the six paths and proposes defaults:

```
SOURCE_TEX     = paper/main.tex                  [confirm]
TEMPLATE_TEX   = paper/template.tex              [confirm]
BASELINE_MD    = paper/main-baseline.md          [confirm]
EDIT_MD        = paper/main-edit.md              [confirm]
OUTPUT_TEX     = paper/main-edited.tex           (you'll rename per cycle)
BIB_PATH       = paper/refs.bib                  [confirm]
```

After confirmation it runs S1–S5 and reports:

```
S1  extracted preamble (47 lines) → paper/template.tex
S2  generated baseline → paper/main-baseline.md
    injected 4 raw-LaTeX blocks: abstract, table:results, table:hyperparams, figure:arch
S3  materialized SCRIPTS/check_roundtrip.sh from assets/check_roundtrip.template.sh
S4  materialized SCRIPTS/regen.sh from assets/regen.template.sh
S5  seeded paper/main-edit.md from paper/main-baseline.md
    ran check_roundtrip.sh → 0 content diffs (12 whitespace lines, OK)
```

### Per edit cycle — make a change and push back to LaTeX

Edit `paper/main-edit.md` in your editor (or have Claude edit it). When ready, ask for a regen with a content-driven output name:

```
> Regenerate the LaTeX as paper/main-tighten-abstract.tex
```

The skill runs `regen.sh` with the content-driven name as its first argument (no script edit needed):

```
$ bash SCRIPTS/regen.sh paper/main-tighten-abstract.tex
Generated: paper/main-tighten-abstract.tex
Review diff: paper/main-tighten-abstract.tex.diff (38 lines, 4 hunks)
```

Open the diff. Three hunks rewrite the abstract — those are the planned change. One hunk shows `\tightlist` macros Pandoc inserted around the contribution list — that's Pandoc drift. Strip them:

```
> Strip the \tightlist drift from paper/main-tighten-abstract.tex
```

Then compile and upload:

```bash
cd paper && pdflatex -interaction=nonstopmode main-tighten-abstract
bibtex main-tighten-abstract
pdflatex -interaction=nonstopmode main-tighten-abstract
pdflatex -interaction=nonstopmode main-tighten-abstract
```

Upload `paper/main-tighten-abstract.tex` (and `refs.bib` if it changed) to Overleaf, replacing the current main file.

### Next cycle — different edit, different output name

Same edit-target MD, a different content-driven output name describing the next change:

```
$ bash SCRIPTS/regen.sh paper/main-add-related-work.tex
```

The baseline, template, scripts, and `EDIT_MD` stay the same. The output name describes this round's content. The diff file (`paper/main-add-related-work.tex.diff`) is again the review unit.

## What this skill does NOT do

- It does not decide *what* to edit — that's the user's call.
- It does not handle figures or auxiliary assets — those are uploaded manually.
- It does not review paper content — only the format round-trip.
- It does not impose a versioning scheme — the user names every output by content.

## Files in this skill

- `SKILL.md` — full operational spec: setup steps S1–S5, per-edit-cycle workflow, parameter contract, discipline rules, risk pockets, failure modes, invocation patterns.
- `README.md` — this file.
- `assets/check_roundtrip.template.sh` — canonical validation script. Placeholders `{{SOURCE_TEX}}`, `{{BASELINE_MD}}`, `{{TEMPLATE_TEX}}` substituted at setup.
- `assets/regen.template.sh` — canonical per-cycle generator. Placeholders `{{EDIT_MD}}`, `{{OUTPUT_TEX}}`, `{{TEMPLATE_TEX}}`, `{{SOURCE_TEX}}` substituted at setup; per-run output name overrides via `$1`.

## Trigger phrases

`set up the round-trip pipeline`, `initialize round-trip for <source>`, `regenerate the LaTeX from MD`, `actualiza el LaTeX desde el MD`, `round-trip check`, `verify roundtrip`, `regenerate the paper`, `compile the edited version`, or any equivalent phrasing about pulling a LaTeX source into MD, editing it, and pushing back. Also fires implicitly on first invocation in a session if the setup artifacts are missing and the user is about to start MD editing of a LaTeX paper.
