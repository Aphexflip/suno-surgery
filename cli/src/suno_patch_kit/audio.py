"""Optional local preview splice with ffmpeg.

Takes the original track and a replacement audio file for one bad
section and splices them together locally, so you can hear the join
*before* spending Suno credits on a Replace Section attempt.

ffmpeg is optional. If it is not installed, this module raises a clear
error and everything else in the kit still works.
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def ffmpeg_available() -> bool:
    return shutil.which("ffmpeg") is not None


def preview_splice(
    original: Path,
    replacement: Path,
    *,
    start_seconds: float,
    end_seconds: float,
    output: Path,
) -> Path:
    """Splice replacement audio into [start, end) of the original.

    Uses ffmpeg's concat demuxer with three segments:
    original[0:start] + replacement (trimmed to the section length)
    + original[end:]. Re-encodes to the output container's default
    codec; this is a *preview*, not a master.
    """
    if not ffmpeg_available():
        raise RuntimeError(
            "ffmpeg is not installed. Install it (e.g. `brew install ffmpeg` "
            "or `sudo apt install ffmpeg`) to use preview splices — "
            "everything else in Suno Patch Kit works without it."
        )
    if end_seconds <= start_seconds:
        raise ValueError("End time must be after start time")
    for path in (original, replacement):
        if not path.exists():
            raise FileNotFoundError(path)
    length = end_seconds - start_seconds
    output.parent.mkdir(parents=True, exist_ok=True)

    def run(*args: str) -> None:
        subprocess.run(
            ["ffmpeg", "-y", "-v", "error", *args],
            check=True,
        )

    tmp = output.parent
    before = tmp / "_spk_before.wav"
    after = tmp / "_spk_after.wav"
    repl = tmp / "_spk_replacement.wav"
    try:
        run("-i", str(original), "-t", str(start_seconds),
            "-c:a", "pcm_s16le", str(before))
        run("-i", str(original), "-ss", str(end_seconds),
            "-c:a", "pcm_s16le", str(after))
        run("-i", str(replacement), "-t", str(length),
            "-c:a", "pcm_s16le", str(repl))
        concat_list = tmp / "_spk_concat.txt"
        concat_list.write_text(
            "".join(f"file '{p}'\n" for p in (before, repl, after)),
            encoding="utf-8")
        run("-f", "concat", "-safe", "0", "-i", str(concat_list),
            "-c:a", "pcm_s16le", str(output))
    finally:
        for p in (before, after, repl, tmp / "_spk_concat.txt"):
            try:
                p.unlink()
            except FileNotFoundError:
                pass
    return output
