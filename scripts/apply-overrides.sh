#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT/site-overrides"
TARGET_DIR="${1:-$ROOT/docs}"

mkdir -p "$TARGET_DIR"
rm -rf \
  "$TARGET_DIR/zh" \
  "$TARGET_DIR/about.html" \
  "$TARGET_DIR/blog/reading-math-papers.html" \
  "$TARGET_DIR/notes/research-notes.html" \
  "$TARGET_DIR/assets/profile-placeholder.svg"
cp -R "$SOURCE_DIR"/. "$TARGET_DIR"/
