from __future__ import annotations

import re
from pathlib import Path

from yt_agent_editor.models import TranscriptSegment
from yt_agent_editor.utils.timecode import parse_timecode

TIMECODE_LINE_RE = re.compile(r"(?P<start>[^ ]+)\s+-->\s+(?P<end>[^ ]+)")


def parse_srt(content: str) -> list[TranscriptSegment]:
    blocks = re.split(r"\n\s*\n", content.strip())
    segments: list[TranscriptSegment] = []

    for fallback_index, block in enumerate(blocks, start=1):
        lines = [line.strip() for line in block.splitlines() if line.strip()]
        if not lines:
            continue

        index = fallback_index
        if lines[0].isdigit():
            index = int(lines[0])
            lines = lines[1:]

        if not lines:
            continue

        time_match = TIMECODE_LINE_RE.search(lines[0])
        if not time_match:
            continue

        text_lines = lines[1:]
        text = normalize_transcript_text(" ".join(text_lines))
        segments.append(
            TranscriptSegment(
                index=index,
                start_seconds=parse_timecode(time_match.group("start")),
                end_seconds=parse_timecode(time_match.group("end")),
                text=text,
            )
        )

    return segments


def parse_srt_file(path: Path) -> list[TranscriptSegment]:
    return parse_srt(path.read_text(encoding="utf-8-sig"))


def normalize_transcript_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()
