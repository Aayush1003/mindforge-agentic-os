"""Memory utilities for MindForge."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryStore:
    """Persistent memory store for notes, goals, and context."""

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except json.JSONDecodeError:
            return []

    def _write(self, data: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(self, text: str, *, tags: list[str] | None = None, source: str = "user", importance: float = 1.0) -> dict[str, Any]:
        memory = {
            "id": f"mem-{len(self._read()) + 1}",
            "text": text.strip(),
            "tags": [tag.strip().lower() for tag in (tags or []) if tag and tag.strip()],
            "source": source,
            "importance": max(0.1, min(5.0, float(importance))),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        records = self._read()
        records.append(memory)
        self._write(records)
        return memory

    def search(self, query: str, *, limit: int = 5) -> list[dict[str, Any]]:
        q = query.lower().strip()
        if not q:
            return self.recent(limit=limit)

        records = self._read()
        scored: list[tuple[float, dict[str, Any]]] = []
        for record in records:
            text = (record.get("text") or "").lower()
            tags = " ".join(record.get("tags") or []).lower()
            score = 0.0
            if q in text:
                score += 3.0
            score += sum(0.5 for token in q.split() if token in text)
            score += sum(0.7 for token in q.split() if token in tags)
            score += float(record.get("importance") or 1.0)
            if score > 0:
                scored.append((score, record))

        scored.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in scored[:limit]]

    def recent(self, *, limit: int = 5) -> list[dict[str, Any]]:
        records = self._read()
        return list(reversed(records))[:limit]

    def count(self) -> int:
        return len(self._read())
