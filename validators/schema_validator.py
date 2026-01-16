from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Tuple

from jsonschema import Draft202012Validator


def validate_schema(output: Dict[str, Any], schema_path: str | Path) -> Tuple[bool, List[str]]:
    schema = json.loads(Path(schema_path).read_text(encoding="utf-8"))
    v = Draft202012Validator(schema)
    errors = sorted(v.iter_errors(output), key=lambda e: e.path)
    if not errors:
        return True, []
    msgs = []
    for e in errors:
        loc = ".".join([str(p) for p in e.path])
        msgs.append(f"{loc or '<root>'}: {e.message}")
    return False, msgs
