# Downloads & Desktop Taming Handbook

*Why the two messiest folders on any computer pile up — and a kind, ADHD-friendly way to keep them from swallowing your attention.*

An ADHD-friendly manual for taming **Downloads** and **Desktop**: one
ten-minute weekly reset, one-decision triage rules, names that survive years,
a safe-delete-vs-archive policy for installers and duplicates, a rescue plan
for when the mess hits thousands of files, and an honest look at where local
AI triage actually helps — plus a reset-day checklist, a printable decision
card, and a plain-English glossary.

Written in the "like a friend would" style of Dylan Asdale's guides
([dylanasdale.github.io](https://dylanasdale.github.io)): plain English, step
by step, never condescending. Every system in the book obeys three laws for
ADHD brains — **one decision at a time, low friction, forgiveness built in**.

## What's inside

| Document | What it's for |
| --- | --- |
| [docs/index.md](docs/index.md) | Start here — how to use the handbook |
| [docs/01-why-it-piles-up.md](docs/01-why-it-piles-up.md) | The real reasons these two folders fill up |
| [docs/02-ten-minute-weekly-reset.md](docs/02-ten-minute-weekly-reset.md) | The weekly ritual that keeps you on the easy side of the curve |
| [docs/03-one-decision-triage.md](docs/03-one-decision-triage.md) | Six yes/no gates; sorting without deliberation |
| [docs/04-naming-that-survives.md](docs/04-naming-that-survives.md) | File names still readable in 2036 |
| [docs/05-safe-delete-vs-archive.md](docs/05-safe-delete-vs-archive.md) | Installers, duplicates, and what's safe to delete |
| [docs/06-the-rescue-plan.md](docs/06-the-rescue-plan.md) | Digging out of 1,000+ files without shame |
| [docs/07-local-ai-triage.md](docs/07-local-ai-triage.md) | Where a local LLM genuinely helps — and where it shouldn't touch your files |
| [docs/checklist-reset-day.md](docs/checklist-reset-day.md) | A printable, checkbox-driven version of the ten-minute reset ritual |
| [docs/decision-card.md](docs/decision-card.md) | All six gates on one page — keep it open while sorting |
| [docs/glossary.md](docs/glossary.md) | Every term, defined in plain English |

## Quick start

```bash
# build the static HTML site into site/
python3 build.py

# read it locally
open site/index.html              # macOS
xdg-open site/index.html          # Linux
start site\index.html             # Windows
```

The site is fully offline-friendly: 11 self-contained pages + one stylesheet,
no JavaScript, no fonts fetched from the network. The decision card and
checklist also print cleanly (`@media print` styles included).

To rebuild the site in [docs](docs/) editions, just edit any file in the `docs/` folder and run `python3 build.py` again. You'll need Python 3.9+ and the `markdown` package:

```bash
pip install markdown    # only dependency; Python stdlib otherwise
```

## The whole book in one breath

> Once a week, for ten minutes: move every file that earned a long-term place
> into one of three homes (**Reference / Projects / Archive**), rename the
> handful that matter, bulk-delete the obvious junk (installers have already
> done their job; duplicates are re-downloadable), and dump anything uncertain
> into one guilt-free `Inbox-unsorted` folder. When the mess reaches
> thousands, the rescue plan sorts by **category**, not file. Local AI can
> read piles and suggest names — it never gets delete permissions.

## Companion guides

- **local-file-organizer-cli** — a command-line tool that automates the triage
  rules from this handbook (draft rules in [docs/07](docs/07-local-ai-triage.md),
  then let a predictable script do the moving).
- **second-brain-basics-guide** — the bigger picture for your notes and
  documents, of which [Filing/](docs/index.md#the-three-homes-that-fix-it) is
  the file-layer component.

You don't need either one to use this handbook.

## Testing

```bash
python3 -m unittest discover -s tests -v
```

The suite rebuilds the site in a scratch directory and verifies: every page
renders, every internal link and anchor resolves, the six triage gates and
five destinations are actually present, the checklist still has its
checkboxes, the glossary still defines its terms, no stray non-Latin script
characters and no secrets snuck into any file, the build is deterministic,
and the LICENSE/README keep their required attribution and copyright lines.

## Project layout

```
├── README.md
├── LICENSE                     # MIT · Copyright (c) 2026 Asdale Dynamics, LLC
├── build.py                    # docs/*.md  →  site/*.html
├── Makefile
├── docs/                       # the handbook (markdown, source of truth)
│   ├── index.md
│   ├── 01-...–07-...md         # seven chapters
│   ├── checklist-reset-day.md
│   ├── decision-card.md
│   └── glossary.md
├── site/                       # generated static site (safe to delete)
├── tests/
│   └── test_build.py
└── STATUS.md                   # current state of the project
```

## Copyright

© 2026 Asdale Dynamics, LLC · MIT License ·
Part of Dylan Asdale's beginner-friendly AI and life-admin guide series at
[dylanasdale.github.io](https://dylanasdale.github.io).
