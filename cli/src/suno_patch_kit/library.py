"""Local JSON library: songs, versions, issues, history.

The library is a single plain ``library.json`` file next to the user's
audio. No network, no account, no credentials. Schema version 1.
"""

from __future__ import annotations

import json
import uuid
from datetime import datetime, timezone
from pathlib import Path

STATUSES = ("draft", "keeper", "fix-needed", "done")
ISSUE_STATUSES = ("open", "fixed", "wontfix")


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def new_library() -> dict:
    return {"schema_version": 1, "songs": []}


def load_library(path: Path) -> dict:
    if not path.exists():
        return new_library()
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or "songs" not in data:
        raise ValueError(f"{path} is not a Suno Patch Kit library")
    return data


def save_library(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                    encoding="utf-8")


def find_song(data: dict, song_id: str) -> dict:
    for song in data["songs"]:
        if song["id"] == song_id or song["id"].startswith(song_id):
            return song
    raise KeyError(f"No song with id {song_id!r}. Run `list` to see ids.")


def add_song(
    data: dict,
    *,
    title: str,
    audio_path: str,
    genre: str = "",
    mood: str = "",
    status: str = "draft",
    lyrics: str = "",
    style_prompt: str = "",
) -> dict:
    if status not in STATUSES:
        raise ValueError(f"status must be one of {STATUSES}, got {status!r}")
    song = {
        "id": uuid.uuid4().hex[:8],
        "title": title,
        "audio_path": audio_path,
        "genre": genre,
        "mood": mood,
        "status": status,
        "lyrics": lyrics,
        "style_prompt": style_prompt,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "versions": [
            {
                "version": 1,
                "label": "v1 original",
                "audio_path": audio_path,
                "note": "Original Suno download",
                "created_at": now_iso(),
            }
        ],
        "issues": [],
        "history": [
            {"at": now_iso(), "action": "import",
             "detail": f"Imported {audio_path}"}
        ],
    }
    data["songs"].append(song)
    return song


def add_issue(
    song: dict,
    *,
    start_seconds: float,
    end_seconds: float,
    note: str,
    replacement_lyrics: str = "",
) -> dict:
    if end_seconds <= start_seconds:
        raise ValueError("End time must be after start time")
    issue = {
        "id": uuid.uuid4().hex[:6],
        "start_seconds": start_seconds,
        "end_seconds": end_seconds,
        "note": note,
        "replacement_lyrics": replacement_lyrics,
        "status": "open",
        "attempts": [],
        "created_at": now_iso(),
    }
    song["issues"].append(issue)
    song["status"] = "fix-needed"
    song["updated_at"] = now_iso()
    song["history"].append({
        "at": now_iso(), "action": "mark-issue",
        "detail": f"Bad section {start_seconds:.1f}-{end_seconds:.1f}s: {note}",
    })
    return issue


def add_version(song: dict, *, label: str, audio_path: str, note: str = "") -> dict:
    version = {
        "version": len(song["versions"]) + 1,
        "label": label,
        "audio_path": audio_path,
        "note": note,
        "created_at": now_iso(),
    }
    song["versions"].append(version)
    song["updated_at"] = now_iso()
    song["history"].append({
        "at": now_iso(), "action": "add-version",
        "detail": f"{label}: {note or audio_path}",
    })
    return version


def log_attempt(song: dict, issue: dict, *, label: str, result: str = "") -> None:
    issue["attempts"].append(
        {"at": now_iso(), "label": label, "result": result})
    song["updated_at"] = now_iso()
