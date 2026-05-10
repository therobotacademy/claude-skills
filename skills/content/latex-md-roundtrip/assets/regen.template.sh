#!/usr/bin/env bash
# Regenerates OUTPUT_TEX from EDIT_MD and produces the review diff vs SOURCE_TEX.
# Generated from latex-md-roundtrip skill assets/regen.template.sh
# Placeholders {{EDIT_MD}}, {{OUTPUT_TEX}}, {{TEMPLATE_TEX}}, {{SOURCE_TEX}} are
# substituted at setup time. OUTPUT_TEX can also be overridden per-run via
# the first positional argument (lets you keep one regen.sh and pick the
# content-driven output name per cycle).
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

EDIT_MD="{{EDIT_MD}}"
TEMPLATE_TEX="{{TEMPLATE_TEX}}"
SOURCE_TEX="{{SOURCE_TEX}}"
OUTPUT_TEX="${1:-{{OUTPUT_TEX}}}"

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
