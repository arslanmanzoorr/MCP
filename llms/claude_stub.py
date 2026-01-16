"""Claude adapter stub.

Your programmer should replace this with the Anthropic Claude SDK / Agent SDK calls.
The engine expects a Python dict that matches schemas/universal_reasoning_schema.json.

Tip: enforce JSON-only output using the SDK's structured output / JSON mode (if available)
or by prompting + strict parsing + retry.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List

from .base import ReasoningLLM


class ClaudeLLMStub(ReasoningLLM):
    def __init__(self):
        pass

    def generate(self, *, system: str, user: str, context_chunks: List[Dict[str, str]]) -> Dict[str, Any]:
        # Placeholder deterministic output for wiring tests.
        return {
            "question": user,
            "given_information": [c["text"][:180] for c in context_chunks],
            "assumptions": ["Assumption: Only the provided context is authoritative for constraints."],
            "reasoning_steps": [
                "Identify constraints from retrieved context.",
                "Apply constraints to the user question.",
                "State limitations where facts are missing.",
            ],
            "alternative_views": ["An alternative interpretation could exist depending on missing facts."],
            "limitations": ["This is a stub output; replace with real Claude SDK calls.", "Insufficient case-specific facts were provided."],
            "conclusion": "Stub conclusion. Replace with real Claude output.",
            "confidence": 0.3,
        }

    def revise(self, *, system: str, user: str, context_chunks: List[Dict[str, str]], draft: Dict[str, Any], feedback: List[str]) -> Dict[str, Any]:
        draft = dict(draft)
        draft["limitations"] = list(draft.get("limitations", [])) + ["Revision requested: " + "; ".join(feedback)]
        draft["confidence"] = min(float(draft.get("confidence", 0.3)), 0.5)
        return draft
