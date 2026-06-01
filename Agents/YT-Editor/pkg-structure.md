youtube-agent-editor/
│
├── README.md
├── pyproject.toml
├── .env.example
├── .gitignore
├── config.yaml
│
├── inputs/
│   ├── sample_video.mp4
│   └── sample_transcript.srt
│
├── outputs/
│   ├── reports/
│   ├── clips/
│   ├── thumbnails/
│   └── final/
│
├── prompts/
│   ├── chapter_generator.md
│   ├── hook_detector.md
│   ├── broll_detector.md
│   ├── youtube_description.md
│   ├── title_generator.md
│   └── shorts_detector.md
│
├── schemas/
│   ├── chapters.schema.json
│   ├── hook_segments.schema.json
│   ├── broll_segments.schema.json
│   ├── youtube_metadata.schema.json
│   └── full_analysis.schema.json
│
├── src/
│   └── yt_agent_editor/
│       ├── __init__.py
│       ├── cli.py
│       ├── config.py
│       ├── models.py
│       │
│       ├── transcript/
│       │   ├── __init__.py
│       │   ├── parse_srt.py
│       │   ├── parse_txt.py
│       │   ├── clean_transcript.py
│       │   └── merge_segments.py
│       │
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── llm_client.py
│       │   ├── generate_chapters.py
│       │   ├── detect_hooks.py
│       │   ├── detect_broll.py
│       │   ├── detect_shorts.py
│       │   └── score_segments.py
│       │
│       ├── video/
│       │   ├── __init__.py
│       │   ├── probe_video.py
│       │   ├── extract_clips.py
│       │   ├── make_intro_montage.py
│       │   ├── concatenate_video.py
│       │   ├── add_text_overlay.py
│       │   └── export_final.py
│       │
│       ├── export/
│       │   ├── __init__.py
│       │   ├── youtube_description.py
│       │   ├── json_report.py
│       │   ├── markdown_report.py
│       │   ├── csv_segments.py
│       │   └── otio_timeline.py
│       │
│       └── utils/
│           ├── __init__.py
│           ├── timecode.py
│           ├── file_utils.py
│           └── validation.py
│
├── scripts/
│   ├── run_full_pipeline.py
│   ├── analyze_transcript.py
│   ├── create_intro_from_hooks.py
│   ├── export_youtube_description.py
│   └── create_shorts.py
│
└── tests/
    ├── test_srt_parser.py
    ├── test_timecode.py
    ├── test_chapter_rules.py
    └── test_clip_extraction.py
