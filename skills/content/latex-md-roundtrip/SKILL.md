---
name: latex-md-roundtrip
description: Round-trip-safe pipeline for editing any LaTeX paper in Markdown and regenerating the LaTeX target file ready for upload (Overleaf, arXiv, journal). Fires when the user asks to "set up the round-trip pipeline", "regenerate the LaTeX from MD", "actualiza el LaTeX desde el MD", "round-trip check", "verify roundtrip", "regenerate the paper", "compile the edited version", or any equivalent phrasing about pulling a LaTeX source into MD, editing it, and pushing back. Also fires implicitly on first invocation in a session if the setup artifacts (template + scripts) are missing and the user is about to start MD editing of a LaTeX paper. The skill is project-agnostic: file paths and naming are supplied by the user at setup time and stored in the generated scripts.
---

# latex-md-roundtrip

Round-trip-safe workflow for editing a LaTeX paper in Markdown and producing a LaTeX target as if the edits had been applied directly to the source `.tex`. The skill is **generic**: source, baseline, edit-target, and output filenames are all user-supplied. Output filenames are content-driven (e.g. `main-after-section2-rewrite.tex`, `main-2026-05-10-citations.tex`), not version-numbered.

## Parameter contract

At setup time, the skill collects six paths from the user. After setup these are baked into the generated scripts; the user does not pass them per cycle.

| Parameter | Meaning | Mutability |
|---|---|---|
| `SOURCE_TEX` | The frozen LaTeX source (the version currently in Overleaf / arXiv / journal). | **Read-only.** Never edit. |
| `TEMPLATE_TEX` | Extracted preamble + `$body$` marker + closing. Created in S1. | **Read-only** after S1. |
| `BASELINE_MD` | Round-trip-safe MD mirror of `SOURCE_TEX`. Created in S2. | **Read-only** after S2. |
| `EDIT_MD` | The MD edit target. Initially a copy of `BASELINE_MD`. | Edit freely. |
| `OUTPUT_TEX` | The regenerated LaTeX target. Filename reflects content (e.g. `main-section2-rewrite.tex`). | Generated; manual patches allowed before upload. |
| `BIB_PATH` *(optional)* | Path to `.bib` file. Empty if the paper has no bibliography. | Edit only to add citations. |

The generated scripts also produce:

- `<OUTPUT_TEX>.diff` — diff of `OUTPUT_TEX` against `SOURCE_TEX`. The **review unit**.

## When to ask the user vs. assume

On first invocation in a project:

1. Check whether `TEMPLATE_TEX` and a `regen.sh` (or equivalent name) already exist near the source.
2. If they do, **read them** to recover the parameter values. Don't re-ask.
3. If they don't, **ask the user** for the six paths. Suggest defaults derived from `SOURCE_TEX` (e.g. if `SOURCE_TEX=paper/main.tex`, suggest `TEMPLATE_TEX=paper/template.tex`, `BASELINE_MD=paper/main-baseline.md`, etc.).
4. Confirm the proposed paths before writing anything.

The skill should only proceed without asking if all six paths are unambiguously discoverable from existing artifacts.

## One-time setup

Setup creates four artifacts (template, baseline MD, two scripts) and runs the validation gate once. Skip if all four already exist and the validation passes.

### Step S1 — Extract the preamble into `TEMPLATE_TEX`

Read `SOURCE_TEX`. Identify the **preamble**: everything from `\documentclass` up to **and including** the last command before the body content begins. Heuristic:

- If `\maketitle` is present, include everything through `\maketitle`.
- Else if `\begin{document}` is present without `\maketitle`, include through `\begin{document}` plus any title-block commands that follow it on consecutive lines.
- The body starts at the first `\begin{abstract}`, `\section{}`, or substantive content command.

Write the preamble verbatim to `TEMPLATE_TEX`, then append:

```
$body$

\bibliography{<bib-stem>}   # only if BIB_PATH is set; use the stem, no extension
\end{document}
```

If the source paper does not use `\bibliography{...}` (e.g. embedded `thebibliography` environment, or biblatex with `\printbibliography`), preserve whatever the source uses — copy the closing commands verbatim from the source's tail.

### Step S2 — Generate the round-trip-safe `BASELINE_MD`

A naïve `pandoc <SOURCE_TEX> -o <BASELINE_MD>` produces a lossy MD (drops preamble, `\label`s, `\resizebox`, captions, `\multirow`, custom column specs). The baseline must be **round-trip-safe**, meaning every construct Pandoc cannot represent natively in MD lives as a raw-LaTeX block inside the MD.

Procedure:

```bash
pandoc <SOURCE_TEX> \
  --from=latex \
  --to=markdown \
  --natbib \
  --wrap=preserve \
  --markdown-headings=atx \
  -o <BASELINE_MD>
```

Then audit the produced MD against `SOURCE_TEX` and **inject raw-LaTeX blocks** for:

- The abstract: keep as `\begin{abstract} ... \end{abstract}` verbatim.
- Each table that uses `\multirow`, `\resizebox`, custom `p{N\textwidth}` columns, or `\hline` patterns Pandoc misrepresents: paste the full `\begin{table} ... \end{table}` block verbatim. Do **not** let Pandoc convert it to a pipe-table.
- Each `\label{...}` that lives inside a float (`tab:`, `fig:`, `sec:`, `eq:`) — keep it inside the corresponding raw-LaTeX block.
- Any `\begin{figure} ... \end{figure}` blocks with non-trivial layout (`\subfloat`, `minipage`, `\resizebox`).
- Any custom macros that appear in the body (e.g. `\textsc{}`, project-specific shortcuts) — these usually survive as `\textsc{...}` in Pandoc's output, but verify.

After the baseline is curated, run `check_roundtrip.sh` (S3) to validate. Treat the baseline as **read-only** thereafter.

### Step S3 — Generate `check_roundtrip.sh`

Write a script next to the project (e.g. `SCRIPTS/check_roundtrip.sh` or wherever the user requests) with the user's paths baked in:

```bash
#!/usr/bin/env bash
# Validates that BASELINE_MD round-trips cleanly to LaTeX.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

SOURCE_TEX="<SOURCE_TEX>"
BASELINE_MD="<BASELINE_MD>"
TEMPLATE_TEX="<TEMPLATE_TEX>"
TMP_TEX="$(mktemp --suffix=.tex)"

pandoc "$BASELINE_MD" \
  --from=markdown \
  --to=latex \
  --natbib \
  --template="$TEMPLATE_TEX" \
  -o "$TMP_TEX"

echo "==== Diff: SOURCE_TEX vs round-tripped baseline ===="
diff -u "$SOURCE_TEX" "$TMP_TEX" || true
echo "==== End diff ===="
echo
echo "Acceptable drift: whitespace; option ordering inside \\usepackage{} groups."
echo "NOT acceptable: missing \\label, missing \\caption, lost \\resizebox,"
echo "                math display reflow, content reordering, lost commands."
```

Run it once after S2. The diff must be empty or trivial. **Any content drift means the baseline has a leak; fix the baseline (add more raw-LaTeX blocks) and re-run before proceeding.**

### Step S4 — Generate `regen.sh` (per-cycle generator)

```bash
#!/usr/bin/env bash
# Regenerates OUTPUT_TEX from EDIT_MD and produces the review diff vs SOURCE_TEX.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

EDIT_MD="<EDIT_MD>"
OUTPUT_TEX="<OUTPUT_TEX>"
TEMPLATE_TEX="<TEMPLATE_TEX>"
SOURCE_TEX="<SOURCE_TEX>"

pandoc "$EDIT_MD" \
  --from=markdown \
  --to=latex \
  --natbib \
  --template="$TEMPLATE_TEX" \
  -o "$OUTPUT_TEX"

diff -u "$SOURCE_TEX" "$OUTPUT_TEX" > "${OUTPUT_TEX}.diff" || true

echo "Generated: $OUTPUT_TEX"
echo "Review diff: ${OUTPUT_TEX}.diff"
echo
echo "NEXT: open the diff and verify every hunk traces to a planned edit."
echo "      Unplanned hunks are either Pandoc drift (patch $OUTPUT_TEX manually)"
echo "      or accidental edits (revert in $EDIT_MD)."
```

### Step S5 — Seed the edit target

Copy `BASELINE_MD` to `EDIT_MD` so the first cycle starts from a known-good state. If `EDIT_MD` already exists, skip and warn the user.

## Per-edit-cycle workflow

Every time the user wants to push a change from MD back to LaTeX:

1. **Edit** `EDIT_MD` — apply the planned changes.
2. **(Optional) Preview** as PDF for visual review:
   ```bash
   pandoc <EDIT_MD> --citeproc --bibliography=<BIB_PATH> -o <EDIT_MD%.md>.pdf
   ```
3. **Generate** the LaTeX target and the review diff:
   ```bash
   bash <path-to>/regen.sh
   ```
4. **Review** `<OUTPUT_TEX>.diff` against whatever edit plan or commit description the user is working from. **Every hunk must trace to a planned change.** Hunks that don't are either Pandoc drift (patch manually in `OUTPUT_TEX`) or unplanned changes (revert in `EDIT_MD`).
5. **Manually patch** `OUTPUT_TEX` for any Pandoc drift uncovered in step 4. Common patches:
   - Strip Pandoc's `\tightlist` macros if present (or define them in the preamble — your call).
   - Fix citation ordering inside `\citep{a, b}` if alphabetical order leaked instead of chronological.
   - Restore exact column-spec strings on tables Pandoc rewrote.
6. **Compile** to verify no broken references:
   ```bash
   cd <directory of OUTPUT_TEX>
   pdflatex -interaction=nonstopmode <output-stem>
   bibtex <output-stem>     # only if BIB_PATH was used
   pdflatex -interaction=nonstopmode <output-stem>
   pdflatex -interaction=nonstopmode <output-stem>
   ```
   Confirm: no `?` placeholders for citations, no missing labels, no math-mode errors.
7. **Upload** `OUTPUT_TEX` to the destination (Overleaf, arXiv staging, journal portal) by replacing the current main file. The bibliography only needs re-upload if it was modified.

## Output naming — content-driven, not numeric

Output filenames should describe **what changed**, not a version number. Examples:

| Good | Bad |
|---|---|
| `main-section2-rewrite.tex` | `main-v2.3.tex` |
| `main-2026-05-10-citations.tex` | `main-v3.tex` |
| `main-after-Antonio-review.tex` | `main-v2-final.tex` |
| `main-tighten-abstract.tex` | `main-new.tex` |

The user picks the name when invoking the regen step. Multiple parallel outputs from the same baseline are fine — each represents a different edit. Numeric versioning is fragile (off-by-one mistakes, ambiguity about which version is current) and gives no information about content. Content-driven names are self-documenting and survive reordering.

## Discipline rules (apply during MD editing)

These are the editor's responsibility because Pandoc cannot enforce them:

1. **Citations in chronological order inside groups.** Write `[@rubin_1998; @sentse_2010]`, never `[@sentse_2010; @rubin_1998]`. Pandoc + natbib collapses these to `\citep{rubin_1998, sentse_2010}` preserving the order you wrote.
2. **`@key` only when the author is the sentence subject.** Use `[@key]` for parenthetical citations. Mirrors the LaTeX `\cite{}` vs `\citep{}` distinction.
3. **Don't convert raw-LaTeX tables to Markdown pipe tables.** Tables with `\multirow`, `\resizebox{\textwidth}{!}{...}`, or `p{N\textwidth}` columns stay as full LaTeX `table` environments. Pipe tables only for simple data tables that don't need those macros.
4. **Math display:** use `$$ ... $$` for display blocks, `$ ... $` for inline. Both round-trip to `\[ ... \]` and `$ ... $` respectively under `--natbib` defaults.
5. **Section emphasis only with `**bold**`** — not mid-sentence in prose.
6. **Em-dashes only as real dashes.** Never as parenthetical separators (use commas).

## Risk pockets — known and how to mitigate

| Pocket | Risk | Mitigation |
|---|---|---|
| Multi-row / multi-column tables | Pandoc rewrites the table, losing `\multirow{}` and column-spec strings. | Keep these tables as raw-LaTeX blocks in the MD body. Never use pipe-table syntax for them. |
| `\resizebox{\textwidth}{!}{...}` wrappers | Pandoc strips them entirely. | Same — keep raw-LaTeX. |
| `\label{...}` inside floats | Pandoc may drop or rename labels under pipe-table or figure conversion. | Embed the `\label{...}` as raw-LaTeX inside the corresponding table/figure environment. |
| Citation group order | `--natbib` preserves the order written in the MD. If you wrote `[@b; @a]`, it stays `[@b; @a]`. | Pre-sort by year when typing. |
| Bibliography style | Pandoc emits `\citep{}`/`\cite{}` correctly with `--natbib`, but only if every citation in the MD is either `@key` (subject) or `[@key1; @key2]` (parenthetical). Mixed forms like `(@key, year)` break. | Use the two canonical forms only. |
| Hyperref + Unicode | Some Unicode symbols (≈, ±, ≤, ×) compile fine inline but break inside `\section{}` titles. | Keep section titles ASCII; put fancy symbols only inside paragraph text. |
| Custom macros | If the source uses `\newcommand{\foo}{...}` and the MD inlines `\foo` in body text, Pandoc may not understand it. | Keep `\newcommand{}` definitions in the preamble (already preserved in `TEMPLATE_TEX`); raw-LaTeX-block any body usage Pandoc mangles. |

## Failure modes

| Symptom | Cause | Recovery |
|---|---|---|
| `check_roundtrip.sh` diff shows lost content | `BASELINE_MD` is lossy on a specific construct. | Identify the construct in the diff. Add it as a raw-LaTeX block in `BASELINE_MD`. Re-run the check. |
| `regen.sh` produces an `OUTPUT_TEX` that fails `pdflatex` | A new MD edit introduced a Pandoc-incompatible structure. | Run `pdflatex -interaction=nonstopmode` to identify the line; revert the offending MD edit; re-do it with safer syntax. |
| `bibtex` reports missing references | Citation key in MD doesn't exist in `BIB_PATH`. | Add the entry, or fix the typo. |
| Diff shows alphabetical-order citation groups | Pandoc canonicalized the order. | Verify your MD source has chronological order; if so, Pandoc version may be too new (≥3.x sorts citations) — pin Pandoc or apply post-processing sed. |
| Upload destination rejects the file because preamble drifted | `TEMPLATE_TEX` was edited inadvertently. | Restore from git; never edit the template after S1. |

## Invocation patterns

Acceptable invocations from the user:

- "Set up the round-trip pipeline" / "initialize round-trip for `<source.tex>`" → run setup S1–S5 (ask for any missing paths first).
- "Check round-trip" / "verify roundtrip" → run `check_roundtrip.sh`.
- "Regenerate the LaTeX" / "generate the edited version as `<name>.tex`" → run the per-edit cycle (steps 3–6) with `OUTPUT_TEX` set to the requested name.
- "Upload to Overleaf" → verify steps 3–6 completed cleanly, then list the file paths to upload.

When the skill runs, output one short status line per executed step and surface the diff path/summary at the end. Do not paste the diff body unless asked.

## What this skill does NOT do

- It does not decide *what* to edit. Edit content comes from the user (or from an edit plan the user maintains separately).
- It does not handle figure files or auxiliary assets (`.png`, `.pdf` includes). Those continue to live wherever the original source kept them and are uploaded manually.
- It does not validate the *content* of the paper — only the *format* round-trip. Content review is human.
- It does not impose a versioning scheme. The user names the output file whatever describes the edit best.
