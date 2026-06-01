from pathlib import Path

from yt_agent_editor.video.concatenate_video import build_concatenate_video_command
from yt_agent_editor.video.extract_clips import build_extract_clip_command
from yt_agent_editor.video.make_intro_montage import build_intro_montage_command
from yt_agent_editor.video.probe_video import build_ffprobe_command


def test_extract_clip_command_uses_no_overwrite_and_output_path() -> None:
    command = build_extract_clip_command(
        video_path=Path("inputs/video.mp4"),
        start_seconds=1.25,
        end_seconds=4.75,
        output_path=Path("outputs/clips/hook-01.mp4"),
    )

    assert command[:3] == ["ffmpeg", "-hide_banner", "-n"]
    assert "inputs/video.mp4" in command
    assert command[-1] == "outputs/clips/hook-01.mp4"
    assert command[command.index("-t") + 1] == "3.500"


def test_intro_montage_command() -> None:
    command = build_intro_montage_command(
        concat_list_path=Path("outputs/final/intro_montage.txt"),
        output_path=Path("outputs/final/intro_montage.mp4"),
    )

    assert command[:3] == ["ffmpeg", "-hide_banner", "-n"]
    assert command[-1] == "outputs/final/intro_montage.mp4"


def test_concatenate_video_command() -> None:
    command = build_concatenate_video_command(
        concat_list_path=Path("outputs/final/final_video.txt"),
        output_path=Path("outputs/final/final_video.mp4"),
    )

    assert "-f" in command
    assert "concat" in command
    assert command[-1] == "outputs/final/final_video.mp4"


def test_ffprobe_command() -> None:
    command = build_ffprobe_command(Path("inputs/video.mp4"))

    assert command[0] == "ffprobe"
    assert command[-1] == "inputs/video.mp4"
