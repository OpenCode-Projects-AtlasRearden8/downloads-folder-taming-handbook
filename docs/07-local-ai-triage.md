# Chapter 7: Where Local AI Actually Helps

This handbook is deliberately AI-light: ten minutes a week and six yes/no
questions don't need a machine learning model. But since "could a local LLM
just... do my files?" is a fair question — and one we get constantly — here's
an honest map of where an AI sitting on your own laptop genuinely helps, where
it's neutral, and where it will actively make things worse.

The short version: **local AI is a good reading assistant and a dangerous
great clicker.** It shines at the tasks you avoid because they're *reading*,
and it should be kept away from the tasks where a mistake is expensive.

## What local models are good at here

### Reading piles, summarizing cheaply

Give it the fifteen mystery PDFs you can't place, and it will tell you —
locally, nothing uploaded — "these three are duplicates; this one is your
wife's visa paperwork; this one is a course syllabus from 2024." It reads fast
and untiringly. That's genuinely useful, because reading-is-the-bottleneck is
exactly the step that makes triage slots feel like meetings. The judgment
stays yours; the summarizing is outsourced.

### Suggesting names and homes (advice only)

Paste a list of filenames — just the names, no contents — into a local model
with the prompt: *"suggest tidy archive-folder names for these, grouped, flag
the ones that look like installers or duplicates."* You get a sorting plan in
seconds, which you can then execute yourself with the
[Decision Card](decision-card.md) in one hand. The model is a
second opinion, not a hand on your mouse.

### Drafting rules you'd never write

Small local models are decent at turning vague habits into concrete rules:
"every file that starts with `invoice` goes to `Filing/Reference/invoices/`,
every `.exe` older than 30 days is deleted first, everything else ask me."
Hand that rule-set to a *script* (not the model; see below) and it becomes your
machine-fast pre-triage.

## What it is neutral at

- **Mass rename.** Tools like PowerRename or a one-line `rename` script are
  faster, free, deterministic, and offline. Use the AI to *draft the pattern*
  if the names are gnarly, then apply it with the tool.
- **Finding duplicates by name/size/date.** `fdupes`-style tools and folder
  searches do this better, instantly, with zero hallucination.
- **Nothing about your Documents structure.** Moving 200 curated files is a
  job for Finder/Explorer and your own three homes.

## Where it will hurt you

The trap is **letting the model move or delete files by itself.** Even a
perfect local model occasionally misreads a PDF — and when your agent is
holding `Documents` in one hand and `rm` in the other, "occasionally" translates
to "someday, your only copy of your lease." Concretely:

- **Never run an auto-delete "suggestion" without a snapshot.** If you want to
  experiment, copy 50 files to a sandbox folder, let the AI triage the copies,
  and compare. (Same placebo-snapshot safety net as [Chapter 6](06-the-rescue-plan.md).)
- **Scripts over agents for bulk actions.** A shell script that moves `.exe`
  files is dumb but *predictably* dumb. An LLM given delete permissions is
  smart-but-unpredictable. For files, prefer predictability every time.
- **Don't send personal documents to cloud models.** The entire reason for
  *local* AI in this chapter is that insurance letters, IDs, and tax documents
  never need to leave the laptop.   If a cloud model is the only AI you have,
  triage by filename only — never contents.

## The honest summary

Local AI earns its space where **reading is the blocker**: summarizing mystery
documents, proposing names, drafting triage rules. It does not earn delete
permissions. Think of it as a very fast intern who reads everything and
recommends — never the one with hands on the filing cabinet. If you want a
tool that implements the safe end of this spectrum (rules you control, decisions
you confirm), that's exactly the design behind our companion project,
local-file-organizer-cli.
