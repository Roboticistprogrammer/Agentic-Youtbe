from __future__ import annotations

from pathlib import Path

from yt_agent_editor.pipeline import run_analysis


def main() -> None:
    run_analysis(
        video_path=Path("inputs/video.mp4"),
        srt_path=Path("inputs/transcript.srt"),
        output_dir=Path("outputs/reports"),
        mode="mock",
    )


if __name__ == "__main__":
    main()
