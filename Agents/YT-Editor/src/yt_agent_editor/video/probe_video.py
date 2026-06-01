from __future__ import annotations

import json
import subprocess
from pathlib import Path


def build_ffprobe_command(video_path: Path, *, ffprobe_bin: str = "ffprobe") -> list[str]:
    return [
        ffprobe_bin,
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        str(video_path),
    ]


def probe_duration_seconds(video_path: Path, *, ffprobe_bin: str = "ffprobe") -> float:
    result = subprocess.run(
        build_ffprobe_command(video_path, ffprobe_bin=ffprobe_bin),
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(result.stdout)
    return float(payload["format"]["duration"])
