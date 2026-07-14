#!/usr/bin/env python3
from __future__ import annotations

import html
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "trees" / "notes"
OUTPUT_DIR = ROOT / "site-overrides" / "zh" / "notes"
ASSET_VERSION = "zh-toc-loose"


@dataclass(frozen=True)
class Note:
    source: str
    output: str
    title: str
    date: str
    tag: str
    summary: str


NOTES = [
    Note(
        source="从最小可计算模型开始.md",
        output="one_neuron_1.html",
        title="从单个神经元开始",
        date="2026-07-01",
        tag="深度学习",
        summary="第 1 部分：从最小的可计算模型到 XOR",
    ),
    Note(
        source="Kantorovich 对偶.md",
        output="kantorovich_duality.html",
        title="Kantorovich 对偶",
        date="2026-06-05",
        tag="最优传输",
        summary="关于 Kantorovich 对偶推导和含义的整理",
    ),
    Note(
        source="熵正则最优传输.md",
        output="entropic_regularized_optimal_transport.html",
        title="熵正则化最优传输",
        date="2026-06-02",
        tag="最优传输",
        summary="关于熵正则化最优传输的一些个人笔记",
    ),
]


def slugify(text: str, used: dict[str, int]) -> str:
    base = re.sub(r"[\s_]+", "-", text.strip().lower())
    base = re.sub(r"[^\w\-\u4e00-\u9fff]+", "", base)
    base = re.sub(r"-+", "-", base).strip("-") or "section"
    count = used.get(base, 0)
    used[base] = count + 1
    return base if count == 0 else f"{base}-{count + 1}"


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
                code_lines.append(lines[i])
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


def render_page(note: Note) -> str:
    markdown = (SOURCE_DIR / note.source).read_text(encoding="utf-8")
    body = render_blocks(markdown)
    title = html.escape(note.title)
    summary = html.escape(note.summary)
    tag = html.escape(note.tag)

    return f"""<!DOCTYPE html>
<html lang="zh-CN" class="notes-site notes-article">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <link rel="icon" href="/assets/favicon.ico">
    <link rel="stylesheet" href="/assets/notes.css?v={ASSET_VERSION}">
    <link rel="stylesheet" href="/assets/vendor/katex/katex.min.css">
    <script defer src="/assets/notes.js?v={ASSET_VERSION}"></script>
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
      <nav id="toc" class="sticky-nav mobile-sticky-nav"></nav>
      <article>
        <section class="block">
          <details open>
            <summary>
              <header>
                <h1>{title}</h1>
                <div class="metadata">
                  <ul>
                    <li class="meta-item">{note.date}</li>
                    <li class="meta-item">笔记</li>
                    <li class="meta-item">{tag}</li>
                    <li class="meta-item">{summary}</li>
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


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for note in NOTES:
        (OUTPUT_DIR / note.output).write_text(render_page(note), encoding="utf-8")


if __name__ == "__main__":
    main()
