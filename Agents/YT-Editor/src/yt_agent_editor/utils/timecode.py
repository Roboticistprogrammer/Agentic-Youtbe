from __future__ import annotations

import re

SRT_TIMECODE_RE = re.compile(
    r"^(?P<hours>\d{1,2}):(?P<minutes>\d{2}):(?P<seconds>\d{2})(?P<millis>[,.]\d{1,3})?$"
)


def parse_timecode(value: str) -> float:
    """Parse SRT-style timecodes into seconds."""
    text = value.strip()
    match = SRT_TIMECODE_RE.match(text)
    if not match:
        raise ValueError(f"Invalid timecode: {value!r}")

    hours = int(match.group("hours"))
    minutes = int(match.group("minutes"))
    seconds = int(match.group("seconds"))
    millis_text = match.group("millis") or ",0"
    millis = int(millis_text[1:].ljust(3, "0")[:3])
    return hours * 3600 + minutes * 60 + seconds + millis / 1000


def format_srt_timecode(seconds: float) -> str:
    total_millis = max(0, int(round(seconds * 1000)))
    hours, remainder = divmod(total_millis, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    whole_seconds, millis = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{whole_seconds:02},{millis:03}"


def format_seconds_for_ffmpeg(seconds: float) -> str:
    total_millis = max(0, int(round(seconds * 1000)))
    whole_seconds, millis = divmod(total_millis, 1000)
    return f"{whole_seconds}.{millis:03}"


def format_ffmpeg_seconds(seconds: float) -> str:
    return format_seconds_for_ffmpeg(seconds)

def format_youtube_timecode(seconds: float) -> str:
    total_seconds = max(0, int(seconds))
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours:
        return f"{hours}:{minutes:02}:{secs:02}"
    return f"{minutes}:{secs:02}"
