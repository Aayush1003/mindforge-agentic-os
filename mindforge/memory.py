"""Memory layer for MindForge."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class MemoryStore:
    """Persistent memory store with typed memory entries and keyword retrieval."""

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("[]", encoding="utf-8")

    def _read(self) -> list[dict[str, Any]]:
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, OSError):
            return []

    def _write(self, data: list[dict[str, Any]]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def add(
        self,
        text: str,
        *,
        title: str | None = None,
        memory_type: str = "note",
        tags: list[str] | None = None,
        source: str = "user",
        importance: float = 1.0,
    ) -> dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Memory text cannot be empty.")

        normalized = text.strip()
        record = {
            "id": f"mem-{len(self._read()) + 1}",
            "title": title or normalized[:48] or "untitled memory",
            "type": memory_type,
            "text": normalized,
            "tags": [tag.strip().lower() for tag in (tags or []) if tag and tag.strip()],
            "source": source,
            "importance": max(0.1, min(5.0, float(importance))),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        records = self._read()
        records.append(record)
        self._write(records)
        return record

    def search(self, query: str, *, memory_type: str | None = None, limit: int = 5) -> list[dict[str, Any]]:
        q = query.lower().strip()
        if not q:
            return self.recent(limit=limit)

        ranked: list[tuple[float, dict[str, Any]]] = []
        for record in self._read():
            if memory_type and record.get("type") != memory_type:
                continue

            text = (record.get("text") or "").lower()
            title = (record.get("title") or "").lower()
            tags = " ".join(record.get("tags") or []).lower()
            score = 0.0

            if q in text:
                score += 4.0
            if q in title:
                score += 2.0
            score += sum(0.5 for token in q.split() if token in text)
            score += sum(0.7 for token in q.split() if token in tags)
            score += float(record.get("importance") or 1.0)

            if score > 0:
                ranked.append((score, record))

        ranked.sort(key=lambda item: item[0], reverse=True)
        return [record for _, record in ranked[:limit]]

    def recent(self, *, limit: int = 5) -> list[dict[str, Any]]:
        records = self._read()
        return list(reversed(records))[:limit]

    def by_type(self, memory_type: str, *, limit: int = 10) -> list[dict[str, Any]]:
        records = [record for record in self._read() if record.get("type") == memory_type]
        return records[-limit:]

    def count(self) -> int:
        return len(self._read())

    def stats(self) -> dict[str, Any]:
        records = self._read()
        by_type: dict[str, int] = {}
        for record in records:
            key = record.get("type", "note")
            by_type[key] = by_type.get(key, 0) + 1
        return {"total": len(records), "by_type": by_type}
