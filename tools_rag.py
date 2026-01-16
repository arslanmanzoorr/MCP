from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import List


@dataclass
class RagChunk:
    doc_id: str
    title: str
    text: str


def _parse_title_and_body(md_text: str) -> tuple[str, str]:
    lines = [l.strip() for l in md_text.splitlines() if l.strip()]
    title = ""
    body_lines: List[str] = []
    for i, line in enumerate(lines):
        if line.lower().startswith("title:"):
            title = line.split(":", 1)[1].strip()
        else:
            body_lines.append(line)
    return title or "Untitled", "\n".join(body_lines).strip()


def rag_search(paths: List[str], query: str, k: int = 3) -> List[RagChunk]:
    """Very small-test RAG: score docs by keyword overlap. Swap in embeddings later."""
    q = set([w for w in query.lower().split() if len(w) > 2])

    chunks: List[tuple[int, RagChunk]] = []
    for p in paths:
        for fp in Path(p).rglob("*.md"):
            txt = fp.read_text(encoding="utf-8")
            title, body = _parse_title_and_body(txt)
            words = set([w for w in (title + " " + body).lower().split() if len(w) > 2])
            score = len(q.intersection(words))
            chunk = RagChunk(doc_id=str(fp), title=title, text=body)
            chunks.append((score, chunk))

    chunks.sort(key=lambda x: x[0], reverse=True)
    top = [c for s, c in chunks if s > 0][:k]
    # If nothing matches, still return the first k docs as constraints.
    if not top:
        top = [c for _, c in chunks[:k]]
    return top
