from __future__ import annotations

import re

from yt_agent_editor.analysis.llm_client import LLMClient, NotConfiguredLLMClient
from yt_agent_editor.analysis.prompts import load_prompt
from yt_agent_editor.analysis.schema_validation import require_keys
from yt_agent_editor.models import Chapter, HookCandidate, SegmentCandidate, TranscriptBlock
from yt_agent_editor.utils.timecode import format_youtube_timecode


def generate_chapters(
    blocks: list[TranscriptBlock],
    *,
    mode: str = "mock",
    llm_client: LLMClient | None = None,
) -> list[Chapter]:
    if mode == "real":
        client = llm_client or NotConfiguredLLMClient()
        data = client.complete_json(
            prompt=_analysis_prompt("chapter_generator", blocks),
            schema_name="chapters.schema.json",
        )
        require_keys(data, {"chapters"}, schema_name="chapters.schema.json")
        return [
            Chapter(start_seconds=float(item["start_seconds"]), title=str(item["title"]))
            for item in data["chapters"]  # type: ignore[index]
        ]

    if not blocks:
        return [Chapter(start_seconds=0, title="Intro")]

    chapters: list[Chapter] = []
    last_chapter_start = -9999.0
    for block in blocks:
        if not chapters:
            chapters.append(Chapter(start_seconds=0, title=_title_from_text(block.text, "Intro")))
            last_chapter_start = block.start_seconds
            continue
        if block.start_seconds - last_chapter_start >= 120:
            chapters.append(
                Chapter(
                    start_seconds=block.start_seconds,
                    title=_title_from_text(block.text, "Next section"),
                )
            )
            last_chapter_start = block.start_seconds

    return chapters[:12]


def detect_hooks(
    blocks: list[TranscriptBlock],
    *,
    mode: str = "mock",
    llm_client: LLMClient | None = None,
    limit: int = 5,
) -> list[HookCandidate]:
    if mode == "real":
        client = llm_client or NotConfiguredLLMClient()
        data = client.complete_json(
            prompt=_analysis_prompt("hook_detector", blocks),
            schema_name="hook_segments.schema.json",
        )
        require_keys(data, {"hooks"}, schema_name="hook_segments.schema.json")
        return [
            HookCandidate(
                id=str(item["id"]),
                start_seconds=float(item["start_seconds"]),
                end_seconds=float(item["end_seconds"]),
                score=float(item["score"]),
                reason=str(item["reason"]),
                transcript=str(item["transcript"]),
            )
            for item in data["hooks"]  # type: ignore[index]
        ]

    scored = sorted((_score_hook_block(block), block) for block in blocks)
    scored.reverse()
    hooks: list[HookCandidate] = []
    for rank, (score, block) in enumerate(scored[:limit], start=1):
        hooks.append(
            HookCandidate(
                id=f"hook-{rank:02}",
                start_seconds=block.start_seconds,
                end_seconds=block.end_seconds,
                score=round(score, 2),
                reason=_hook_reason(block.text),
                transcript=block.text,
            )
        )
    return hooks


def detect_broll(
    blocks: list[TranscriptBlock],
    *,
    mode: str = "mock",
    llm_client: LLMClient | None = None,
    limit: int = 5,
) -> list[SegmentCandidate]:
    if mode == "real":
        client = llm_client or NotConfiguredLLMClient()
        data = client.complete_json(
            prompt=_analysis_prompt("broll_detector", blocks),
            schema_name="broll_segments.schema.json",
        )
        require_keys(data, {"segments"}, schema_name="broll_segments.schema.json")
        return [_segment_from_mapping(item, f"broll-{index:02}") for index, item in enumerate(data["segments"], start=1)]  # type: ignore[arg-type,index]

    return [
        SegmentCandidate(
            id=f"broll-{index:02}",
            start_seconds=block.start_seconds,
            end_seconds=block.end_seconds,
            score=0.5,
            reason="Mock B-roll candidate from transcript block.",
            transcript=block.text,
        )
        for index, block in enumerate(blocks[:limit], start=1)
    ]


def detect_shorts(
    blocks: list[TranscriptBlock],
    *,
    mode: str = "mock",
    llm_client: LLMClient | None = None,
    limit: int = 5,
) -> list[SegmentCandidate]:
    if mode == "real":
        client = llm_client or NotConfiguredLLMClient()
        data = client.complete_json(
            prompt=_analysis_prompt("shorts_detector", blocks),
            schema_name="full_analysis.schema.json",
        )
        require_keys(data, {"shorts"}, schema_name="full_analysis.schema.json")
        return [_segment_from_mapping(item, f"short-{index:02}") for index, item in enumerate(data["shorts"], start=1)]  # type: ignore[arg-type,index]

    candidates = [block for block in blocks if 10 <= block.duration_seconds <= 60] or blocks
    return [
        SegmentCandidate(
            id=f"short-{index:02}",
            start_seconds=block.start_seconds,
            end_seconds=block.end_seconds,
            score=0.5,
            reason="Mock Shorts candidate from a concise transcript block.",
            transcript=block.text,
        )
        for index, block in enumerate(candidates[:limit], start=1)
    ]


def generate_youtube_description(
    blocks: list[TranscriptBlock],
    chapters: list[Chapter],
    *,
    mode: str = "mock",
    llm_client: LLMClient | None = None,
) -> str:
    if mode == "real":
        client = llm_client or NotConfiguredLLMClient()
        data = client.complete_json(
            prompt=_analysis_prompt("youtube_description", blocks),
            schema_name="youtube_metadata.schema.json",
        )
        require_keys(data, {"description"}, schema_name="youtube_metadata.schema.json")
        return str(data["description"])

    summary = _title_from_text(" ".join(block.text for block in blocks[:2]), "Video overview")
    chapter_lines = "\n".join(
        f"{format_youtube_timecode(chapter.start_seconds)} {chapter.title}" for chapter in chapters
    )
    return f"{summary}\n\nChapters:\n{chapter_lines}\n\nGenerated in mock mode."


def _analysis_prompt(name: str, blocks: list[TranscriptBlock]) -> str:
    prompt = load_prompt(name)
    transcript = "\n".join(
        f"[{format_youtube_timecode(block.start_seconds)}] {block.text}" for block in blocks
    )
    return f"{prompt}\n\nTranscript:\n{transcript}"


def _title_from_text(text: str, fallback: str) -> str:
    words = re.findall(r"[A-Za-z0-9']+", text)
    if not words:
        return fallback
    title = " ".join(words[:8])
    return title[:1].upper() + title[1:]


def _score_hook_block(block: TranscriptBlock) -> float:
    text = block.text.lower()
    score = 0.2
    if "?" in block.text:
        score += 0.25
    if "!" in block.text:
        score += 0.15
    if any(word in text for word in ["secret", "mistake", "avoid", "best", "worst", "why"]):
        score += 0.25
    if 8 <= block.duration_seconds <= 45:
        score += 0.2
    return min(score, 1.0)


def _hook_reason(text: str) -> str:
    if "?" in text:
        return "Question-style moment that can open a curiosity loop."
    if "!" in text:
        return "High-emphasis moment suitable for an intro hook."
    return "Concise transcript block selected by mock scoring."


def _segment_from_mapping(item: object, fallback_id: str) -> SegmentCandidate:
    if not isinstance(item, dict):
        raise ValueError("Expected segment item to be an object")
    return SegmentCandidate(
        id=str(item.get("id", fallback_id)),
        start_seconds=float(item["start_seconds"]),
        end_seconds=float(item["end_seconds"]),
        score=float(item.get("score", 0.5)),
        reason=str(item.get("reason", "")),
        transcript=str(item.get("transcript", "")),
    )
