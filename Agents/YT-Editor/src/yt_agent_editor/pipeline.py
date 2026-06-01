from __future__ import annotations

from pathlib import Path

from yt_agent_editor.analysis import (
    detect_broll,
    detect_hooks,
    detect_shorts,
    generate_chapters,
    generate_youtube_description,
)
from yt_agent_editor.export.reports import (
    write_analysis_report,
    write_chapters,
    write_hook_candidates,
    write_youtube_description,
)
from yt_agent_editor.models import AnalysisResult
from yt_agent_editor.transcript import merge_transcript_segments, parse_srt_file


def run_analysis(
    *,
    video_path: Path,
    srt_path: Path,
    output_dir: Path = Path("outputs/reports"),
    mode: str = "mock",
) -> AnalysisResult:
    # video_path is accepted now so CLI calls match the future full workflow.
    _ = video_path
    segments = parse_srt_file(srt_path)
    blocks = merge_transcript_segments(segments)
    chapters = generate_chapters(blocks, mode=mode)
    hooks = detect_hooks(blocks, mode=mode)
    broll = detect_broll(blocks, mode=mode)
    shorts = detect_shorts(blocks, mode=mode)
    description = generate_youtube_description(blocks, chapters, mode=mode)

    result = AnalysisResult(
        chapters=chapters,
        hooks=hooks,
        broll=broll,
        shorts=shorts,
        youtube_description=description,
        transcript_blocks=blocks,
    )

    output_dir.mkdir(parents=True, exist_ok=True)
    write_chapters(output_dir / "chapters.txt", chapters)
    write_hook_candidates(output_dir / "hook_candidates.json", hooks)
    write_youtube_description(output_dir / "youtube_description.txt", description)
    write_analysis_report(output_dir / "analysis_report.md", result)
    return result
