#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PREVIEW_DIR="$ROOT/.cache/preview"

cd "$ROOT/.tools/kodama"
cargo run -- serve -c "$ROOT/Kodama.toml" -v &
SERVER_PID=$!

cleanup() {
  kill "$SERVER_PID" 2>/dev/null || true
}

trap cleanup EXIT

while kill -0 "$SERVER_PID" 2>/dev/null; do
  "$ROOT/scripts/apply-overrides.sh" "$PREVIEW_DIR"
  sleep 1
done

wait "$SERVER_PID"
