from __future__ import annotations

from yt_agent_editor.models import TranscriptBlock, TranscriptSegment


def merge_transcript_segments(
    segments: list[TranscriptSegment],
    *,
    max_gap_seconds: float = 1.5,
    max_chars: int = 700,
) -> list[TranscriptBlock]:
    if not segments:
        return []

    blocks: list[TranscriptBlock] = []
    current_start = segments[0].start_seconds
    current_end = segments[0].end_seconds
    current_text = segments[0].text
    current_indexes = [segments[0].index]

    for segment in segments[1:]:
        gap = segment.start_seconds - current_end
        candidate_text = f"{current_text} {segment.text}".strip()
        should_merge = gap <= max_gap_seconds and len(candidate_text) <= max_chars

        if should_merge:
            current_end = segment.end_seconds
            current_text = candidate_text
            current_indexes.append(segment.index)
            continue

        blocks.append(
            TranscriptBlock(
                start_seconds=current_start,
                end_seconds=current_end,
                text=current_text,
                source_indexes=current_indexes,
            )
        )
        current_start = segment.start_seconds
        current_end = segment.end_seconds
        current_text = segment.text
        current_indexes = [segment.index]

    blocks.append(
        TranscriptBlock(
            start_seconds=current_start,
            end_seconds=current_end,
            text=current_text,
            source_indexes=current_indexes,
        )
    )
    return blocks
