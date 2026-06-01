from __future__ import annotations

import json
import subprocess
from pathlib import Path

from yt_agent_editor.models import HookCandidate
from yt_agent_editor.utils.timecode import format_seconds_for_ffmpeg


def build_extract_clip_command(
    *,
    video_path: Path,
    start_seconds: float,
    end_seconds: float,
    output_path: Path,
    ffmpeg_bin: str = "ffmpeg",
) -> list[str]:
    duration = max(0.1, end_seconds - start_seconds)
    return [
        ffmpeg_bin,
        "-hide_banner",
        "-n",
        "-ss",
        format_seconds_for_ffmpeg(start_seconds),
        "-i",
        str(video_path),
        "-t",
        format_seconds_for_ffmpeg(duration),
        "-c",
        "copy",
        str(output_path),
    ]


def load_hooks(path: Path) -> list[HookCandidate]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    return [
        HookCandidate(
            id=str(item["id"]),
            start_seconds=float(item["start_seconds"]),
            end_seconds=float(item["end_seconds"]),
            score=float(item["score"]),
            reason=str(item["reason"]),
            transcript=str(item["transcript"]),
        )
        for item in payload.get("hooks", [])
    ]


def extract_hook_clips(
    *,
    video_path: Path,
    hooks: list[HookCandidate],
    output_dir: Path = Path("outputs/clips"),
    dry_run: bool = False,
    ffmpeg_bin: str = "ffmpeg",
) -> list[list[str]]:
    output_dir.mkdir(parents=True, exist_ok=True)
    commands: list[list[str]] = []
    for hook in hooks:
        output_path = output_dir / f"{hook.id}.mp4"
        command = build_extract_clip_command(
            video_path=video_path,
            start_seconds=hook.start_seconds,
            end_seconds=hook.end_seconds,
            output_path=output_path,
            ffmpeg_bin=ffmpeg_bin,
        )
        commands.append(command)
        if not dry_run:
            subprocess.run(command, check=True)
    return commands
