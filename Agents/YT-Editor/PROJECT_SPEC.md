# YouTube Agent Editor - Project Specification

I am building a Python package that helps automate my YouTube editing workflow.

## Goal

The package should take:

- A video file, usually exported from CapCut
- A transcript/subtitle file, preferably `.srt`

And generate:

- YouTube chapters/timestamps
- YouTube description draft
- Hook candidates for the intro
- B-roll candidate segments
- Shorts candidate clips
- Optional intro montage created from the best hook clips
- Final video with the hook montage inserted at the beginning

## Main workflow

Input:

- `inputs/video.mp4`
- `inputs/transcript.srt`

Pipeline:

1. Parse SRT transcript
2. Clean and merge transcript segments
3. Generate YouTube chapters
4. Detect hook-worthy moments
5. Detect B-roll candidate moments
6. Detect Shorts candidates
7. Export analysis report as JSON and Markdown
8. Use FFmpeg or MoviePy to extract selected clips
9. Create intro montage from selected hooks
10. Concatenate intro montage with original video
11. Export final YouTube description

## MVP priority

Build MVP 1 first:

- Parse `.srt`
- Generate `chapters.txt`
- Generate `youtube_description.txt`
- Generate `hook_candidates.json`
- Generate `analysis_report.md`

Then build MVP 2:

- Extract clips from `hook_candidates.json`
- Create intro montage
- Export final video

## Preferred architecture

Use Python, Markdown prompt files, JSON schemas, and deterministic scripts.

Do not build a complicated app yet.

Use a CLI command like:

```bash
yt-agent-editor analyze --video inputs/video.mp4 --srt inputs/transcript.srt
yt-agent-editor make-intro --video inputs/video.mp4 --hooks outputs/reports/hook_candidates.json
yt-agent-editor full --video inputs/video.mp4 --srt inputs/transcript.srt
```

## Package structure

Use this structure:

```text
youtube-agent-editor/
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── config.yaml
├── AGENTS.md
├── PROJECT_SPEC.md
├── inputs/
├── outputs/
│   ├── reports/
│   ├── clips/
│   ├── thumbnails/
│   └── final/
├── prompts/
│   ├── chapter_generator.md
│   ├── hook_detector.md
│   ├── broll_detector.md
│   ├── youtube_description.md
│   ├── title_generator.md
│   └── shorts_detector.md
├── schemas/
│   ├── chapters.schema.json
│   ├── hook_segments.schema.json
│   ├── broll_segments.schema.json
│   ├── youtube_metadata.schema.json
│   └── full_analysis.schema.json
├── src/
│   └── yt_agent_editor/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       ├── transcript/
│       ├── analysis/
│       ├── video/
│       ├── export/
│       └── utils/
├── scripts/
└── tests/
```

## Engineering requirements

- Use Python 3.10+
- Prefer simple readable code
- Use type hints
- Use pathlib
- Use pydantic if helpful for data models
- Use pytest for tests
- Use ruff if adding linting
- Use FFmpeg through subprocess for reliable video cutting
- Keep LLM calls isolated in `analysis/llm_client.py`
- Do not require OpenAI API for basic tests
- Add mock/test mode for LLM outputs

## Done means

The project is done when:

- `pytest` passes
- Running the sample command produces:
  - `outputs/reports/chapters.txt`
  - `outputs/reports/youtube_description.txt`
  - `outputs/reports/hook_candidates.json`
  - `outputs/reports/analysis_report.md`
- The codebase has a clear README with usage instructions
