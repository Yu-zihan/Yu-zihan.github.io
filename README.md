# Academic Homepage with Notes

This repository contains a small English academic homepage with linked notes and essays, built on top of a local Kodama checkout.

## Structure

- `trees/en/`: English generated content source
- `drafts/`: unpublished material
- `assets/`: static assets, including local KaTeX files
- `site-overrides/`: hand-authored homepage files copied over the generated output
- `publish/`: generated deployable site output
- `scripts/`: preview and build entrypoints
- `.tools/kodama/`: local Kodama source used to build and serve the site

## Content Layout

```text
trees/
  en/
    blog/
    notes/
  _lib/kodama.typ
```

Use `type: note` for notes pages and `type: blog` for essays.

The public homepage is maintained separately from the generated notes pages. `site-overrides/` mirrors the output structure and is copied into `publish/` after each build, so `/` and `/en/` can behave like a personal academic homepage instead of inheriting the raw notes-site layout.

## Daily Workflow

Preview locally:

```bash
./scripts/serve-site.sh
```

Build the deployable site:

```bash
./scripts/build-site.sh
```

## Notes

- Math rendering is configured in `import-math.html`.
- Kodama generates the note and essay pages under `publish/en/`.
- `scripts/apply-overrides.sh` overlays the hand-authored homepage and archive index files onto both `publish/` and the local preview output, and removes stale routes that are no longer part of the public site.
- Generated cache output under `.cache/` is disposable.
