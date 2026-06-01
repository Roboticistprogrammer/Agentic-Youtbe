import json

from yt_agent_editor.pipeline import run_analysis


def test_run_analysis_writes_mvp_outputs(tmp_path) -> None:
    srt_path = tmp_path / "transcript.srt"
    srt_path.write_text(
        """1
00:00:00,000 --> 00:00:03,000
Why should you care about this hook?

2
00:02:10,000 --> 00:02:20,000
This section explains the editing workflow.
""",
        encoding="utf-8",
    )
    output_dir = tmp_path / "reports"

    run_analysis(video_path=tmp_path / "video.mp4", srt_path=srt_path, output_dir=output_dir)

    assert (output_dir / "chapters.txt").exists()
    assert (output_dir / "youtube_description.txt").exists()
    hooks = json.loads((output_dir / "hook_candidates.json").read_text(encoding="utf-8"))
    assert hooks["hooks"]
    assert (output_dir / "analysis_report.md").exists()
