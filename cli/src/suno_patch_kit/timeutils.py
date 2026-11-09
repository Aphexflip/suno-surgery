"""Time parsing/formatting for song positions.

Accepts seconds (``42``, ``42.5``) or ``M:SS`` / ``MM:SS`` (``0:42``).
"""

from __future__ import annotations


def parse_time(value: str | float | int) -> float:
    """Parse a time value to seconds. Raises ValueError on bad input."""
    if isinstance(value, (int, float)):
        seconds = float(value)
    else:
        text = str(value).strip()
        if ":" in text:
            parts = text.split(":")
            if len(parts) != 2:
                raise ValueError(f"Bad time {value!r}: use seconds or M:SS")
            minutes, secs = parts
            seconds = int(minutes) * 60 + float(secs)
        else:
            seconds = float(text)
    if seconds < 0:
        raise ValueError("Time cannot be negative")
    return seconds


def format_time(seconds: float) -> str:
    """Format seconds as ``M:SS`` (e.g. 42.0 -> ``0:42``)."""
    total = int(round(float(seconds)))
    return f"{total // 60}:{total % 60:02d}"


def section_warning(start: float, end: float) -> str | None:
    """Return a Replace Section sweet-spot warning, or None.

    Suno community consensus (and Suno's own editor guidance): 15-20s
    is the sweet spot. Under 5s the joins sound stitched; over 30s the
    model loses the melodic thread.
    """
    length = end - start
    if length < 5:
        return (
            f"Section is only {length:.1f}s — under 5s often produces "
            "audible seams. Widen it to a bar/line boundary if you can."
        )
    if length > 30:
        return (
            f"Section is {length:.1f}s — over 30s the model can lose the "
            "melodic thread. Split it into smaller sections if you can."
        )
    if not 15 <= length <= 20:
        return (
            f"Section is {length:.1f}s. The 15-20s sweet spot usually "
            "gives the cleanest joins."
        )
    return None
