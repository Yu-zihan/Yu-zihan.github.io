# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal academic blog for Zihan Yu, built with **Kodama** — a Typst-friendly static Zettelkästen site generator. The `kodama/` subdirectory is the generator's Rust source. Content lives in `trees/`. Built output goes to `publish/`.

## Commands

All commands must be run from `kodama/` (the Rust crate root), pointing at the config one level up.

```bash
# Live preview at http://127.0.0.1:8088
cd /Users/yzh/Desktop/Code/Blog/Blog/kodama
cargo run -- serve -c ../Kodama.toml -v

# Static build → publish/
cd /Users/yzh/Desktop/Code/Blog/Blog/kodama
cargo run -- build -c ../Kodama.toml -v

# Validate without producing output
cargo run -- check -c ../Kodama.toml
```

Run Kodama's own tests:
```bash
cd /Users/yzh/Desktop/Code/Blog/Blog/kodama
cargo test
```

## Content structure

```
trees/
  index.md          # home page (type: page)
  about-me.md       # about page (type: page)
  blog/             # blog posts (type: blog)
  notes/            # notes (type: note)
  projects/         # projects (type: project)
  _lib/kodama.typ   # Typst helper library (math, subtrees, etc.)
```

Every content file begins with YAML frontmatter. Supported fields in academic mode:

```yaml
---
title: "..."
date: YYYY-MM-DD
type: blog | note | project | reading | paper | page
tags: comma, separated
summary: "..."
draft: false
---
```

## Architecture overview

`Kodama.toml` is the single source of truth for site config (trees dir, output dir, academic mode, serve command, etc.). The `[academic]` section enables the homepage/blog/notes/projects routing layer.

**Kodama Rust pipeline** (`kodama/src/`):
- `main.rs` — CLI entry point; dispatches `new / init / build / check / serve / snip / upgrade`
- `compiler/` — core compilation pipeline: Markdown parsing (`parser/`), Typst compilation (`typst.rs`), section graph resolution, incremental rebuild (`incremental.rs`), RSS generation (`rss.rs`), academic-mode HTML generation (`academic.rs`)
- `config/` — `Kodama.toml` deserialization
- `entry.rs` — metadata model (frontmatter fields)
- `cli/serve/` — file-watcher + HTTP server for live preview
- `html_flake/` — HTML fragment utilities
- `process/` — external process invocation (Typst CLI, etc.)

**Typst support**: `.typ` files in `trees/` are compiled via the Typst CLI installed on the system. `trees/_lib/kodama.typ` provides the `#kodama()` document wrapper and helpers: `#metadata()`, `#subtree()`, `#embed()`, `#local()`, and math layout fixups for inline SVG rendering. Math in Markdown uses `$...$` (inline) and `$$...$$` (block); `import-math.html` injects the MathJax/KaTeX loader.

**Output**: `publish/` contains the deployable static site (HTML, `kodama.json` graph, `kodama.graph.json`, `rss.xml`). Serve mode writes to `.cache/publish` instead and is ephemeral — ignore `/tmp/kodama-academic-preview`.
