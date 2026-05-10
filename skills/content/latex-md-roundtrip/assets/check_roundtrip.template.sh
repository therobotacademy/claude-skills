#!/usr/bin/env bash
# Validates that BASELINE_MD round-trips cleanly to LaTeX.
# Generated from latex-md-roundtrip skill assets/check_roundtrip.template.sh
# Placeholders {{SOURCE_TEX}}, {{BASELINE_MD}}, {{TEMPLATE_TEX}} are substituted at setup time.
set -euo pipefail
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
cd "$ROOT"

SOURCE_TEX="{{SOURCE_TEX}}"
BASELINE_MD="{{BASELINE_MD}}"
TEMPLATE_TEX="{{TEMPLATE_TEX}}"
TMP_TEX="$(mktemp --suffix=.tex)"
trap 'rm -f "$TMP_TEX"' EXIT

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
