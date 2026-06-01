import json

from yt_agent_editor.analysis import detect_hooks, generate_chapters, generate_youtube_description
from yt_agent_editor.export.reports import write_chapters, write_hook_candidates
from yt_agent_editor.models import TranscriptBlock


def sample_blocks() -> list[TranscriptBlock]:
    return [
        TranscriptBlock(
            start_seconds=12,
            end_seconds=24,
            text="Why does this editing mistake ruin retention?",
            source_indexes=[1],
        ),
        TranscriptBlock(
            start_seconds=150,
            end_seconds=170,
            text="Now we fix the timeline and create a stronger intro.",
            source_indexes=[2],
        ),
    ]


def test_chapter_formatting_starts_at_zero(tmp_path) -> None:
    chapters = generate_chapters(sample_blocks())
    output = tmp_path / "chapters.txt"

    write_chapters(output, chapters)

    assert output.read_text(encoding="utf-8").splitlines()[0].startswith("0:00 ")


def test_hook_json_export_validity(tmp_path) -> None:
    hooks = detect_hooks(sample_blocks())
    output = tmp_path / "hook_candidates.json"

    write_hook_candidates(output, hooks)
    payload = json.loads(output.read_text(encoding="utf-8"))

    assert "hooks" in payload
    assert payload["hooks"][0]["id"].startswith("hook-")
    assert 0 <= payload["hooks"][0]["score"] <= 1


def test_mock_description_includes_chapters() -> None:
    chapters = generate_chapters(sample_blocks())
    description = generate_youtube_description(sample_blocks(), chapters)

    assert "Chapters:" in description
    assert "0:00" in description
