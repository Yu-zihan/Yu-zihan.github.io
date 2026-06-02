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

mkdir -p \
  "$TARGET_DIR/assets" \
  "$TARGET_DIR/blog" \
  "$TARGET_DIR/notes"

cp "$SOURCE_DIR/index.html" "$TARGET_DIR/index.html"
cp "$SOURCE_DIR/blog/index.html" "$TARGET_DIR/blog/index.html"
cp "$SOURCE_DIR/notes/index.html" "$TARGET_DIR/notes/index.html"
cp "$SOURCE_DIR/assets/home.css" "$TARGET_DIR/assets/home.css"
cp "$SOURCE_DIR/assets/notes.css" "$TARGET_DIR/assets/notes.css"
cp "$SOURCE_DIR/assets/notes.js" "$TARGET_DIR/assets/notes.js"
cp "$SOURCE_DIR/assets/favicon.ico" "$TARGET_DIR/assets/favicon.ico"
cp "$SOURCE_DIR/assets/favicon.png" "$TARGET_DIR/assets/favicon.png"
cp "$SOURCE_DIR/assets/profile.jpg" "$TARGET_DIR/assets/profile.jpg"
