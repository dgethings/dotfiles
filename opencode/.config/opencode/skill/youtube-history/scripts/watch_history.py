#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# ///
"""Parse a Google Takeout YouTube watch-history JSON file, filter to a single
date, and merge the videos into an Obsidian daily note under a `## Media`
section (deduplicating against what is already there).

Designed for the `youtube-history` opencode skill. Pure stdlib, no deps.

Usage:
    watch_history.py --takeout PATH [--note PATH] [--date YYYY-MM-DD]
                     [--timezone NAME] [--media-heading TEXT] [--dry-run] [--json]

If --note is omitted, no note is edited; the matched videos are printed as
markdown bullets (or JSON with --json) so the caller can inspect them.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Iterable
from zoneinfo import ZoneInfo

VIDEO_ID_RE = re.compile(r"(?:v=|youtu\.be/)([\w-]{11})")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*?)\s*$")
WATCHED_PREFIX_RE = re.compile(r"^Watched\s+", re.IGNORECASE)
RULE_RE = re.compile(r"^\s*-{3,}\s*$")  # horizontal rule


def local_tz(name: str | None) -> ZoneInfo:
    if name:
        return ZoneInfo(name)
    # Derive the system local timezone.
    return datetime.now().astimezone().tzinfo  # type: ignore[return-value]


def parse_time(raw: str) -> datetime | None:
    if not raw:
        return None
    raw = raw.strip()
    try:
        # Python <3.11 cannot parse a trailing "Z".
        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        return datetime.fromisoformat(raw)
    except ValueError:
        return None


def video_id_from_url(url: str) -> str | None:
    m = VIDEO_ID_RE.search(url or "")
    return m.group(1) if m else None


def clean_title(title: str | None) -> str:
    if not title:
        return "(untitled)"
    t = WATCHED_PREFIX_RE.sub("", title).strip()
    # Unescape HTML entities Takeout sometimes emits.
    t = (
        t.replace("&amp;", "&")
        .replace("&quot;", '"')
        .replace("&#39;", "'")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
    )
    return t or "(untitled)"


def iter_entries(path: Path) -> Iterable[dict]:
    with path.open("r", encoding="utf-8-sig") as fh:
        data = json.load(fh)
    if isinstance(data, dict):
        # Some exports wrap the list under a key.
        data = data.get("items") or data.get("entries") or []
    if not isinstance(data, list):
        raise SystemExit(f"Unexpected JSON structure in {path} (expected a list)")
    yield from data


def extract_video(entry: dict) -> dict | None:
    url = entry.get("titleUrl") or ""
    vid = video_id_from_url(url)
    if not vid:
        return None  # ads / deleted / private videos have no watch URL
    subs = entry.get("subtitles") or []
    channel = subs[0].get("name") if subs and isinstance(subs[0], dict) else None
    return {
        "id": vid,
        "title": clean_title(entry.get("title")),
        "url": f"https://www.youtube.com/watch?v={vid}",
        "channel": channel,
        "time": entry.get("time"),
    }


def videos_on_date(path: Path, target: date, tz) -> list[dict]:
    out: list[dict] = []
    seen: set[str] = set()
    for entry in iter_entries(path):
        vid = extract_video(entry)
        if not vid:
            continue
        dt = parse_time(vid["time"])
        if dt is None:
            continue
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        local_dt = dt.astimezone(tz)
        if local_dt.date() != target:
            continue
        if vid["id"] in seen:
            continue
        seen.add(vid["id"])
        out.append(vid)
    # Most-recently-watched first within the day.
    out.sort(key=lambda v: v["time"] or "", reverse=True)
    return out


def format_bullet(v: dict) -> str:
    line = f"- [{v['title']}]({v['url']})"
    if v.get("channel"):
        line += f" — {v['channel']}"
    return line


def existing_ids_in_section(section_lines: list[str]) -> set[str]:
    ids: set[str] = set()
    for line in section_lines:
        for m in VIDEO_ID_RE.finditer(line):
            ids.add(m.group(1))
    return ids


def build_media_section(videos: list[dict], heading: str, include_help: bool) -> str:
    lines = [f"## {heading}", ""]
    if videos:
        lines.append("### YouTube")
        lines.append("")
        lines.extend(format_bullet(v) for v in videos)
        lines.append("")
    if include_help:
        lines.append(REFRESH_CALLOUT)
        lines.append("")
    return "\n".join(lines)


REFRESH_CALLOUT = """> [!info]- How I update this list
> These links come from a **Google Takeout** export of your YouTube watch history (the YouTube Data API does not expose watch history).
> 1. Go to **takeout.google.com** and click *Deselect all*.
> 2. Select **YouTube and YouTube Music**, then *All YouTube data included* and keep only **history**.
> 3. Open *Multiple formats* and set the history export to **JSON**.
> 4. Create export, download, unzip.
> 5. Copy `Takeout/YouTube and YouTube Music/history/watch_history.json` to `Sources/YouTube History/watch_history.json` in this vault.
> 6. Re-run: *"add today's YouTube to my daily note"*."""


def find_section_bounds(lines: list[str], heading: str) -> tuple[int, int] | None:
    """Return (start_index, end_index_exclusive) for a `## heading` section.

    end_index is the index of the next same-or-higher level heading, a
    standalone horizontal rule, or len(lines).
    """
    target = heading.strip().lower()
    start = None
    level = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if not m:
            continue
        this_level = len(m.group(1))
        this_text = m.group(2).strip().lower()
        if start is None:
            if this_level == 2 and this_text == target:
                start = i
                level = this_level
            continue
        # Inside the section: stop at same/higher level heading or a rule.
        if this_level <= level:
            return start, i
    if start is not None:
        # Section runs to the first standalone rule after it, or end of file.
        for j in range(start + 1, len(lines)):
            if RULE_RE.match(lines[j]):
                return start, j
        return start, len(lines)
    return None


def insert_index_for_media(lines: list[str]) -> int:
    """Where to insert a new `## Media` section: just before `## Evening
    Review`, else before the first horizontal rule after `## Notes`, else
    before `## Evening Review`-style fallbacks, else at end."""
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(2).strip().lower() == "evening review":
            return i
    # Before the first rule that appears after the Notes heading.
    notes_idx = None
    for i, line in enumerate(lines):
        m = HEADING_RE.match(line)
        if m and m.group(2).strip().lower() == "notes":
            notes_idx = i
            break
    if notes_idx is not None:
        for j in range(notes_idx + 1, len(lines)):
            if RULE_RE.match(lines[j]):
                return j
    return len(lines)


def merge_into_note(note_text: str, videos: list[dict], heading: str) -> tuple[str, list[dict], list[dict]]:
    """Merge videos into note_text. Returns (new_text, added, skipped)."""
    # Preserve trailing newline state.
    had_trailing_nl = note_text.endswith("\n")
    lines = note_text.split("\n")

    bounds = find_section_bounds(lines, heading)
    added: list[dict] = []
    skipped: list[dict] = []

    if bounds is None:
        # Create the section fresh.
        new_section = build_media_section(videos, heading, include_help=True)
        idx = insert_index_for_media(lines)
        # Ensure blank-line separation.
        block = new_section.rstrip("\n").split("\n")
        if idx > 0 and lines[idx - 1].strip() != "":
            block.insert(0, "")
        # Ensure blank line after.
        if idx < len(lines) and lines[idx].strip() != "":
            block.append("")
        lines[idx:idx] = block
        added = list(videos)
    else:
        start, end = bounds
        section = lines[start:end]
        existing = existing_ids_in_section(section)
        fresh = [v for v in videos if v["id"] not in existing]
        skipped = [v for v in videos if v["id"] in existing]
        if fresh:
            # Rebuild the section, preserving any non-video prose lines (help
            # callout, headers) and appending fresh bullets under ### YouTube.
            new_bullets = [format_bullet(v) for v in fresh]
            rebuilt = rebuild_section_with_bullets(section, new_bullets)
            lines[start:end] = rebuilt
        added = fresh

    new_text = "\n".join(lines)
    if had_trailing_nl and not new_text.endswith("\n"):
        new_text += "\n"
    return new_text, added, skipped


def rebuild_section_with_bullets(section: list[str], new_bullets: list[str]) -> list[str]:
    """Insert new_bullets into an existing Media section.

    Strategy: if an `### YouTube` subsection exists, add bullets there (after
    existing bullets, before any callout). Otherwise create the subsection right
    after the `## Media` heading line.
    """
    out = list(section)

    # Locate `### YouTube` within the section.
    yt_idx = None
    for i, line in enumerate(out):
        m = HEADING_RE.match(line)
        if m and len(m.group(1)) == 3 and m.group(2).strip().lower() == "youtube":
            yt_idx = i
            break

    if yt_idx is None:
        # No subsection yet: insert one after the heading + blank line.
        head = out[:1]
        rest = out[1:]
        sub = ["### YouTube", ""]
        sub.extend(new_bullets)
        sub.append("")
        return head + sub + rest

    # Find the last existing bullet within the YouTube subsection.
    insert_at = yt_idx + 1
    last_bullet = None
    for i in range(yt_idx + 1, len(out)):
        line = out[i]
        if HEADING_RE.match(line):
            break  # next subsection
        if line.lstrip().startswith("- "):
            last_bullet = i
    if last_bullet is not None:
        insert_at = last_bullet + 1
    else:
        # Skip blank lines after the heading.
        while insert_at < len(out) and out[insert_at].strip() == "":
            insert_at += 1

    block = list(new_bullets)
    out[insert_at:insert_at] = block
    return out


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--takeout", required=True, type=Path, help="Path to watch_history.json from Google Takeout")
    p.add_argument("--note", type=Path, default=None, help="Daily note .md path to merge into (optional)")
    p.add_argument("--date", default=None, help="Target date YYYY-MM-DD (default: today or derived from --note filename)")
    p.add_argument("--timezone", default=None, help="Local timezone name, e.g. Europe/London (default: system local)")
    p.add_argument("--media-heading", default="Media", help="Heading text for the media section (default: Media)")
    p.add_argument("--dry-run", action="store_true", help="Do not write the note; print what would change")
    p.add_argument("--json", action="store_true", help="Print matched videos as JSON to stdout")
    return p.parse_args(argv)


def resolve_date(args: argparse.Namespace) -> date:
    if args.date:
        return date.fromisoformat(args.date)
    if args.note:
        m = re.search(r"(\d{4})-(\d{2})-(\d{2})", args.note.name)
        if m:
            return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    return date.today()


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.takeout.exists():
        print(f"ERROR: takeout file not found: {args.takeout}", file=sys.stderr)
        return 2

    tz = local_tz(args.timezone)
    target = resolve_date(args)

    videos = videos_on_date(args.takeout, target, tz)

    if args.json or args.note is None:
        if args.json:
            print(json.dumps({"date": target.isoformat(), "timezone": str(tz), "videos": videos}, indent=2))
        else:
            print(f"# YouTube watched on {target.isoformat()} ({tz})")
            print()
            if videos:
                for v in videos:
                    print(format_bullet(v))
            else:
                print("_(no videos found for this date)_")
        if args.note is None:
            return 0

    note_path = args.note
    if not note_path.exists():
        print(f"ERROR: daily note not found: {note_path}", file=sys.stderr)
        return 2

    note_text = note_path.read_text(encoding="utf-8")
    new_text, added, skipped = merge_into_note(note_text, videos, args.media_heading)

    if new_text == note_text:
        print(f"No changes. {len(videos)} video(s) matched {target.isoformat()}; all already present.")
        return 0

    if not args.dry_run:
        note_path.write_text(new_text, encoding="utf-8")

    action = "would add" if args.dry_run else "added"
    print(
        f"{action} {len(added)} video(s) to {args.media_heading} section"
        f" ({len(skipped)} already present, {len(videos)} total matched for {target.isoformat()})."
    )
    if args.dry_run:
        print("--- DRY RUN: note not written ---")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
