from __future__ import annotations

from pathlib import Path


def load_prompt(name: str, prompts_dir: Path = Path("prompts")) -> str:
    path = prompts_dir / name
    if path.suffix != ".md":
        path = path.with_suffix(".md")
    return path.read_text(encoding="utf-8")
