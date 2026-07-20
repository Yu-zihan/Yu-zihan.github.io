#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "trees" / "notes"
EN_OUTPUT_DIR = ROOT / "site-overrides" / "notes"
ZH_OUTPUT_DIR = ROOT / "site-overrides" / "zh" / "notes"
ASSET_VERSION = "notes-mobile"

TAG_SLUGS = {
    "Deep learning": "deep-learning",
    "Optimal transport": "optimal-transport",
    "深度学习": "deep-learning",
    "最优传输": "optimal-transport",
}

LANGUAGE_SETTINGS = {
    "en": {
        "html_lang": "en-US",
        "output_dir": EN_OUTPUT_DIR,
        "kind": "note",
        "archive_title": "Notes archive",
        "archive_description": "Research notes by Zihan Yu.",
        "archive_intro": "Working notes and topic pages.",
        "archive_nav_label": "Archive sections",
        "archive_links": [
            ("/", "Home"),
            ("/notes/index.html", "Notes"),
            ("/blog/index.html", "Essays"),
            ("/zh/notes/index.html", "中文"),
        ],
        "archive_path": "/notes/index.html",
        "filter_label": "Filter",
        "all_label": "All",
        "known_tags": [("deep-learning", "Deep learning"), ("optimal-transport", "Optimal transport")],
        "article_class": "notes-site notes-article notes-article-legacy",
        "archive_class": "notes-site notes-list",
        "font_links": True,
    },
    "zh": {
        "html_lang": "zh-CN",
        "output_dir": ZH_OUTPUT_DIR,
        "kind": "笔记",
        "archive_title": "笔记归档",
        "archive_description": "于子涵的中文笔记归档。",
        "archive_intro": "一些学习笔记、阅读记录和主题整理。",
        "archive_nav_label": "归档导航",
        "archive_links": [
            ("/", "主页"),
            ("/zh/notes/index.html", "笔记"),
            ("/notes/index.html", "English"),
        ],
        "archive_path": "/zh/notes/index.html",
        "filter_label": "筛选",
        "all_label": "全部",
        "known_tags": [("deep-learning", "深度学习"), ("optimal-transport", "最优传输")],
        "article_class": "notes-site notes-article",
        "archive_class": "notes-site notes-list",
        "font_links": False,
    },
}


@dataclass(frozen=True)
class NoteEntry:
    source: str
    output: str
    lang: str


@dataclass(frozen=True)
class Note:
    source: str
    output: str
    title: str
    date: str
    tag: str
    summary: str
    lang: str

    @property
    def tag_slug(self) -> str:
        return TAG_SLUGS.get(self.tag, slugify_plain(self.tag))


# This list is the public archive source of truth. Files can remain in
# trees/notes while staying unpublished if they are not listed here.
NOTE_ENTRIES = [
    NoteEntry("neuron_wave_tactic.md", "neuron_wave_tactic.html", "en"),
    NoteEntry("one_neuron_1.md", "one_neuron_1.html", "en"),
    NoteEntry("kantorovich_duality.md", "kantorovich_duality.html", "en"),
    NoteEntry("entropic_regularized_optimal_transport.md", "entropic_regularized_optimal_transport.html", "en"),
    NoteEntry("元海战术行不行.md", "neuron_wave_tactic.html", "zh"),
    NoteEntry("从最小可计算模型开始.md", "one_neuron_1.html", "zh"),
    NoteEntry("Kantorovich 对偶.md", "kantorovich_duality.html", "zh"),
    NoteEntry("熵正则最优传输.md", "entropic_regularized_optimal_transport.html", "zh"),
]


LEGACY_ARTICLE_CSS = """
<style>
  html {
    font-size: 18px;
  }

  :root body {
    color-scheme: light dark;
    --content-gap: 15px;
    --radius: 5px;
    --article-max-width: 90ex;
    --toc-max-width: 90ex;
    --text-font-family: "Inria Sans", sans-serif;
    --kaiti-font-family: "LXGW WenKai TC", "FandolKai", "KaiTi", "SimKai", "STKaiti", "Kaiti SC", "Kaiti TC", "华文楷体", "楷体", serif;
    --pre-font-size: 1rem;
    --code-font-size: 1rem;
    --katex-font-size: 1em;
    --katex-frac-line-font-size: 1.25em;
    --details-h1-font-size: 1.2rem;
    --article-details-h1-font-size: 1.5rem;
    --article-details-h1-taxon-font-size: 1.35rem;
    --logo-font-size: 1.5rem;
    --p-line-height: 1.55rem;
    --text-color: black;
    --toc-link-color: #555;
    --background-color: white;
    --background-color-pre: rgba(0, 100, 100, 0.04);
    --background-color-code: rgba(0, 100, 100, 0.04);
    --hover-color-block: rgba(0, 100, 255, 0.04);
    --hover-color-link: rgba(0, 100, 255, 0.1);
    --target-color: rgb(67, 92, 255);
    --link-color: black;
    --slug-color: gray;
    --logo-color: #666;
    --logo-hover-color: #aaa;
    --span-taxon-color: #444;
    --article-taxon-color: #888;
    --mark-color: rgb(255, 255, 151);
    --em-color: var(--text-color);
    --alert-border-color: gray;
  }

  body {
    color: var(--text-color);
    font-optical-sizing: auto;
    font-size: 1rem;
    font-family: var(--text-font-family);
    hyphens: auto;
    background-color: var(--background-color);
  }

  p,
  pre {
    line-height: var(--p-line-height);
  }

  pre {
    border-radius: var(--radius);
    background-color: var(--background-color-pre);
    padding: 0.5rem;
    font-size: var(--pre-font-size);
    margin-top: 0;
    overflow-x: auto;
    white-space: pre-wrap;
    overflow-wrap: break-word;
  }

  code {
    border-radius: var(--radius);
    background-color: var(--background-color-code);
    padding: 0.1rem;
    font-size: var(--code-font-size);
  }

  pre,
  code {
    font-family: monospace;
  }

  .table-wrap {
    max-width: 100%;
    overflow-x: auto;
  }

  table {
    border-collapse: separate;
    border-spacing: 0 5px;
    margin-bottom: 1rem;
    display: block;
    white-space: nowrap;
    overflow-x: auto;
    overflow-y: hidden;
  }

  th {
    font-weight: normal;
    text-align: left;
  }

  th,
  td {
    padding: 0 15px;
    vertical-align: top;
  }

  pre > code {
    border-radius: 0;
    background-color: transparent;
    padding: 0;
  }

  .math.math-display,
  .katex-display {
    display: block;
    margin: 0.55rem 0 0.65rem;
    overflow-x: auto;
    overflow-y: hidden;
    padding: 0.05rem 0.1rem 0.12rem;
  }

  .katex-display > .katex {
    min-width: fit-content;
    padding-top: 1px;
    padding-bottom: 1px;
  }

  h1,
  h2,
  h3,
  h4 {
    margin-top: 0.5em;
  }

  h1,
  h2,
  h3,
  h4,
  h5,
  h6 {
    font-weight: 500;
    margin-bottom: 0;
  }

  h5,
  h6,
  p {
    margin-top: 0;
  }

  details > summary {
    list-style-type: none;
    outline: none;
  }

  details > summary > header {
    display: inline;
  }

  details > summary::marker,
  details > summary::-webkit-details-marker {
    display: none;
  }

  details h1 {
    font-size: var(--details-h1-font-size);
    display: inline;
  }

  span.taxon {
    color: var(--span-taxon-color);
    font-weight: 500;
  }

  article > section > details > summary > header > h1 {
    font-size: var(--article-details-h1-font-size);
  }

  article > section > details > summary > header {
    display: block;
    margin-bottom: 0.5em;
  }

  section.block > details {
    margin-bottom: 0.4em;
  }

  section.block > details[open] {
    margin-bottom: 1em;
  }

  .block {
    padding-left: 5px;
    padding-right: 10px;
    padding-bottom: 2px;
    border-radius: var(--radius);
  }

  .block:hover {
    background-color: var(--hover-color-block);
  }

  img {
    object-fit: cover;
    max-width: 100%;
  }

  hr {
    margin-top: 10px;
    margin-bottom: 20px;
    background-color: gray;
    border: 0 none;
    width: 100%;
    height: 1pt;
  }

  ul,
  ol {
    margin-top: 1em;
    margin-bottom: 1em;
  }

  .metadata ul {
    padding-left: 0;
    display: inline;
  }

  .metadata li::after {
    content: " · ";
  }

  .metadata li:last-child::after {
    content: "";
  }

  .metadata * {
    display: inline;
  }

  a {
    color: var(--link-color);
    text-decoration: inherit;
  }

  .slug,
  .edit {
    color: var(--slug-color);
    font-weight: 200;
  }

  #grid-wrapper > article {
    max-width: var(--article-max-width);
    margin-right: auto;
    grid-area: article;
  }

  nav#toc ul {
    list-style-type: none;
  }

  nav#toc li > ul {
    margin: 0;
    padding-left: 1rem;
  }

  nav#toc,
  nav#toc a {
    color: var(--toc-link-color);
  }

  nav#toc {
    grid-area: toc;
  }

  @media only screen and (min-width: 1000px) {
    body {
      margin-top: 2rem;
      margin-left: 2rem;
      transition: ease all 0.2s;
    }

    #grid-wrapper {
      display: grid;
      grid-auto-flow: column;
      grid-template-columns: var(--article-max-width) var(--toc-max-width);
    }

    .sticky-nav {
      position: sticky;
      top: 0;
      max-height: 100vh;
      overflow-y: auto;
      scrollbar-width: thin;
    }

    nav#toc {
      max-width: 45ex;
    }
  }

  @media only screen and (max-width: 1000px) {
    :root body {
      --code-font-size: 0.9rem;
    }

    .block {
      padding-left: 2px;
      padding-right: 2px;
      padding-bottom: 2px;
      border-radius: 5px;
    }

    .mobile-sticky-nav {
      position: sticky;
      top: 0;
      max-height: 100vh;
      overflow-y: auto;
      scrollbar-width: thin;
      background-color: var(--background-color);
      z-index: 7;
      border-bottom: solid var(--text-color);
    }
  }

  article {
    font-size: 19px;
    line-height: 1.78;
  }

  article h1 {
    font-size: 2.35rem;
    line-height: 1.15;
  }

  article h2 {
    font-size: 1.5rem;
    line-height: 1.2;
  }

  article h3 {
    font-size: 1.25rem;
    line-height: 1.25;
  }

  article p,
  article li {
    margin-bottom: 0.72em;
  }

  article pre {
    padding: 1.2rem;
  }
</style>
"""


def slugify_plain(text: str) -> str:
    slug = text.strip().lower().replace("&", "and")
    slug = re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "-", slug)
    return slug.strip("-") or "tag"


def slugify(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"[\s_]+", "-", text.strip().lower())
    base = re.sub(r"[^\w\-\u4e00-\u9fff]+", "", base)
    base = re.sub(r"-+", "-", base).strip("-") or "section"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else f"{base}-{count + 1}"


def strip_wrapping_quotes(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def split_frontmatter(markdown: str) -> tuple[dict[str, str], str]:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, markdown

    end = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end = index
            break

    if end is None:
        return {}, markdown

    frontmatter: dict[str, str] = {}
    for line in lines[1:end]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        frontmatter[key.strip()] = strip_wrapping_quotes(value)

    body = "\n".join(lines[end + 1 :]).lstrip("\n")
    return frontmatter, body


def protect_inline(text: str, pattern: re.Pattern[str], renderer) -> tuple[str, dict[str, str]]:
    placeholders: dict[str, str] = {}

    def replace(match: re.Match[str]) -> str:
        key = f"\u0000{len(placeholders)}\u0000"
        placeholders[key] = renderer(match)
        return key

    return pattern.sub(replace, text), placeholders


def restore_placeholders(text: str, placeholders: dict[str, str]) -> str:
    for key, value in placeholders.items():
        text = text.replace(key, value)
    return text


def render_inline(text: str) -> str:
    code_pattern = re.compile(r"`([^`]+)`")
    double_dollar_pattern = re.compile(r"(?<!\\)\$\$(.+?)(?<!\\)\$\$")
    math_pattern = re.compile(r"(?<![\\$])\$(?!\$)(.+?)(?<![\\$])\$(?!\$)")
    link_pattern = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
    raw_url_pattern = re.compile(r"(?<![\"'=])(https?://[^\s<]+)")

    text, code = protect_inline(
        text,
        code_pattern,
        lambda match: f"<code>{html.escape(match.group(1))}</code>",
    )
    text, double_dollar_math = protect_inline(
        text,
        double_dollar_pattern,
        lambda match: f'<span class="math math-inline">{html.escape(match.group(1))}</span>',
    )
    text, math = protect_inline(
        text,
        math_pattern,
        lambda match: f'<span class="math math-inline">{html.escape(match.group(1))}</span>',
    )
    text, links = protect_inline(
        text,
        link_pattern,
        lambda match: (
            f'<a href="{html.escape(match.group(2), quote=True)}">'
            f"{html.escape(match.group(1))}</a>"
        ),
    )

    text = html.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = raw_url_pattern.sub(
        lambda match: (
            f'<a href="{match.group(1).rstrip(".,;，。；")}" rel="noopener">'
            f'{match.group(1).rstrip(".,;，。；")}</a>'
            f'{match.group(1)[len(match.group(1).rstrip(".,;，。；")):]}'
        ),
        text,
    )

    for placeholders in (links, math, double_dollar_math, code):
        text = restore_placeholders(text, placeholders)
    return text


def is_table_start(lines: list[str], index: int) -> bool:
    if index + 1 >= len(lines):
        return False
    first = lines[index].strip()
    second = lines[index + 1].strip()
    return first.startswith("|") and first.endswith("|") and bool(
        re.match(r"^\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)+\|?$", second)
    )


def split_table_row(line: str) -> list[str]:
    stripped = line.strip().strip("|")
    return [cell.strip() for cell in stripped.split("|")]


def render_table(lines: list[str]) -> str:
    headers = split_table_row(lines[0])
    rows = [split_table_row(line) for line in lines[2:]]
    header_html = "".join(f"<th>{render_inline(cell)}</th>" for cell in headers)
    row_html = []
    for row in rows:
        cells = "".join(f"<td>{render_inline(cell)}</td>" for cell in row)
        row_html.append(f"<tr>{cells}</tr>")
    return (
        '<div class="table-wrap"><table>'
        f"<thead><tr>{header_html}</tr></thead>"
        f"<tbody>{''.join(row_html)}</tbody>"
        "</table></div>"
    )


def normalize_heading(text: str) -> str:
    return re.sub(r"^(\d+)\.\s+(\d+)\s*", r"\1.\2 ", text.strip())


def render_blocks(markdown: str) -> str:
    lines = markdown.splitlines()
    blocks: list[str] = []
    used_slugs: dict[str, int] = {}
    i = 0

    while i < len(lines):
        raw = lines[i]
        stripped = raw.strip()

        if not stripped:
            i += 1
            continue

        if stripped.startswith("```"):
            language = stripped.removeprefix("```").strip()
            code_lines: list[str] = []
            i += 1
            while i < len(lines) and not lines[i].strip().startswith("```"):
                code_lines.append(lines[i].rstrip())
                i += 1
            i += 1
            class_name = f' class="language-{html.escape(language)}"' if language else ""
            blocks.append(f"<pre><code{class_name}>{html.escape(chr(10).join(code_lines))}</code></pre>")
            continue

        if stripped.startswith("$$"):
            math_lines: list[str] = []
            rest = stripped[2:]
            if rest.endswith("$$") and rest[:-2].strip():
                math_lines.append(rest[:-2].strip())
                i += 1
            else:
                if rest.strip():
                    math_lines.append(rest.strip())
                i += 1
                while i < len(lines):
                    candidate = lines[i].strip()
                    if candidate.endswith("$$"):
                        math_lines.append(candidate[:-2].strip())
                        i += 1
                        break
                    math_lines.append(lines[i].strip())
                    i += 1
            math = "\n".join(line for line in math_lines if line)
            blocks.append(f'<div class="math math-display">{html.escape(math)}</div>')
            continue

        heading = re.match(r"^(#{1,6})\s+(.+)$", stripped)
        if heading:
            level = min(len(heading.group(1)), 3)
            text = normalize_heading(heading.group(2))
            slug = slugify(text, used_slugs)
            blocks.append(f'<h{level} id="{slug}">{render_inline(text)}</h{level}>')
            i += 1
            continue

        bold_heading = re.match(r"^\*\*(.+?)\*\*$", stripped)
        if bold_heading:
            text = normalize_heading(bold_heading.group(1))
            slug = slugify(text, used_slugs)
            blocks.append(f'<h2 id="{slug}">{render_inline(text)}</h2>')
            i += 1
            continue

        if stripped == "---":
            blocks.append("<hr>")
            i += 1
            continue

        if is_table_start(lines, i):
            table_lines = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and lines[i].strip().startswith("|") and lines[i].strip().endswith("|"):
                table_lines.append(lines[i])
                i += 1
            blocks.append(render_table(table_lines))
            continue

        if stripped.startswith(">"):
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                quote_lines.append(lines[i].strip()[1:].strip())
                i += 1
            quote = "<br>".join(render_inline(line) for line in quote_lines if line)
            blocks.append(f"<blockquote><p>{quote}</p></blockquote>")
            continue

        if re.match(r"^[-*]\s+", stripped):
            items: list[str] = []
            while i < len(lines) and re.match(r"^[-*]\s+", lines[i].strip()):
                item = re.sub(r"^[-*]\s+", "", lines[i].strip())
                items.append(f"<li>{render_inline(item)}</li>")
                i += 1
            blocks.append(f"<ul>{''.join(items)}</ul>")
            continue

        if re.match(r"^\d+\.\s+", stripped):
            items = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                item = re.sub(r"^\d+\.\s+", "", lines[i].strip())
                items.append(f"<li>{render_inline(item)}</li>")
                i += 1
            blocks.append(f"<ol>{''.join(items)}</ol>")
            continue

        paragraph_lines = [stripped]
        i += 1
        while i < len(lines):
            candidate = lines[i].strip()
            if not candidate:
                break
            if (
                candidate.startswith(("```", "$$", ">", "---"))
                or re.match(r"^(#{1,6})\s+", candidate)
                or re.match(r"^\*\*(.+?)\*\*$", candidate)
                or re.match(r"^[-*]\s+", candidate)
                or re.match(r"^\d+\.\s+", candidate)
                or is_table_start(lines, i)
            ):
                break
            paragraph_lines.append(candidate)
            i += 1
        paragraph = " ".join(paragraph_lines)
        blocks.append(f"<p>{render_inline(paragraph)}</p>")

    return "\n            ".join(blocks)


def source_path_for(entry: NoteEntry) -> Path:
    return SOURCE_DIR / entry.source


def load_note(entry: NoteEntry) -> tuple[Note, str]:
    source_path = source_path_for(entry)
    markdown = source_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(markdown)
    note = Note(
        source=entry.source,
        output=entry.output,
        title=frontmatter.get("title", source_path.stem),
        date=frontmatter.get("date", ""),
        tag=frontmatter.get("tags", ""),
        summary=frontmatter.get("summary", ""),
        lang=entry.lang,
    )
    return note, body


def render_head_extras(note: Note) -> str:
    settings = LANGUAGE_SETTINGS[note.lang]
    font_links = ""
    if settings["font_links"]:
        font_links = """
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inria+Sans:ital,wght@0,300;0,400;0,700;1,300;1,400;1,700&display=swap" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css2?family=LXGW+WenKai+TC:wght@400;700&display=swap" rel="stylesheet">"""

    legacy_css = LEGACY_ARTICLE_CSS if note.lang == "en" else ""
    return f"""{legacy_css}{font_links}
    <link rel="stylesheet" href="/assets/notes.css?v={ASSET_VERSION}">
    <script defer src="/assets/notes.js?v={ASSET_VERSION}"></script>"""


def render_article_page(note: Note, markdown_body: str) -> str:
    settings = LANGUAGE_SETTINGS[note.lang]
    html_lang = settings["html_lang"]
    kind = html.escape(settings["kind"])
    title = html.escape(note.title)
    summary = html.escape(note.summary)
    tag = html.escape(note.tag)
    body = render_blocks(markdown_body)
    slug = html.escape(note.output.removesuffix(".html"))
    summary_id = html.escape(f"{note.lang}-notes-{note.output.removesuffix('.html')}")
    page_path = "/zh/notes/" + note.output if note.lang == "zh" else "/notes/" + note.output

    return f"""<!DOCTYPE html>
<html lang="{html_lang}" class="{settings["article_class"]}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="icon" href="/assets/favicon.ico">
    <script src="/main.js"></script>
    <link rel="stylesheet" href="/assets/vendor/katex/katex.min.css">
{render_head_extras(note)}
    <script defer src="/assets/vendor/katex/katex.min.js"></script>
    <script defer src="/assets/vendor/katex/contrib/auto-render.min.js"></script>
    <script defer src="/assets/vendor/katex/contrib/copy-tex.min.js"></script>
    <script>
      document.addEventListener("DOMContentLoaded", function () {{
        if (!window.katex) return;

        document.querySelectorAll(".math.math-inline").forEach(function (el) {{
          katex.render(el.textContent, el, {{
            displayMode: false,
            throwOnError: false,
            strict: false
          }});
        }});

        document.querySelectorAll(".math.math-display").forEach(function (el) {{
          katex.render(el.textContent, el, {{
            displayMode: true,
            throwOnError: false,
            strict: false
          }});
        }});

        if (window.renderMathInElement) {{
          renderMathInElement(document.body, {{
            delimiters: [
              {{ left: "$$", right: "$$", display: true }},
              {{ left: "$", right: "$", display: false }},
              {{ left: "\\\\(", right: "\\\\)", display: false }},
              {{ left: "\\\\[", right: "\\\\]", display: true }}
            ],
            throwOnError: false
          }});
        }}
      }});
    </script>
    <script data-goatcounter="https://zihanyu.goatcounter.com/count"
            async src="//gc.zgo.at/count.js"></script>
  </head>
  <body>
    <div id="grid-wrapper" style="grid-template-areas: 'article toc';" data-base-url="/">
      <nav id="toc" class="sticky-nav mobile-sticky-nav"><div id="theme-options"></div></nav>

      <article>
        <section class="block" data-taxon="">
          <details open>
            <summary id="{summary_id}">
              <header>
                <h1><span class="taxon"></span>{title} <a class="slug" href="{html.escape(page_path)}">[{slug}]</a></h1>
                <div class="metadata">
                  <ul>
                    <li class="meta-item meta-date">{html.escape(note.date)}</li>
                    <li class="meta-item meta-kind">{kind}</li>
                    <li class="meta-item meta-tags">{tag}</li>
                    <li class="meta-item meta-summary">{summary}</li>
                  </ul>
                </div>
              </header>
            </summary>

            {body}
          </details>
        </section>
      </article>
    </div>
  </body>
</html>
"""


def render_tag_menu(settings: dict[str, object]) -> str:
    archive_path = str(settings["archive_path"])
    all_label = html.escape(str(settings["all_label"]))
    items = [f'<a class="tag-pill is-current" href="{archive_path}" data-tag-filter="all">{all_label}</a>']
    for slug, label in settings["known_tags"]:
        items.append(
            f'<a class="tag-pill" href="{archive_path}?tag={html.escape(slug)}" '
            f'data-tag-filter="{html.escape(slug)}">{html.escape(label)}</a>'
        )
    return "\n                  ".join(items)


def render_archive_page(lang: str, notes: list[Note]) -> str:
    settings = LANGUAGE_SETTINGS[lang]
    title = html.escape(str(settings["archive_title"]))
    description = html.escape(str(settings["archive_description"]))
    intro = html.escape(str(settings["archive_intro"]))
    archive_path = str(settings["archive_path"])
    filter_label = html.escape(str(settings["filter_label"]))
    all_label = html.escape(str(settings["all_label"]))
    nav_links = []

    for href, label in settings["archive_links"]:
        current = ' class="is-current"' if href == archive_path else ""
        nav_links.append(f'<a{current} href="{html.escape(href)}">{html.escape(label)}</a>')

    posts = []
    for note in notes:
        href = "/zh/notes/" + note.output if lang == "zh" else "/notes/" + note.output
        tag_href = f"{archive_path}?tag={note.tag_slug}"
        posts.append(
            f"""              <li class="post-item" data-tags="{html.escape(note.tag_slug)}">
                <div class="post-date">{html.escape(note.date)}</div>
                <a href="{html.escape(href)}">
                  {html.escape(note.title)}
                </a>
                <div class="post-summary">
                  {html.escape(note.summary)}
                </div>
                <div class="post-tags">
                  <a class="tag-pill" href="{html.escape(tag_href)}" data-tag-filter="{html.escape(note.tag_slug)}">{html.escape(note.tag)}</a>
                </div>
              </li>"""
        )

    return f"""<!DOCTYPE html>
<html lang="{settings["html_lang"]}" class="{settings["archive_class"]}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <meta name="description" content="{description}">
    <link rel="icon" href="/assets/favicon.ico">
    <link rel="stylesheet" href="/assets/notes.css?v={ASSET_VERSION}">
    <script defer src="/assets/notes.js?v={ASSET_VERSION}"></script>
    <script data-goatcounter="https://zihanyu.goatcounter.com/count"
            async src="//gc.zgo.at/count.js"></script>
  </head>
  <body>
    <div id="grid-wrapper">
      <article>
        <main class="academic">
          <header>
            <h1>{title}</h1>
            <p>{intro}</p>
            <div class="archive-toolbar">
              <nav aria-label="{html.escape(str(settings["archive_nav_label"]))}">
                {"\n                ".join(nav_links)}
              </nav>
              <details class="tag-filter" aria-label="{filter_label}">
                <summary>
                  <span class="tag-filter-label">{filter_label}</span>
                  <span class="tag-filter-current">{all_label}</span>
                </summary>
                <div class="tag-filter-menu">
                  {render_tag_menu(settings)}
                </div>
              </details>
            </div>
          </header>

          <section>
            <ul class="post-list">
{"\n".join(posts)}
            </ul>
          </section>
        </main>
      </article>
    </div>
  </body>
</html>
"""


def write_if_changed(path: Path, content: str) -> None:
    normalized = "\n".join(line.rstrip() for line in content.splitlines()) + "\n"
    if path.exists() and path.read_text(encoding="utf-8") == normalized:
        return
    path.write_text(normalized, encoding="utf-8")


def main() -> None:
    notes_by_language: dict[str, list[Note]] = {"en": [], "zh": []}

    for settings in LANGUAGE_SETTINGS.values():
        settings["output_dir"].mkdir(parents=True, exist_ok=True)

    for entry in NOTE_ENTRIES:
        note, body = load_note(entry)
        notes_by_language[entry.lang].append(note)
        output = LANGUAGE_SETTINGS[entry.lang]["output_dir"] / entry.output
        write_if_changed(output, render_article_page(note, body))

    for lang, notes in notes_by_language.items():
        output_dir = LANGUAGE_SETTINGS[lang]["output_dir"]
        write_if_changed(output_dir / "index.html", render_archive_page(lang, notes))


if __name__ == "__main__":
    main()
