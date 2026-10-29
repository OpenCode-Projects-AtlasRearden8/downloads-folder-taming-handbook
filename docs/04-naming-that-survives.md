# Chapter 4: Names That Survive Years

A filename is a message from present-you to future-you. Most filenames fail as
messages: `scan0073.pdf`, `final_v3(2)_REAL.docx`, `IMG_4821.jpg`. The failure
mode is painful and easy to demo: try finding "that insurance letter" in a
folder of 40 scans named `scan0032.pdf`. The information was always inside the
file — but *unreadable until opened*, which for an ADHD brain means effectively
gone.

Good naming is a tiny time investment that makes every future Search and every
future triage faster. This chapter's rules are deliberately boring and
deliberately few.

## The pattern

```
neighbor - what it is - distinguishing detail
```

Three parts, hyphen-separated, lowercase. For anything with a date that
matters, prepend the date:

```
2026-10-14 home insurance renewal letter.pdf
2026-10 bluetooth speaker manual.pdf
passport - renewal receipt - application PA-3391.pdf
```

## The six rules

1. **Dates first, `YYYY-MM-DD`, only when the date matters.** ISO dates sort
   chronologically in every OS and read unambiguously at a glance. Don't date
   files where the date is trivia — every rule you don't apply is OK.
2. **Name by search intent, not by content.** When you think "I'll need that
   later," ask: *what will I type in the Search box?* Name it with those exact
   words. `insurance` beats `policy-doc-AETNA-2026-scan` if a searching-you
   will type "insurance."
3. **Be specific in the one place it matters.** `manual.pdf` is useless;
   `manual - rowing machine.pdf` is forever useful. One good distinguishing
   detail beats five vague ones.
4. **No forbidden characters.** `/ \ : * ? " < > |` break on Windows (and `/`
   on Mac). Hyphens and spaces are safe everywhere. Question marks in
   filenames ("invoice?") are a classic Windows heartbreak.
5. **Kill the noise words.** No `final`, `new`, `latest`, `v2-really-FINAL`.
   These describe your *stress*, not the file. If versions matter,
   `2026-10-14` versions beat `FINAL-v3`.
6. **One name decided once.** Renaming is a *reset-day* job (step 4 of the
   checklist), not a mid-download activity. Mid-download, just drop the file;
   trust the ritual.

## Batch renaming without pain

You never rename 100 files — you rename 100 files *once, with a tool*:

- **Simple version-killers:** search/sort files starting with the same stem,
  select all, and use macOS "Rename → Add Text" / Windows "F2 pattern" /
  [PowerToys PowerRename](https://learn.microsoft.com/windows/powertoys/powerrename)
  to stamp them with one prefix like `boat trailer manual - `.
- **The date-stamp trick:** for photos/screenshots, "sort by date created" then
  batch-rename with the month (`2026-09`), and Search never fails you again.

## What this has to do with Downloads

Notice that Downloads sorts with **newest first** by default — which buries
your oldest true valuables under an avalanche of this week's junk. A file named
well can be *found* from the avalanche; a file named `IMG_4821.jpg` can't.
Naming is the difference between Archive and oblivion, which is why
"rename the handful that matter" is a permanent step of the weekly reset, not
an aspiration to one-day rename everything (you won't, and that's fine).
