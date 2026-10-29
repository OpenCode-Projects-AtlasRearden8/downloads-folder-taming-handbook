#!/usr/bin/env python3
"""Test suite for the Downloads & Desktop Taming Handbook.

Run:  python3 -m unittest discover -s tests -v

The suite (re)builds the site into a scratch directory copy of the project so
it never leaves a half-written site/ behind, then checks structure, links,
content promises, hygiene, and determinism.
"""

import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Stray non-Latin scripts that must never appear in the handbook (they've bitten
# us before: CJK characters can sneak into prose). Emoji and typographic
# punctuation are fine.
STRAY_SCRIPT_RE = re.compile(
    "[\u4e00-\u9fff\u3040-\u30ff\uac00-\ud7af\u0600-\u06ff\u0590-\u05ff]"
)

SECRET_PATTERNS = [
    r"AKIA[0-9A-Z]{16}",
    r"gh[pousr]_[A-Za-z0-9]{20,}",
    r"sk-[A-Za-z0-9]{20,}",
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"api[_-]?key\s*[:=]\s*['\"][^'\"]{8,}",
    r"password\s*[:=]\s*['\"][^'\"]{8,}",
]

TEXT_SUFFIXES = {".md", ".py", ".css", ".html", ".txt", ".sh", ".cfg", ".ya?ml"}


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8")


def build_site(dest: Path) -> Path:
    """Copy the project into dest, run build.py there, return its site/ dir."""
    shutil.copytree(
        ROOT,
        dest,
        ignore=shutil.ignore_patterns(".git", "__pycache__", "site", "htmlcov"),
        dirs_exist_ok=True,
    )
    subprocess.run(
        [sys.executable, "build.py", "--clean"],
        cwd=dest,
        check=True,
        capture_output=True,
        text=True,
    )
    return dest / "site"


class BuildTestCase(unittest.TestCase):
    """Base: one built site on disk, shared by tests that inspect HTML."""

    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="handbook-test-"))
        cls.site = build_site(cls.tmp)

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.tmp, ignore_errors=True)


class TestBuildOutput(BuildTestCase):
    REQUIRED_PAGES = [
        "index.html",
        "01-why-it-piles-up.html",
        "02-ten-minute-weekly-reset.html",
        "03-one-decision-triage.html",
        "04-naming-that-survives.html",
        "05-safe-delete-vs-archive.html",
        "06-the-rescue-plan.html",
        "07-local-ai-triage.html",
        "checklist-reset-day.html",
        "decision-card.html",
        "glossary.html",
        "style.css",
    ]

    def test_all_required_pages_generated(self):
        for name in self.REQUIRED_PAGES:
            self.assertTrue(
                (self.site / name).is_file(), f"missing site/{name}"
            )

    def test_pages_contain_site_chrome(self):
        for name in self.REQUIRED_PAGES:
            if name.endswith(".css"):
                continue
            text = read(self.site / name)
            self.assertIn("<main", text, name)
            self.assertIn('link rel="stylesheet" href="style.css"', text, name)
            self.assertIn("<!DOCTYPE html>", text, name)
            self.assertIn("<title>", text, name)
            self.assertNotIn("{{", text, f"unrendered placeholder in {name}")

    def test_no_raw_md_links_in_html(self):
        for page in self.site.glob("*.html"):
            self.assertNotIn('.md"', read(page), page.name)

    def test_overview_links_every_chapter(self):
        body = read(self.site / "index.html")
        for slug in [
            "01-why-it-piles-up",
            "02-ten-minute-weekly-reset",
            "03-one-decision-triage",
            "04-naming-that-survives",
            "05-safe-delete-vs-archive",
            "06-the-rescue-plan",
            "07-local-ai-triage",
        ]:
            self.assertIn(f'href="{slug}.html"', body, f"index does not link {slug}")

    def test_build_is_deterministic(self):
        tmp2 = Path(tempfile.mkdtemp(prefix="handbook-test2-"))
        try:
            site2 = build_site(tmp2)
            for page in self.site.glob("*.html"):
                self.assertEqual(
                    read(page), read(site2 / page.name), page.name
                )
        finally:
            shutil.rmtree(tmp2, ignore_errors=True)


class TestLinksAndAnchors(BuildTestCase):
    def test_every_relative_href_resolves(self):
        for page in self.site.glob("*.html"):
            for href in re.findall(r'href="([^"]+)"', read(page)):
                if href.startswith(("http", "mailto:", "#")):
                    continue
                target = href.split("#")[0]
                self.assertTrue(
                    (self.site / target).is_file(),
                    f"{page.name} links to missing {href}",
                )

    def test_every_internal_anchor_exists_on_target(self):
        for page in self.site.glob("*.html"):
            text = read(page)
            for href in re.findall(r'href="([^"]+)"', text):
                if "#" not in href:
                    continue
                file_part, anchor = href.split("#", 1)
                target_page = self.site / (file_part or page.name)
                ids = set(re.findall(r'id="([^"]+)"', read(target_page)))
                self.assertIn(
                    anchor,
                    ids,
                    f"{page.name} anchor #{anchor} missing on {target_page.name}",
                )

    def test_nav_links_current_page(self):
        for page in self.site.glob("*.html"):
            self.assertIn('aria-current="page"', read(page), page.name)


class TestContentPromises(unittest.TestCase):
    """The handbook's core structure must actually be there, chapter by chapter."""

    def setUp(self):
        self.docs = ROOT / "docs"

    def chapter(self, slug: str) -> str:
        return read(self.docs / f"{slug}.md")

    def test_every_doc_has_exactly_one_h1(self):
        for doc in sorted(self.docs.glob("*.md")):
            h1s = re.findall(r"^# (.+)$", read(doc), flags=re.M)
            self.assertEqual(
                len(h1s), 1, f"{doc.name} should have exactly one H1, has {len(h1s)}"
            )

    def test_six_gates_present_in_triage_chapter(self):
        text = self.chapter("03-one-decision-triage")
        for marker in ("Gate 1", "Gate 2", "Gate 3", "Gate 4", "Gate 5", "Gate 6"):
            self.assertIn(marker, text, f"triage chapter lacks {marker}")

    def test_decision_card_has_six_gate_rows(self):
        text = self.chapter("decision-card")
        self.assertIn("The Six Gates", text)
        rows = re.findall(r"^\| \d \|", text, flags=re.M)
        self.assertEqual(len(rows), 6, "decision card should have 6 numbered gates")

    def test_decision_card_has_five_destinations(self):
        text = self.chapter("decision-card")
        for home in ("Reference", "Projects", "Archive", "Trash", "Inbox-unsorted"):
            self.assertIn(home, text)

    def test_checklist_is_ten_minute_and_tiered(self):
        text = self.chapter("checklist-reset-day")
        self.assertIn("10 minutes", text)
        for step in ("Step 1", "Step 2", "Step 3", "Step 4"):
            self.assertIn(step, text)
        # Resolution day is a checkbox ritual; count the boxes.
        boxes = re.findall(r"- \[ \]", text)
        self.assertGreaterEqual(len(boxes), 15, "checklist lost its checkboxes")

    def test_glossary_defines_core_terms(self):
        text = self.chapter("glossary").lower()
        for term in ("downloads", "desktop", "triage", "reset day", "archive",
                     "installers", "duplicate", "executive function", "local ai",
                     "catch-all", "one-decision", "rescue plan"):
            self.assertIn(f"**{term}", text, f"glossary lacks {term}")

    def test_each_cornerstone_chapter_exists_and_bites(self):
        promises = {
            "01-why-it-piles-up": ["conveyor belt", "three homes"],
            "02-ten-minute-weekly-reset": ["ten minutes", "timer", "Inbox-unsorted"],
            "03-one-decision-triage": ["one-decision", "Trash", "Reference"],
            "04-naming-that-survives": ["YYYY-MM-DD", "search", "FINAL"],
            "05-safe-delete-vs-archive": ["installer", "duplicate", "Archive"],
            "06-the-rescue-plan": ["4,000", "type", "installer"],
            "07-local-ai-triage": ["local", "delete", "snapshot"],
        }
        for slug, needles in promises.items():
            text = self.chapter(slug).lower()
            for needle in needles:
                self.assertIn(needle.lower(), text, f"{slug} lost '{needle}'")

    def test_index_front_loads_the_two_daily_tools(self):
        text = self.chapter("index")
        self.assertIn("checklist-reset-day.md", text)
        self.assertIn("decision-card.md", text)
        self.assertIn("glossary.md", text)

    def test_companion_projects_referenced(self):
        text = self.chapter("index")
        self.assertIn("local-file-organizer-cli", text)
        self.assertIn("second-brain-basics-guide", text)


class TestHygiene(unittest.TestCase):
    def test_no_cjk_or_stray_scripts_in_docs(self):
        for doc in sorted((ROOT / "docs").glob("*.md")):
            match = STRAY_SCRIPT_RE.search(read(doc))
            self.assertIsNone(match, f"stray script char in {doc.name}: {match!r}")

    def test_no_cjk_or_stray_scripts_in_generated_site(self):
        for page in (ROOT / "site").glob("*.html"):
            match = STRAY_SCRIPT_RE.search(read(page))
            self.assertIsNone(match, f"stray script char in {page.name}: {match!r}")

    def test_no_secrets_in_text_files(self):
        for p in ROOT.rglob("*"):
            if not p.is_file() or p.suffix not in TEXT_SUFFIXES:
                continue
            if ".git" in p.parts or p.name == "STATUS.md":
                continue
            text = read(p)
            for pattern in SECRET_PATTERNS:
                self.assertIsNone(
                    re.search(pattern, text),
                    f"possible secret matching {pattern} in {p.relative_to(ROOT)}",
                )


class TestPackaging(unittest.TestCase):
    def test_license_line_exact(self):
        lic = read(ROOT / "LICENSE")
        self.assertIn("Copyright (c) 2026 Asdale Dynamics, LLC", lic)
        self.assertIn("MIT License", lic)

    def test_readme_credits_llc_and_states_purpose(self):
        readme = read(ROOT / "README.md")
        self.assertIn("Asdale Dynamics, LLC", readme)
        self.assertIn("Downloads", readme)
        self.assertIn("Desktop", readme)
        self.assertIn("python3 build.py", readme)

    def test_docs_build_docstring_accurate(self):
        code = read(ROOT / "build.py")
        self.assertIn("PAGES", code)
        self.assertIn("def build(", code)


if __name__ == "__main__":
    unittest.main(verbosity=2)
