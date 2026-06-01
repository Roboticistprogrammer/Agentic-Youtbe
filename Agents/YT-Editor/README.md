# YouTube Agent Editor

A small Python CLI package for generating YouTube editing assets from a video file and an SRT transcript.

The MVP is deterministic and works without OpenAI or any other API. It parses `.srt` files, creates mock chapter and hook analysis, and writes report files under `outputs/`.

## Install

```bash
python -m pip install -e ".[dev]"
```

## MVP 1 Usage

Put your files here:

```text
inputs/video.mp4
inputs/transcript.srt
```

Run analysis:

```bash
yt-agent-editor analyze --video inputs/video.mp4 --srt inputs/transcript.srt
```

The command writes:

```text
outputs/reports/chapters.txt
outputs/reports/youtube_description.txt
outputs/reports/hook_candidates.json
outputs/reports/analysis_report.md
```

You can also run the module directly:

```bash
python -m yt_agent_editor.cli analyze --video inputs/video.mp4 --srt inputs/transcript.srt
```

## Video Commands

Video commands are scaffolded with FFmpeg subprocess command generation and dry-run support:

```bash
yt-agent-editor make-intro --video inputs/video.mp4 --hooks outputs/reports/hook_candidates.json --dry-run
yt-agent-editor full --video inputs/video.mp4 --srt inputs/transcript.srt --dry-run
yt-agent-editor export-description --srt inputs/transcript.srt
```

## Tests

```bash
python -m pytest
```

## Architecture

- `src/yt_agent_editor/transcript/`: SRT parsing and transcript merging
- `src/yt_agent_editor/analysis/`: mock analysis, prompt loading, and LLM boundary
- `src/yt_agent_editor/video/`: FFmpeg and FFprobe subprocess command builders
- `src/yt_agent_editor/export/`: report and JSON writers
- `prompts/`: prompt templates for future LLM calls
- `schemas/`: JSON schemas for generated outputs

Generated files should only be written under `outputs/`.
