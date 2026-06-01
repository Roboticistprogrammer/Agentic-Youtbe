import json
from pathlib import Path


def test_schema_files_are_valid_json() -> None:
    for path in Path("schemas").glob("*.json"):
        payload = json.loads(path.read_text(encoding="utf-8"))
        assert payload["type"] == "object"
