from __future__ import annotations

import subprocess
from pathlib import Path


def build_intro_montage_command(
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


def write_concat_list(clips: list[Path], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"file '{clip.as_posix()}'" for clip in clips]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def make_intro_montage(
    *,
    clips: list[Path],
    output_path: Path = Path("outputs/final/intro_montage.mp4"),
    dry_run: bool = False,
    ffmpeg_bin: str = "ffmpeg",
) -> list[str]:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    concat_list_path = output_path.with_suffix(".txt")
    write_concat_list(clips, concat_list_path)
    command = build_intro_montage_command(
        concat_list_path=concat_list_path,
        output_path=output_path,
        ffmpeg_bin=ffmpeg_bin,
    )
    if not dry_run:
        subprocess.run(command, check=True)
    return command
