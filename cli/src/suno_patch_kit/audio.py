"""Offline ffmpeg preview splice for a single repair region.

A replacement can be a short extracted clip (offset 0), or a complete
candidate song (offset equals the original start time). Source files are
read only. Previews are re-encoded to 44.1 kHz stereo PCM WAV.
"""
from __future__ import annotations

import math
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
    replacement_offset_seconds: float = 0.0,
) -> Path:
    """Preview original[0:start] + candidate[offset:offset+length] + original[end:].

    Use replacement_offset_seconds=0 for an isolated replacement clip, or
    start_seconds for a complete candidate song with matching timestamps.
    The output must be a different path from either input.
    """
    original, replacement, output = Path(original), Path(replacement), Path(output)
    values = (start_seconds, end_seconds, replacement_offset_seconds)
    if not all(math.isfinite(v) for v in values):
        raise ValueError("Time values must be finite")
    if start_seconds < 0 or end_seconds <= start_seconds:
        raise ValueError("End must be after a non-negative start")
    if replacement_offset_seconds < 0:
        raise ValueError("Replacement offset cannot be negative")
    if output.resolve() in (original.resolve(), replacement.resolve()):
        raise ValueError("Preview output must not overwrite either source file")
    for path in (original, replacement):
        if not path.is_file():
            raise FileNotFoundError(path)
    if not ffmpeg_available():
        raise RuntimeError(
            "ffmpeg is not installed. Install ffmpeg to preview a splice. "
            "The other commands still work without it."
        )
    if output.suffix.lower() != ".wav":
        raise ValueError("Preview output must have a .wav extension")
    output.parent.mkdir(parents=True, exist_ok=True)

    length = end_seconds - start_seconds
    # Use one filter graph rather than concat-demuxing unnormalized WAV files.
    # Normalize sample rate/channel layout so mixed Suno exports concatenate.
    norm = "aresample=44100,aformat=sample_fmts=s16:channel_layouts=stereo"
    flt = ";".join([
        f"[0:a]atrim=start=0:end={start_seconds},asetpts=PTS-STARTPTS,{norm}[before]",
        f"[1:a]atrim=start={replacement_offset_seconds}:duration={length},asetpts=PTS-STARTPTS,{norm}[patch]",
        f"[0:a]atrim=start={end_seconds},asetpts=PTS-STARTPTS,{norm}[after]",
        "[before][patch][after]concat=n=3:v=0:a=1[out]",
    ])
    subprocess.run([
        "ffmpeg", "-y", "-v", "error",
        "-i", str(original), "-i", str(replacement),
        "-filter_complex", flt, "-map", "[out]",
        "-c:a", "pcm_s16le", str(output),
    ], check=True)
    return output
