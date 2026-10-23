"""Mission board for tracking goals and structured plans."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class MissionBoard:
    """Tracks objectives and plan history for the MindForge system."""

    def __init__(self):
        self._missions: list[dict[str, Any]] = []

    def add(self, *, title: str, objective: str, tags: list[str] | None = None) -> dict[str, Any]:
        mission = {
            "title": title,
            "objective": objective.strip(),
            "tags": [tag.strip().lower() for tag in (tags or []) if tag and tag.strip()],
            "status": "active",
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self._missions.append(mission)
        return mission

    def latest(self) -> dict[str, Any]:
        if not self._missions:
            return {"title": "No missions yet", "objective": "", "status": "idle", "created_at": None}
        return self._missions[-1]

    def stats(self) -> dict[str, Any]:
        return {"total": len(self._missions), "latest": self.latest()}
