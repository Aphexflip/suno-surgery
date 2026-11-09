"""Command-line interface for Suno Patch Kit.

Standard library only. Default library file is ``library.json`` in the
current directory; pass ``--library`` to use another file.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from . import __version__
from .audio import ffmpeg_available, preview_splice
from .library import (
    STATUSES,
    add_issue,
    add_song,
    add_version,
    find_song,
    load_library,
    log_attempt,
    save_library,
)
from .replace import build_replace_prompt
from .timeutils import format_time, parse_time, section_warning

DEFAULT_LIBRARY = "library.json"


def _library_path(args) -> Path:
    return Path(args.library or DEFAULT_LIBRARY)


def _load(args) -> dict:
    return load_library(_library_path(args))


def _save(args, data: dict) -> None:
    save_library(_library_path(args), data)


def cmd_init(args) -> int:
    path = _library_path(args)
    if path.exists():
        print(f"Library already exists: {path}")
        return 0
    save_library(path, {"schema_version": 1, "songs": []})
    print(f"Created empty library: {path}")
    return 0


def cmd_import(args) -> int:
    audio = Path(args.audio)
    if not audio.exists():
        print(f"error: audio file not found: {audio}", file=sys.stderr)
        return 2
    if audio.suffix.lower() not in (".wav", ".mp3", ".flac", ".ogg"):
        print(f"warning: unusual audio extension {audio.suffix!r} — continuing")
    lyrics = ""
    if args.lyrics_file:
        lyrics = Path(args.lyrics_file).read_text(encoding="utf-8")
    data = _load(args)
    song = add_song(
        data,
        title=args.title,
        audio_path=str(audio),
        genre=args.genre or "",
        mood=args.mood or "",
        status=args.status,
        lyrics=lyrics,
        style_prompt=args.prompt or "",
    )
    _save(args, data)
    print(f"Imported {song['id']}  {song['title']}  [{song['status']}]")
    print(f"  audio: {song['audio_path']}")
    return 0


def cmd_list(args) -> int:
    data = _load(args)
    if not data["songs"]:
        print("No songs yet. Run `suno-patch-kit import <audio> --title ...`")
        return 0
    for song in data["songs"]:
        open_issues = sum(1 for i in song["issues"] if i["status"] == "open")
        print(
            f"{song['id']}  {song['title']:<40} "
            f"[{song['status']}]  "
            f"{song.get('genre','')}/{song.get('mood','')}  "
            f"v{len(song['versions'])}  issues:{open_issues} open"
        )
    return 0


def cmd_show(args) -> int:
    data = _load(args)
    try:
        song = find_song(data, args.song)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    print(f"{song['title']}  ({song['id']})  [{song['status']}]")
    print(f"  audio:  {song['audio_path']}")
    print(f"  genre:  {song.get('genre') or '-'}   mood: {song.get('mood') or '-'}")
    if song.get("style_prompt"):
        print(f"  prompt: {song['style_prompt']}")
    print("  versions:")
    for v in song["versions"]:
        print(f"    v{v['version']}  {v['label']} — {v.get('note','')} ({v['audio_path']})")
    print("  issues:")
    if not song["issues"]:
        print("    none — nothing marked yet")
    for issue in song["issues"]:
        print(
            f"    {issue['id']}  {format_time(issue['start_seconds'])}–"
            f"{format_time(issue['end_seconds'])}  [{issue['status']}]  "
            f"{issue['note']}  ({len(issue['attempts'])} attempts)"
        )
    if song.get("lyrics"):
        print("  lyrics: (stored, first 200 chars)")
        print("   ", song["lyrics"][:200].replace("\n", " / "))
    return 0


def cmd_mark(args) -> int:
    try:
        start = parse_time(args.start)
        end = parse_time(args.end)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    warning = section_warning(start, end)
    if warning:
        print(f"note: {warning}")
    data = _load(args)
    try:
        song = find_song(data, args.song)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    issue = add_issue(
        song, start_seconds=start, end_seconds=end, note=args.note,
        replacement_lyrics=args.lyrics or "",
    )
    _save(args, data)
    print(
        f"Marked issue {issue['id']} on {song['title']}: "
        f"{format_time(start)}–{format_time(end)} — {args.note}"
    )
    print("Next: `suno-patch-kit replace-prompt "
          f"{song['id']} --issue {issue['id']}`")
    return 0


def cmd_replace_prompt(args) -> int:
    data = _load(args)
    try:
        song = find_song(data, args.song)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    issue = next((i for i in song["issues"] if i["id"] == args.issue), None)
    if issue is None:
        print(f"error: no issue {args.issue!r} on this song", file=sys.stderr)
        return 2
    print(build_replace_prompt(song, issue))
    return 0


def cmd_version(args) -> int:
    data = _load(args)
    try:
        song = find_song(data, args.song)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    version = add_version(
        song, label=args.label, audio_path=args.audio, note=args.note or "")
    if args.mark_keeper:
        song["status"] = "keeper"
        for issue in song["issues"]:
            if issue["status"] == "open":
                issue["status"] = "fixed"
                log_attempt(song, issue, label=args.label,
                            result="committed as keeper")
    _save(args, data)
    print(f"Added v{version['version']} ({version['label']}) to {song['title']}")
    return 0


def cmd_preview(args) -> int:
    data = _load(args)
    try:
        song = find_song(data, args.song)
    except KeyError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    issue = next((i for i in song["issues"] if i["id"] == args.issue), None)
    if issue is None:
        print(f"error: no issue {args.issue!r} on this song", file=sys.stderr)
        return 2
    if not ffmpeg_available():
        print("error: ffmpeg is not installed — preview splice needs it.",
              file=sys.stderr)
        print("Install ffmpeg, or use Suno's Replace Section directly.",
              file=sys.stderr)
        return 2
    output = Path(args.out or f"preview-{song['id']}-{issue['id']}.wav")
    try:
        preview_splice(
            Path(song["audio_path"]), Path(args.replacement),
            start_seconds=issue["start_seconds"],
            end_seconds=issue["end_seconds"], output=output,
            replacement_offset_seconds=parse_time(args.replacement_offset))
    except (FileNotFoundError, RuntimeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # ffmpeg failure
        print(f"error: ffmpeg failed: {exc}", file=sys.stderr)
        return 2
    log_attempt(song, issue, label=f"local preview {output.name}",
                result="preview splice created")
    _save(args, data)
    print(f"Preview splice written: {output}")
    print("Listen to the joins at both ends before spending Suno credits.")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="suno-patch-kit",
        description="Local-first organizer for Suno songs. No Suno API, no login.",
    )
    parser.add_argument("--version", action="version",
                        version=f"suno-patch-kit {__version__}")
    parser.add_argument("--library", default=None,
                        help="library file (default: library.json)")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("init", help="create an empty library.json")
    p.set_defaults(func=cmd_init)

    p = sub.add_parser("import", help="import a downloaded Suno WAV/MP3")
    p.add_argument("audio")
    p.add_argument("--title", required=True)
    p.add_argument("--genre", default="")
    p.add_argument("--mood", default="")
    p.add_argument("--status", default="draft", choices=STATUSES)
    p.add_argument("--prompt", default="", help="style prompt used in Suno")
    p.add_argument("--lyrics-file", default=None)
    p.set_defaults(func=cmd_import)

    p = sub.add_parser("list", help="list songs in the library")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="show one song, versions and issues")
    p.add_argument("song")
    p.set_defaults(func=cmd_show)

    p = sub.add_parser("mark", help="mark a bad time range on a song")
    p.add_argument("song")
    p.add_argument("--start", required=True, help="e.g. 0:42 or 42")
    p.add_argument("--end", required=True, help="e.g. 0:58 or 58")
    p.add_argument("--note", required=True, help="what is wrong here")
    p.add_argument("--lyrics", default="", help="replacement lyrics for this range")
    p.set_defaults(func=cmd_mark)

    p = sub.add_parser("replace-prompt",
                       help="print the Replace Section brief to paste into Suno")
    p.add_argument("song")
    p.add_argument("--issue", required=True)
    p.set_defaults(func=cmd_replace_prompt)

    p = sub.add_parser("version", help="record a new version of a song")
    p.add_argument("song")
    p.add_argument("--label", required=True, help="e.g. 'v2 chorus fix'")
    p.add_argument("--audio", required=True)
    p.add_argument("--note", default="")
    p.add_argument("--mark-keeper", action="store_true",
                   help="mark song keeper and close its open issues")
    p.set_defaults(func=cmd_version)

    p = sub.add_parser("preview",
                       help="local ffmpeg splice preview (needs ffmpeg)")
    p.add_argument("song")
    p.add_argument("--issue", required=True)
    p.add_argument("--replacement", required=True,
                   help="audio file for the replacement section")
    p.add_argument("--out", default=None)
    p.add_argument("--replacement-offset", default="0",
                   help="source start in replacement file, e.g. 0 for a clip or 0:42 for a full-song candidate")
    p.set_defaults(func=cmd_preview)

    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
