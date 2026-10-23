"""Reasoning engine for MindForge."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .memory import MemoryStore


@dataclass
class SessionLog:
    question: str
    answer: str
    related_memories: list[str] = field(default_factory=list)


class MindForge:
    """Memory-first agentic reasoning assistant."""

    def __init__(self, memory_path: str | Path = "~/.mindforge/memory.json"):
        self.memory = MemoryStore(Path(memory_path).expanduser())
        self.session_history: list[SessionLog] = []
        self.profile: dict[str, Any] = {
            "name": "MindForge",
            "mode": "dream-like reasoning",
            "focus": ["clarity", "memory", "research", "creative systems"],
        }

    def remember(self, text: str, *, tags: list[str] | None = None, source: str = "user") -> dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Memory text cannot be empty.")
        memory = self.memory.add(text, tags=tags or [], source=source)
        return memory

    def ask(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        related = self.memory.search(question, limit=3)
        response = self._compose_response(question, related)
        self.session_history.append(
            SessionLog(
                question=question.strip(),
                answer=response,
                related_memories=[item.get("text", "") for item in related],
            )
        )
        return response

    def _compose_response(self, question: str, related: list[dict[str, Any]]) -> str:
        q = question.strip()
        memory_context = "\n".join(f"- {item['text']}" for item in related) if related else "- No directly matching memories found yet."

        understanding = self._understanding(q)
        synthesis = self._synthesis(q, related)
        next_actions = self._next_actions(q)

        return (
            "MindForge Insight\n\n"
            f"Understanding\n{understanding}\n\n"
            f"Relevant memory\n{memory_context}\n\n"
            f"Synthesis\n{synthesis}\n\n"
            f"Next actions\n{next_actions}"
        )

    def _understanding(self, question: str) -> str:
        lowered = question.lower()
        if any(word in lowered for word in ["plan", "build", "roadmap", "system", "design"]):
            return "- The user is asking for a system design or a strategic direction, not just a one-off fix."
        if any(word in lowered for word in ["why", "how", "explain", "reason"]):
            return "- This is a reasoning task: the answer should be structured, grounded, and easy to act on."
        if any(word in lowered for word in ["math", "calculate", "equation", "physics"]):
            return "- This request likely benefits from explicit assumptions, a clear model, and a disciplined derivation."
        return "- The user is exploring an idea that deserves context, intent, and a thoughtful synthesis."

    def _synthesis(self, question: str, related: list[dict[str, Any]]) -> str:
        lowered = question.lower()
        if related:
            memory_signal = "The memory store supports the direction with relevant context."
        else:
            memory_signal = "No direct memory is present yet, so the answer should be framed as a fresh, adaptable design."

        if "project" in lowered or "system" in lowered:
            return (
                "- Build the system around memory, intention, and execution loops.\n"
                "- Keep separate layers for perception, memory, planning, and action.\n"
                f"- {memory_signal}"
            )

        if "research" in lowered or "study" in lowered:
            return (
                "- Treat the question like a research workflow: gather evidence, classify it, and synthesize pattern.\n"
                "- Convert raw information into a strong summary and a concrete next experiment.\n"
                f"- {memory_signal}"
            )

        if "code" in lowered or "python" in lowered:
            return (
                "- Prototype the idea in small, testable units first.\n"
                "- Favor well-named modules and a clean data flow over clever but brittle abstractions.\n"
                f"- {memory_signal}"
            )

        return (
            "- Frame the answer as a calm, structured response with a clear objective and a meaningful next step.\n"
            "- Keep the reasoning grounded in user intent while allowing room for creativity and surprise.\n"
            f"- {memory_signal}"
        )

    def _next_actions(self, question: str) -> str:
        lowered = question.lower()
        actions = [
            "1. Capture the user goal in a durable memory",
            "2. Distill the idea into a small set of constraints",
            "3. Translate the insight into a practical working plan",
        ]

        if any(word in lowered for word in ["project", "system", "build", "design"]):
            actions.insert(0, "1. Define a minimum viable system architecture with a clear memory layer")
        if any(word in lowered for word in ["research", "study", "analysis"]):
            actions.insert(0, "1. Collect the most relevant evidence and summarize the key patterns")
        if any(word in lowered for word in ["code", "python", "app"]):
            actions.insert(0, "1. Write a small working prototype and verify the core interaction")

        return "\n".join(actions)

    def dashboard(self) -> dict[str, Any]:
        return {
            "profile": self.profile,
            "memory_count": self.memory.count(),
            "session_count": len(self.session_history),
            "recent_sessions": [
                {"question": session.question, "answer_preview": session.answer[:120]} for session in self.session_history[-3:]
            ],
        }
