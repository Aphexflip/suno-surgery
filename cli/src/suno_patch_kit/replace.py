"""Generate the exact Replace Section prompt for Suno.

This does NOT call Suno. It writes the text you paste into Suno's own
editor: More Actions > Edit > Replace Section (Pro/Premier), highlight
the time range, paste the lyrics/prompt below, Recreate Section.

The point is discipline: one variable at a time (fix the lyric OR push
the style, not both), the same length, and the surrounding context
named so the new take joins cleanly.
"""

from __future__ import annotations

from .timeutils import format_time, section_warning


def build_replace_prompt(song: dict, issue: dict) -> str:
    """Return a ready-to-paste Replace Section brief for one issue."""
    start = format_time(issue["start_seconds"])
    end = format_time(issue["end_seconds"])
    length = issue["end_seconds"] - issue["start_seconds"]
    warning = section_warning(issue["start_seconds"], issue["end_seconds"])

    lines = [
        f"REPLACE SECTION — EDITING BRIEF (NOT LYRICS) — {song['title']}  ({start}–{end}, {length:.0f}s)",
        "",
        "Keep everything outside this range exactly as it is. "
        "Regenerate ONLY this section.",
        "",
        f"Problem: {issue['note']}",
    ]
    if song.get("style_prompt"):
        lines += ["", f"Style to keep: {song['style_prompt']}"]
    if song.get("genre") or song.get("mood"):
        style_bits = " / ".join(
            b for b in (song.get("genre"), song.get("mood")) if b)
        lines += [f"Genre/mood: {style_bits}"]
    if issue.get("replacement_lyrics"):
        lines += [
            "",
            "Replacement lyrics for this section only:",
            issue["replacement_lyrics"],
            "",
            "Keep the syllable count and line shape close to the original "
            "so the new audio fits the surrounding bars. Same length, "
            "same tempo, same key.",
        ]
    else:
        lines += [
            "",
            "No new lyrics supplied — keep the original lyrics for this "
            "section, fix only the performance / pronunciation / mix.",
        ]
    lines += [
        "",
        "In Suno: open the song > More Actions (…) > Edit > "
        "Replace Section > highlight "
        f"{start}–{end}. Put ONLY replacement lyrics in the lyrics field "
        "(if provided), not this editing brief. Use the brief as guidance "
        "or in a separate instruction field if available. Click Recreate Section "
        "and listen to both versions before committing.",
    ]
    if warning:
        lines += ["", f"Note: {warning}"]
    return "\n".join(lines)
