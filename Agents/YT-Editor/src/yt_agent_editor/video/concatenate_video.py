from __future__ import annotations

import subprocess
from pathlib import Path

from yt_agent_editor.video.make_intro_montage import write_concat_list


def build_concatenate_video_command(
    *,
    concat_list_path: Path,
    output_path: Path,
    ffmpeg_bin: str = "ffmpeg",
) -> list[str]:
    return [
        ffmpeg_bin,
        "-hide_banner",
        "-n",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_list_path),
        "-c",
        "copy",
        str(output_path),
    ]


def concatenate_intro_with_video(
    *,
    intro_path: Path,
    video_path: Path,
    output_path: Path = Path("outputs/final/final_video.mp4"),
    dry_run: bool = False,
    ffmpeg_bin: str = "ffmpeg",
) -> list[str]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list_path = output_path.with_suffix(".txt")
    write_concat_list([intro_path, video_path], concat_list_path)
    command = build_concatenate_video_command(
        concat_list_path=concat_list_path,
        output_path=output_path,
        ffmpeg_bin=ffmpeg_bin,
    )
    if not dry_run:
        subprocess.run(command, check=True)
    return command
