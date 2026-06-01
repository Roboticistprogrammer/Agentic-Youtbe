from __future__ import annotations

from typing import Protocol


class LLMClient(Protocol):
    def complete_json(self, *, prompt: str, schema_name: str) -> dict[str, object]:
        """Return JSON-compatible data for a prompt and schema."""


class NotConfiguredLLMClient:
    def complete_json(self, *, prompt: str, schema_name: str) -> dict[str, object]:
        raise RuntimeError(
            "Real LLM mode is not configured yet. Use mock mode or provide an LLMClient."
        )
