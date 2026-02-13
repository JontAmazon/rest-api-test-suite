from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import validate


SCHEMA_DIR = Path(__file__).resolve().parents[1] / "schemas"


def load_schema(filename: str) -> dict[str, Any]:
    with open(SCHEMA_DIR / filename, "r", encoding="utf-8") as handle:
        return json.load(handle)


def validate_schema(payload: Any, schema_name: str) -> None:
    schema = load_schema(schema_name)
    validate(instance=payload, schema=schema)
