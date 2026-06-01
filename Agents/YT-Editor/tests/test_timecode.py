from yt_agent_editor.utils.timecode import (
    format_ffmpeg_seconds,
    format_srt_timecode,
    format_youtube_timecode,
    parse_timecode,
)


def test_parse_srt_timecode_to_seconds() -> None:
    assert parse_timecode("00:01:02,500") == 62.5
    assert parse_timecode("01:02:03.250") == 3723.25


def test_format_timecodes() -> None:
    assert format_srt_timecode(62.5) == "00:01:02,500"
    assert format_youtube_timecode(0) == "0:00"
    assert format_youtube_timecode(62) == "1:02"
    assert format_youtube_timecode(3723) == "1:02:03"
    assert format_ffmpeg_seconds(1.25) == "1.250"
