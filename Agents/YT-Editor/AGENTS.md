# AGENTS.md

## Project

This repository is a Python package for automating YouTube editing workflows from video files and CapCut SRT transcripts.

## Rules for Codex

- Read `PROJECT_SPEC.md` before making architectural decisions.
- Keep the first version simple and CLI-based.
- Do not build a web app unless explicitly requested.
- Prefer deterministic Python scripts over complicated agent logic.
- Keep LLM calls isolated in `src/yt_agent_editor/analysis/llm_client.py`.
- Make the code usable without API calls by supporting mock outputs.
- Use type hints and `pathlib`.
- Add tests for timecode parsing, SRT parsing, chapter formatting, and clip extraction command generation.
- Do not overwrite user media files.
- Write generated files only under `outputs/`.

## Commands

Use these commands when relevant:

```bash
python -m pytest
python -m yt_agent_editor.cli --help
```

## Done criteria

A task is complete only when:

- Code is implemented
- Tests are added or updated
- Existing tests pass
- README usage is updated if behavior changed
