from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AppConfig:
    mode: str = "mock"
    outputs_dir: Path = Path("outputs")
    reports_dir: Path = Path("outputs/reports")
    clips_dir: Path = Path("outputs/clips")
    final_dir: Path = Path("outputs/final")
    chapter_interval_seconds: int = 120
    max_merged_segment_chars: int = 700
    ffmpeg_bin: str = "ffmpeg"
    ffprobe_bin: str = "ffprobe"


def default_config() -> AppConfig:
    return AppConfig()
