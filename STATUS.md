# STATUS.md — Downloads & Desktop Taming Handbook

Last updated: 2026-10-29

## What was built

A complete, tested, ADHD-friendly manual for taming the two messiest folders
on any computer — **Downloads** and **Desktop** — delivered as Markdown source
in `docs/` plus a generated static HTML site in `site/`.

### Content (all seven required topics + the three reference artifacts)

| Required topic | Where it lives |
| --- | --- |
| Why Downloads and Desktop pile up | `docs/01-why-it-piles-up.md` (conveyor belt vs. low shelf; the ADHD layer; the three homes) |
| Ten-minute weekly reset ritual | `docs/02-ten-minute-weekly-reset.md` + `docs/checklist-reset-day.md` |
| One-decision triage rules | `docs/03-one-decision-triage.md` (six gates) + `docs/decision-card.md` |
| Naming that survives years | `docs/04-naming-that-survives.md` (ISO dates, search-intent naming) |
| Safe delete vs. archive (installers, duplicates) | `docs/05-safe-delete-vs-archive.md` |
| Rescue plan for thousands of files | `docs/06-the-rescue-plan.md` (category-first, 30–45 min sessions) |
| Where local AI triage honestly helps | `docs/07-local-ai-triage.md` (reading assistant, never deleter) |
| Reset-day checklist | `docs/checklist-reset-day.md` (checkbox ritual, 4 steps) |
| Decision card | `docs/decision-card.md` (six gates on one page, print-friendly) |
| Glossary | `docs/glossary.md` (17 plain-English terms) |

### Infrastructure

- `build.py` — zero-install build script (Python stdlib + the `markdown`
  package). Renders `docs/*.md` → `site/*.html` with a shared warm,
  low-stimulation stylesheet (no JavaScript, print styles included, offline-
  friendly), rewrites internal `.md` links to `.html`, adds nav, prev/next
  pager, and heading anchor ids.
- `tests/test_build.py` — 23-test unittest suite covering build output,
  link/anchor integrity, content promises (six gates, five destinations,
  checkbox count, glossary terms), determinism, stray non-Latin character
  detection, secret scanning, and LICENSE/README attribution.
- `Makefile` — `make build`, `make test`, `make clean`, `make check`.
- `README.md`, `LICENSE` (MIT, `Copyright (c) 2026 Asdale Dynamics, LLC`),
  `STATUS.md` (this file).

### Companion guides

Referenced (as text, not fake links) in `docs/index.md`, `README.md`, and
`docs/07-local-ai-triage.md`: **local-file-organizer-cli** and
**second-brain-basics-guide**. The handbook stands alone without them.

## How to run it

```bash
pip install markdown        # only dependency
python3 build.py            # builds site/ from docs/
python3 -m unittest discover -s tests -v   # run the 23-test suite
open/xdg-open site/index.html              # read the site
```

Or `make check` for build + tests in one line.

## Verification results

- `python3 build.py` — builds 11 pages + `style.css` into `site/`; exit 0.
- `python3 -m unittest discover -s tests` — **23 tests, 0 failures**:
  - every expected page generated, no unrendered placeholders
  - every internal `href` resolves; every `#anchor` matches a real heading id
  - no raw `.md` links survive in HTML; nav marks current page
  - six gates present in Chapter 3; six numbered rows on the decision card
  - checklist ≥ 15 checkboxes, 4 steps, "10 minutes" present
  - glossary defines all core terms; chapters carry their key concepts
  - no CJK/other stray script characters anywhere (a real bug class we caught
    and fixed in three files during development)
  - no secret-shaped strings in any text file
  - build is deterministic (byte-identical across runs)
  - LICENSE contains the exact required line; README credits
    Asdale Dynamics, LLC and documents `python3 build.py`
- Manual check: rendered pages spot-read for tone, table rendering, emoji
  table destinations, and mobile viewport meta.
- Verified commands: `python3 build.py` and `python3 -m unittest discover -s
  tests` (exact invocations above). `make` was not installed in the
  development environment, so the Makefile targets mirror those commands
  textually but were not executed here.

## Known gaps / honest limitations

- The build has **one** dependency (`markdown`); if it's missing the build
  fails loudly with instructions (`pip install markdown`) rather than silently.
- Tasks `- [ ]` render as literal `[ ]` list text (python-markdown has no
  task-list syntax without pymdown-extensions, which we deliberately avoided
  to stay zero-install). It's readable; checkboxes are styled via CSS only if
  ever upgraded.
- Site section ids come from the `toc` extension's slugification — very
  long headings produce long ids. Cosmetic only.
- The decision card and checklist are separate pages; a combined printable
  one-pager could be added later.
- No search box in the static site (browser Ctrl+F works fine for an 11-page
  site); could be added if the handbook grows.
- Companion projects (`local-file-organizer-cli`,
  `second-brain-basics-guide`) are referenced by name only — they're separate
  repos, intentionally not linked to guessed URLs.
