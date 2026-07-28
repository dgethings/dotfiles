---
name: youtube-history
description: Add links to YouTube videos watched today into the Obsidian daily note, using a Google Takeout watch-history JSON export. Use whenever the user asks to log today's YouTube videos, add watched videos to their daily note, record what they watched on YouTube today, or pull their YouTube watch history into the daily note. Also trigger for "what did I watch on YouTube today" when the intent is to record it. The data comes from a manual Takeout export, NOT the YouTube API (which cannot read watch history).
---

# YouTube History → Daily Note

Record the YouTube videos watched today as markdown links in the daily note, under a `## Media` section.

## Important: where the data comes from

**The YouTube Data API cannot read watch history** — Google returns a `403 watchHistoryNotAccessible` error. This skill therefore uses a **Google Takeout JSON export** of the user's watch history, which lives at a known path in the vault. The export must be refreshed manually before running (see the foldable block the skill writes into every daily note).

- **Expected file:** `Sources/YouTube History/watch_history.json` (vault-relative)
- **Inside a Takeout zip** the file is at `Takeout/YouTube and YouTube Music/history/watch-history.json`
- The JSON is an array of entries; each has `title` ("Watched <Title>"), `titleUrl` (the watch URL), `subtitles[].name` (channel), and `time` (ISO-8601 UTC timestamp of when it was watched).

All parsing, date filtering (timezone-aware), deduplication, and section placement are handled by the bundled script — do not do this by hand.

## When this skill triggers

Any request to record/log today's watched YouTube videos, e.g.:
- "Add today's YouTube to my daily note"
- "Log the YouTube videos I watched today"
- "What did I watch on YouTube today? Put it in the daily note"
- "Update my daily note with YouTube history"
- "Pull my YouTube watch history"

## Workflow

### 1. Locate the Takeout JSON

First try the canonical location, then fall back to a search:

```bash
ls "Sources/YouTube History/watch-history.json"
```

If missing, look for a recent export in the usual landing spots (the Downloads folder and the vault), which you can do with glob/grep for `**/watch_history.json` or `**/Takeout/**/watch_history.json`.

If no `watch_history.json` exists anywhere, **stop and tell the user** to export one (give them the steps from the `REFRESH_CALLOUT` below), copy it to `Sources/YouTube History/watch_history.json`, and re-run. Do not fabricate video links.

### 2. Resolve today's daily note path

```bash
obsidian daily:path
```

This prints the absolute path to today's note (e.g. `.../Daily/2026-07-09.md`).

- If today's note **does not exist yet**, create it from `Templates/Daily Note GTD.md` using the Write tool (read the template first), so the `## Notes` / `## Evening Review` structure the placement logic relies on is present.
- If it exists, the script will read and edit it in place.

### 3. Run the merge script

The script filters the Takeout JSON to the target date (derived from the note filename, or today), dedupes against links already in the note, and inserts/updates a `## Media` section positioned between `## Notes` and `## Evening Review`.

```bash
python3 ~/.config/opencode/skill/youtube-history/scripts/watch_history.py \
  --takeout "Sources/YouTube History/watch-history.json" \
  --note "<absolute path to Daily/YYYY-MM-DD.md>"
```

Notes on flags:
- `--date YYYY-MM-DD` — override the target date (defaults to the note's filename date, else today).
- `--timezone "Europe/London"` — override the timezone used when deciding what "today" means (defaults to the system local timezone).
- `--dry-run` — preview the change without writing. Useful if the user is unsure.
- `--json` — print the matched videos as JSON instead of editing the note.

Use absolute paths for `--note` (the vault lives under `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/Main/`). For `--takeout` you may pass a vault-relative path only if you run the command from the vault root; otherwise use an absolute path.

The script writes the note directly via file I/O (no shell escaping issues). It will create the `## Media` section with a `### YouTube` subsection of video bullets, and embed a collapsible `> [!info]-` callout explaining how to refresh the export — **only on first creation**, so re-runs don't litter the note with duplicate help blocks.

### 4. Reload Obsidian and verify

The file was written on disk; tell Obsidian to pick it up:

```bash
obsidian reload
```

Then read the note back to confirm the section landed correctly:

```bash
obsidian read path="Daily/YYYY-MM-DD.md"
```

### 5. Report and log

Tell the user how many videos were added vs. already present. If nothing matched for the date, say so plainly (and remind them to re-export the Takeout JSON, since today's views may not have landed in the export yet).

Append to the vault log per the vault's AGENTS.md conventions:

```bash
cat <<'__OBS__' | obsidian append path="log.md"
## [YYYY-MM-DD HH:MM] youtube-history | Updated daily note media
Added N YouTube videos to [[YYYY-MM-DD]].
__OBS__
```

## Output format

A new `## Media` section in the daily note, placed before `## Evening Review`:

```markdown
## Media

### YouTube

- [Video Title](https://www.youtube.com/watch?v=abc123) — Channel Name
- [Another Video](https://www.youtube.com/watch?v=def456) — Channel Name

> [!info]- How I update this list
> These links come from a **Google Takeout** export ...
```

Re-runs append new videos under `### YouTube` and skip any already linked (matched by video ID). The help callout is added once, when the section is first created.

## Common issues

- **"no videos found for this date"** — The Takeout export is stale. YouTube needs time to register views; ask the user to re-export (and note Takeout can take minutes to hours to generate).
- **Wrong timezone** — If the user watches videos late at night and they land on "tomorrow", pass `--timezone` with their local IANA zone.
- **Takeout HTML instead of JSON** — The script only parses JSON. Tell the user to switch the history export format to JSON in Takeout (*Multiple formats*).
- **Duplicate `## Media` sections** — Should not happen; if the note already has one, the script reuses it. If a stray duplicate appears, the user can delete the extra heading.
