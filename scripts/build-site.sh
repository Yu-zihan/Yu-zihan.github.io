#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

cd "$ROOT/.tools/kodama"
cargo run -- build -c "$ROOT/Kodama.toml" -v --no-indexes --no-graph

"$ROOT/scripts/apply-overrides.sh" "$ROOT/docs"
