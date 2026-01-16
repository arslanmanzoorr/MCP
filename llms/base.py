from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class ReasoningLLM(ABC):
    """Pluggable LLM interface for the engine."""

    @abstractmethod
    def generate(self, *, system: str, user: str, context_chunks: List[Dict[str, str]]) -> Dict[str, Any]:
        """Return a dict matching the universal schema."""

    @abstractmethod
    def revise(self, *, system: str, user: str, context_chunks: List[Dict[str, str]], draft: Dict[str, Any], feedback: List[str]) -> Dict[str, Any]:
        """Return a revised dict matching the universal schema."""
