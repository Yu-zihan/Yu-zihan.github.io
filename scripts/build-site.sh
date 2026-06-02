#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TEMPLATE="$ROOT/templates/note.html"
OUTPUT="$ROOT/docs"

build_dir() {
  local src="$1" out="$2"
  mkdir -p "$out"
  for md in "$src"/*.md; do
    [[ -f "$md" ]] || continue
    name=$(basename "$md" .md)
    pandoc "$md" \
      --template="$TEMPLATE" \
      --toc --toc-depth=3 \
      --katex \
      --output="$out/$name.html"
    echo "Built: $out/$name.html"
  done
}

build_dir "$ROOT/trees/notes" "$OUTPUT/notes"
build_dir "$ROOT/trees/blog"  "$OUTPUT/blog"

"$ROOT/scripts/apply-overrides.sh" "$OUTPUT"
echo "Done."
