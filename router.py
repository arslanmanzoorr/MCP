from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class RouteResult:
    domain: str
    matched_keywords: List[str]


class DomainRouter:
    """Simple keyword router. Replace with an LLM router later if needed."""

    def __init__(self, config_path: str | Path):
        self.config_path = Path(config_path)
        self.config = json.loads(self.config_path.read_text(encoding="utf-8"))

    def route(self, text: str) -> RouteResult:
        t = text.lower()
        best_domain = "science"
        best_hits: List[str] = []

        for domain, cfg in self.config.items():
            hits = [kw for kw in cfg.get("keywords", []) if re.search(r"\b" + re.escape(kw) + r"\b", t)]
            if len(hits) > len(best_hits):
                best_domain = domain
                best_hits = hits

        return RouteResult(domain=best_domain, matched_keywords=best_hits)
