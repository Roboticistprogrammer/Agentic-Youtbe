from yt_agent_editor.transcript import merge_transcript_segments, parse_srt


def test_parse_srt_segments() -> None:
    content = """1
00:00:00,000 --> 00:00:02,000
Hello there.

2
00:00:02,500 --> 00:00:04,000
This is a second
caption line.
"""
    segments = parse_srt(content)

    assert len(segments) == 2
    assert segments[0].index == 1
    assert segments[0].start_seconds == 0
    assert segments[1].text == "This is a second caption line."


def test_merge_transcript_segments_by_gap_and_size() -> None:
    segments = parse_srt(
        """1
00:00:00,000 --> 00:00:02,000
First sentence.

2
00:00:02,400 --> 00:00:04,000
Second sentence.

3
00:00:08,000 --> 00:00:09,000
Later sentence.
"""
    )

    blocks = merge_transcript_segments(segments, max_gap_seconds=1)

    assert len(blocks) == 2
    assert blocks[0].text == "First sentence. Second sentence."
    assert blocks[0].source_indexes == [1, 2]
