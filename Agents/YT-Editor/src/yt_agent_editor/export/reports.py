from __future__ import annotations

import json
from pathlib import Path

from yt_agent_editor.models import AnalysisResult, Chapter, HookCandidate
from yt_agent_editor.utils.timecode import format_youtube_timecode


def write_chapters(path: Path, chapters: list[Chapter]) -> None:
    lines = [f"{format_youtube_timecode(chapter.start_seconds)} {chapter.title}" for chapter in chapters]
    _write_text(path, "\n".join(lines) + "\n")


def write_youtube_description(path: Path, description: str) -> None:
    _write_text(path, description.strip() + "\n")


def write_hook_candidates(path: Path, hooks: list[HookCandidate]) -> None:
    payload = {"hooks": [hook.to_dict() for hook in hooks]}
    _write_text(path, json.dumps(payload, indent=2) + "\n")


def write_analysis_report(path: Path, result: AnalysisResult) -> None:
    lines = [
        "# Analysis Report",
        "",
        "## Chapters",
        "",
        *[
            f"- {format_youtube_timecode(chapter.start_seconds)} {chapter.title}"
            for chapter in result.chapters
        ],
        "",
        "## Hook Candidates",
        "",
        *[
            (
                f"- `{hook.id}` {format_youtube_timecode(hook.start_seconds)}-"
                f"{format_youtube_timecode(hook.end_seconds)} score={hook.score}: {hook.reason}"
            )
            for hook in result.hooks
        ],
        "",
        "## YouTube Description",
        "",
        result.youtube_description.strip(),
        "",
    ]
    _write_text(path, "\n".join(lines))


def _write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
