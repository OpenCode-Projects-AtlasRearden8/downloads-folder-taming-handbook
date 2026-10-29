# Chapter 5: Safe Delete vs. Archive

Deleting is where tidy people get anxious and everyone else gets buried in
registries — receipts, licenses, tax documents — that can't be re-downloaded.
This chapter gives you a simple rule for choosing between *delete* and
*archive*, and settles the two questions that cause the most clutter in a
Downloads folder: installers and duplicate copies.

## The fundamental rule

> **"Can I get this back if I need it?"**
> — If yes, delete it.
> — If it's irreplaceable *and* must be kept, archive it.

That's the whole decision. Everything below is just training your instinct to
answer it honestly in one second.

## The three baskets

| Basket | Rule of thumb | Examples |
| --- | --- | --- |
| **Replaceable** | Re-downloadable in under a minute, and you'd know where | installers (already run), software you own, browser-saved tickets |
| **Regeneratable** | Annoying to recreate, but possible | blank forms, templates you made, work email attachments whose source still exists |
| **Irreplaceable** | Could not get this back | insurance PDFs, scanned IDs, contracts, tax records, photos you'd be sad about especially if they're the *only* copy |

Delete basket 1 with no guilt. Basket 2 stays in Downloads only if Downloads
still feels navigable — otherwise move it to `Filing/Reference`. Basket 3 has
one destination, and it isn't a folder you visit every day:

- **Put irreplaceable files in an archive folder** (e.g. `Filing/Archive`),
  never in Downloads, never on Desktop.
- **Make one backup of the archive** on a cloud drive or external USB drive
  twice a year. (Cloud-only copies die with your account; local-only copies
  die with the laptop — one of each is the sweet spot. If the local one lives
  on a drive that's usually unplugged, it also shrugs off ransomware.)
  Two copies is enough: update them if you remember; a partial backup still
  rescues most of history.

## Installers: safe to delete, always

The single biggest source of Downloads folder bulk is installers — `.exe`,
`.msi`, `.dmg`, `.pkg`, and `.zip`/`.7z` files that contain programs. The
confusion is understandable, because for one specific class of installer, there
IS a reason to keep it around. So here's the breakdown:

### Delete without hesitation

Apps you downloaded once and installed:
Chrome, Steam, the new PDF reader, the game client installer **after** it
finished installing. Uninstalling the app later does not require the original
installer — modern operating systems remove installed programs using their own
uninstallers, and re-installing "later" is one browser trip.

Also delete: the *new* `.zip` versions of installer packages you've decided not
to install, and every "Setup-thing-FINAL(2).exe" copy.

### The one category worth a second look

Old, *versioned* installers for software you can no longer download — an
installer for a niche tool whose developer vanished, or a hardware driver a
printer manufacturer stopped hosting. Before deleting, ask once: "would I still
want this if the vendor's download page disappears?" If yes → archive it (with
a good filename per [Chapter 4](04-naming-that-survives.md)). If it's an
artifact you can't even recall by name, it's trash.

### The one thing that's genuinely careful

System-level "rescue" media — Windows recovery ISOs, macOS full installers
(those `.app` files in Applications you might move elsewhere once), and
BIOS-update packages for hardware you still own. These are cheap to re-download
in theory. **But if your theory is "the internet will always be there when I
need it," remember the exact scenarios where you can't use the internet.**
Keep the recovery media, delete everything else.

## Duplicates: delete the *copies*, keep the *history*

Duplicate images and duplicate documents are the second-biggest Downloads
clutter source. Process them this way, strictly:

1. **Sort by name, look for self-confessed clones.** Files named
   `invoice(1).pdf`, `photo copy.jpg`, `report - Copy(2).docx` are almost
   always your doing — browser re-downloads or Ctrl-V slips. Delete all but
   the newest, opening at most one comparison.
2. For images, sort by **date created** and keep the earliest (often the
   original) unless the *later* one is visibly larger or a real crop.
3. For folders that fan out (`Backup old laptop/` inside
   `Backup of backup/`), **compare file counts and total size first**, then
   keep the nest and delete the copy of the nest.
4. When in doubt: move the whole family to `Inbox-unsorted`, dated. It gets
   re-triaged next week and takes 30 seconds of zero pressure.

And one hard rule for safety: **never delete duplicates from an archive folder
based on filename alone** — Archives are where "accidentally deleted the only
copy" incidents live. Open them or compare checksums, or just leave them; dead
weight in Archive does no harm to anyone's desktop peace.
