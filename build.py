#!/usr/bin/env python3
"""Build the static HTML site from the Markdown handbook in docs/.

Zero-install: uses only the Python standard library plus the `markdown`
package (any 3.x version works). Run from the project root:

    python3 build.py            # build site/ from docs/
    python3 build.py --clean    # wipe site/ first, then build

Output: site/index.html ... site/glossary.html + site/style.css
Every page is self-contained HTML sharing one stylesheet, so the site works
offline from a folder, a file:// URL, or any static host.
"""

import argparse
import html
import re
import shutil
import sys
from pathlib import Path

try:
    import markdown
except ImportError:
    sys.stderr.write(
        "error: the 'markdown' package is required (pip install markdown)\n"
    )
    sys.exit(2)

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / "docs"
SITE = ROOT / "site"

# Reading order doubles as the site navigation.
PAGES = [
    ("index", "Start Here"),
    ("01-why-it-piles-up", "1. Why It Piles Up"),
    ("02-ten-minute-weekly-reset", "2. Ten-Minute Reset"),
    ("03-one-decision-triage", "3. Triage Rules"),
    ("04-naming-that-survives", "4. Naming"),
    ("05-safe-delete-vs-archive", "5. Delete vs. Archive"),
    ("06-the-rescue-plan", "6. Rescue Plan"),
    ("07-local-ai-triage", "7. Local AI"),
    ("checklist-reset-day", "Reset-Day Checklist"),
    ("decision-card", "Decision Card"),
    ("glossary", "Glossary"),
]

MD_EXTENSIONS = ["extra", "sane_lists", "toc"]

TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="An ADHD-friendly manual for keeping Downloads and Desktop under control — ten-minute reset, one-decision triage, safe delete vs archive, and a rescue plan.">
<title>{title} — Downloads &amp; Desktop Taming Handbook</title>
<link rel="stylesheet" href="style.css">
</head>
<body>
<a class="skip" href="#content">Skip to content</a>
<header>
  <p class="bookmark"><span aria-hidden="true">\U0001f5c2\ufe0f</span> <a href="index.html">Downloads &amp; Desktop Taming Handbook</a></p>
  <nav aria-label="Site pages">
    {nav}
  </nav>
</header>
<main id="content">
{content}
</main>
<footer>
  <p class="pager">{prevnext}</p>
  <p>A beginner-friendly guide from Asdale Dynamics, LLC · <a href="https://dylanasdale.github.io">dylanasdale.github.io</a></p>
</footer>
</body>
</html>
"""

CSS = """/* Downloads & Desktop Taming Handbook — warm, low-stimulation, readable */
:root {
  --paper: #fbf7f0;
  --ink: #2f2a26;
  --muted: #6f655d;
  --accent: #b4581e;
  --accent-soft: #f3e3d3;
  --card: #fffdf9;
  --line: #e7dccd;
}
* { box-sizing: border-box; }
html { scroll-behavior: smooth; }
@media (prefers-reduced-motion: reduce) {
  html { scroll-behavior: auto; }
}
body {
  margin: 0;
  background: var(--paper);
  color: var(--ink);
  font: 18px/1.75 Georgia, "Iowan Old Style", "Times New Roman", serif;
  -webkit-font-smoothing: antialiased;
}
.skip {
  position: absolute; left: -999px; top: 0;
  background: var(--accent); color: #fff; padding: .5em 1em;
}
.skip:focus { left: 0; }
header, main, footer {
  max-width: 46rem;
  margin: 0 auto;
  padding: 0 1.25rem;
}
header {
  padding-top: 2rem;
}
header .bookmark a {
  font-size: .85rem;
  letter-spacing: .06em;
  text-transform: uppercase;
  text-decoration: none;
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
}
header .bookmark a:hover { color: var(--accent); }
nav {
  margin-top: 1.25rem;
  padding: .8rem 1rem;
  background: var(--card);
  border: 1px solid var(--line);
  border-radius: 12px;
  font-family: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  font-size: .88rem;
  line-height: 1.9;
}
nav a { color: var(--ink); text-decoration: none; }
nav a:hover, nav a[aria-current="page"] { color: var(--accent); }
nav a[aria-current="page"] {
  font-weight: 700;
  text-decoration: underline;
  text-decoration-thickness: 2px;
}
main {
  padding-top: 1.75rem;
  padding-bottom: 3rem;
}
h1, h2, h3, h4 {
  font-family: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  line-height: 1.3;
  font-weight: 700;
  overflow-wrap: break-word;
}
h1 { font-size: 2rem; margin: 1rem 0 1.5rem; letter-spacing: -0.015em; }
h2 { font-size: 1.4rem; margin: 2em 0 .6em; letter-spacing: -0.01em; }
h3 { font-size: 1.12rem; margin: 1.8em 0 .5em; }
h4 { font-size: 1rem; margin: 1.6em 0 .4em; }
a { color: var(--accent); }
a:hover { text-decoration-thickness: 2px; }
hr {
  border: 0;
  border-top: 1px solid var(--line);
  margin: 2.5em 0;
}
blockquote {
  margin: 1.5em 0;
  padding: 1em 1.4em;
  background: var(--accent-soft);
  border-left: 4px solid var(--accent);
  border-radius: 0 10px 10px 0;
}
blockquote p { margin: .25em 0; }
code, pre {
  font: .88em/1.6 ui-monospace, "SFMono-Regular", Consolas, monospace;
}
code {
  background: var(--accent-soft);
  padding: .1em .35em;
  border-radius: 5px;
}
pre {
  background: #2f2a26;
  color: #f4efe8;
  padding: 1em 1.2em;
  border-radius: 10px;
  overflow-x: auto;
}
pre code { background: none; padding: 0; color: inherit; }
table {
  border-collapse: collapse;
  width: 100%;
  margin: 1.5em 0;
  font-size: .95rem;
}
th, td {
  border: 1px solid var(--line);
  padding: .55em .75em;
  text-align: left;
  vertical-align: top;
}
th { background: var(--accent-soft); }
tr:nth-child(even) td { background: var(--card); }
li { margin: .4em 0; }
li p { margin: .35em 0; }
footer {
  color: var(--muted);
  font-family: ui-sans-serif, system-ui, "Segoe UI", sans-serif;
  font-size: .85rem;
  padding-bottom: 3rem;
}
footer .pager { display: flex; flex-wrap: wrap; justify-content: space-between; gap: .5rem 1rem; }
footer .pager a { color: var(--accent); text-decoration: none; }
footer .pager a:hover { text-decoration: underline; }
@media print {
  header nav, footer, .skip { display: none; }
  body { background: #fff; font-size: 12pt; }
  a { color: inherit; text-decoration: none; }
  pre, blockquote, table { break-inside: avoid; }
}
"""


def page_title(md_text: str, slug: str, label: str) -> str:
    """First H1 (minus any 'Chapter N:' prefix) or the nav label."""
    m = re.search(r"^# (.+)$", md_text, flags=re.M)
    if not m:
        return label
    title = m.group(1).strip()
    if ":" in title:
        title = title.split(":", 1)[1].strip()
    return title or label


def convert(md_text: str) -> str:
    """Markdown -> HTML. The toc extension also assigns heading ids."""
    rendered = markdown.Markdown(extensions=MD_EXTENSIONS).convert(md_text)
    # Internal links were written against the docs/ tree (.md); the site serves
    # .html pages, so rewrite same-directory doc links (keeps #anchors intact).
    return re.sub(r'(href=")([A-Za-z0-9-]+)(\.md)([#"])', r"\1\2.html\4", rendered)


def render_page(slug: str, label: str, idx: int) -> str:
    src = DOCS / f"{slug}.md"
    if not src.is_file():
        raise SystemExit(f"error: missing source doc {src}")
    md_text = src.read_text(encoding="utf-8")
    title = page_title(md_text, slug, label)
    content = convert(md_text)

    nav_items = []
    for other, other_label in PAGES:
        current = ' aria-current="page"' if other == slug else ""
        nav_items.append(
            f'<a href="{other}.html"{current}>{html.escape(other_label)}</a>'
        )
    nav = " · ".join(nav_items)

    pager = ['<span class="spacer"></span>']
    if idx > 0:
        prev_slug, prev_label = PAGES[idx - 1]
        pager.insert(0, f'<a href="{prev_slug}.html">← {html.escape(prev_label)}</a>')
    if idx < len(PAGES) - 1:
        next_slug, next_label = PAGES[idx + 1]
        pager.append(f'<a href="{next_slug}.html">{html.escape(next_label)} →</a>')

    return TEMPLATE.format(
        title=html.escape(title),
        nav=nav,
        content=content,
        prevnext="".join(pager),
    )


def build(clean: bool = False) -> list[str]:
    if not DOCS.is_dir():
        raise SystemExit("error: docs/ not found — run from the project root")
    if clean and SITE.is_dir():
        shutil.rmtree(SITE)
    SITE.mkdir(exist_ok=True)
    (SITE / "style.css").write_text(CSS, encoding="utf-8")
    written = []
    for idx, (slug, label) in enumerate(PAGES):
        out = SITE / f"{slug}.html"
        out.write_text(render_page(slug, label, idx), encoding="utf-8")
        written.append(str(out.relative_to(ROOT)))
    print(f"built {len(written)} pages + style.css into site/")
    for name in written:
        print(f"  {name}")
    return written


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--clean", action="store_true", help="remove site/ before building")
    args = ap.parse_args()
    build(clean=args.clean)


if __name__ == "__main__":
    main()
