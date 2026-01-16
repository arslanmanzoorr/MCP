"""Local LLM adapter using an OpenAI-compatible chat/completions endpoint.

Works with LM Studio, vLLM, Ollama (with compatibility layer), etc.

Set env vars:
  LOCAL_LLM_BASE_URL (e.g., http://localhost:1234/v1)
  LOCAL_LLM_MODEL    (e.g., mistral, llama)

NOTE: This is optional for the demo. If requests is not installed, keep using the stub.
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, List

import requests

from .base import ReasoningLLM


class LocalOpenAICompatLLM(ReasoningLLM):
    def __init__(self, base_url: str | None = None, model: str | None = None, api_key: str | None = None):
        self.base_url = base_url or os.environ.get("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
        self.model = model or os.environ.get("LOCAL_LLM_MODEL", "local-model")
        self.api_key = api_key or os.environ.get("LOCAL_LLM_API_KEY", "")

    def _call(self, system: str, user: str, context_chunks: List[Dict[str, str]]) -> Dict[str, Any]:
        ctx = "\n\n".join([f"[DOC] {c['title']}\n{c['text']}" for c in context_chunks])
        prompt = (
            "You must output ONLY valid JSON matching this schema keys: "
            "question, given_information, assumptions, reasoning_steps, alternative_views, limitations, conclusion, confidence.\n"
            "Constraints: use only the provided DOCs for normative constraints; if unsure, add to limitations.\n\n"
            f"DOCS:\n{ctx}\n\nQUESTION:\n{user}"
        )

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.2,
        }

        r = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=60)
        r.raise_for_status()
        content = r.json()["choices"][0]["message"]["content"]
        return json.loads(content)

    def generate(self, *, system: str, user: str, context_chunks: List[Dict[str, str]]) -> Dict[str, Any]:
        return self._call(system, user, context_chunks)

    def revise(self, *, system: str, user: str, context_chunks: List[Dict[str, str]], draft: Dict[str, Any], feedback: List[str]) -> Dict[str, Any]:
        rev_user = (
            f"Revise the previous JSON to address these issues: {feedback}. "
            "Return ONLY JSON."
        )
        return self._call(system, rev_user, context_chunks)
