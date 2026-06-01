from __future__ import annotations


def require_keys(data: dict[str, object], required_keys: set[str], *, schema_name: str) -> None:
    missing = sorted(required_keys - data.keys())
    if missing:
        raise ValueError(f"{schema_name} is missing required keys: {', '.join(missing)}")
