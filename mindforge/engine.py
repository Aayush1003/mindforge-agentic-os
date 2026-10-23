"""Core reasoning engine for MindForge."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from .memory import MemoryStore
from .mission import MissionBoard


@dataclass
class SessionLog:
    question: str
    answer: str
    related_memories: list[str] = field(default_factory=list)


class MindForge:
    """Memory-first reasoning and planning engine."""

    def __init__(self, memory_path: str | Path = "~/.mindforge/memory.json"):
        self.memory = MemoryStore(Path(memory_path).expanduser())
        self.missions = MissionBoard()
        self.session_history: list[SessionLog] = []
        self.profile: dict[str, Any] = {
            "name": "MindForge",
            "mode": "memory-first intelligence",
            "focus": ["clarity", "reflection", "memory", "planning", "execution"],
        }

    def remember(self, text: str, *, title: str | None = None, memory_type: str = "note", tags: list[str] | None = None, source: str = "user") -> dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Memory text cannot be empty.")
        return self.memory.add(text, title=title, memory_type=memory_type, tags=tags or [], source=source)

    def capture_goal(self, goal: str, *, tags: list[str] | None = None) -> dict[str, Any]:
        if not goal or not goal.strip():
            raise ValueError("Goal cannot be empty.")
        memory = self.remember(goal, title="Goal", memory_type="goal", tags=tags or ["mission", "intent"], source="mindforge")
        self.missions.add(
            title=memory["title"],
            objective=goal.strip(),
            tags=tags or ["mission", "intent"],
        )
        return memory

    def ask(self, question: str) -> str:
        if not question or not question.strip():
            raise ValueError("Question cannot be empty.")

        q = question.strip()
        related = self.memory.search(q, limit=3)
        answer = self._compose_response(q, related)
        self.session_history.append(
            SessionLog(
                question=q,
                answer=answer,
                related_memories=[item.get("text", "") for item in related],
            )
        )
        return answer

    def plan(self, objective: str) -> dict[str, Any]:
        if not objective or not objective.strip():
            raise ValueError("Objective cannot be empty.")

        cleaned = objective.strip()
        self.capture_goal(cleaned, tags=["plan", "mission"])
        steps = self._build_plan(cleaned)
        mission = {
            "objective": cleaned,
            "steps": steps,
            "status": "ready",
            "created_at": self.missions.latest()["created_at"],
        }
        return mission

    def reflect(self, prompt: str) -> str:
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        memories = self.memory.search(prompt, limit=4)
        if not memories:
            return (
                "Reflection\n\n"
                "- The system has no direct memory for this prompt yet.\n"
                "- Begin by capturing the user objective and then define the next meaningful step.\n"
                "- Think in terms of intention, constraints, and useful movement."
            )

        return (
            "Reflection\n\n"
            + "\n".join(f"- {entry['text']}" for entry in memories)
            + "\n\n"
            + "- The pattern here suggests a deeper theme: clarify the mission, reduce uncertainty, and execute the next obvious step."
        )

    def dashboard(self) -> dict[str, Any]:
        memory_stats = self.memory.stats()
        recent = [
            {"question": session.question, "answer_preview": session.answer[:140]}
            for session in self.session_history[-3:]
        ]
        return {
            "profile": self.profile,
            "memory": memory_stats,
            "missions": self.missions.stats(),
            "session_count": len(self.session_history),
            "recent_sessions": recent,
        }

    def _compose_response(self, question: str, related: list[dict[str, Any]]) -> str:
        memory_context = "\n".join(f"- {item['text']}" for item in related) if related else "- No directly matching memories yet."
        understanding = self._understanding(question)
        synthesis = self._synthesis(question, related)
        next_actions = self._next_actions(question)

        return (
            "MindForge Insight\n\n"
            f"Understanding\n{understanding}\n\n"
            f"Relevant memory\n{memory_context}\n\n"
            f"Synthesis\n{synthesis}\n\n"
            f"Next actions\n{next_actions}"
        )

    def _understanding(self, question: str) -> str:
        lowered = question.lower()
        if any(word in lowered for word in ["plan", "build", "design", "system", "roadmap"]):
            return "- The user is asking for directional architecture or strategic structure instead of a single tactical answer."
        if any(word in lowered for word in ["why", "how", "explain", "reason"]):
            return "- This is a reasoning task that benefits from structured interpretation and grounded synthesis."
        if any(word in lowered for word in ["math", "physics", "calculate", "equation"]):
            return "- The request likely needs assumptions, clear variables, and disciplined derivation."
        return "- The user is exploring an idea that deserves context, intent, and a thoughtful transformation into action."

    def _synthesis(self, question: str, related: list[dict[str, Any]]) -> str:
        lowered = question.lower()
        memory_signal = "The memory store supports the direction with relevant context." if related else "No direct memory is present yet, so the answer should be framed as a fresh, adaptable design."

        if "project" in lowered or "system" in lowered or "design" in lowered:
            return (
                "- Build around memory, intention, and an execution loop.\n"
                "- Separate perception, planning, reflection, and action into distinct layers.\n"
                f"- {memory_signal}"
            )
        if "research" in lowered or "study" in lowered:
            return (
                "- Treat the prompt as a research workflow: gather, classify, synthesize, and convert insight into an experiment.\n"
                "- Reduce ambiguity before committing to a final answer.\n"
                f"- {memory_signal}"
            )
        if "code" in lowered or "python" in lowered or "software" in lowered:
            return (
                "- Prototype in small, testable units first.\n"
                "- Prefer clear abstractions and stable data flow over clever, brittle complexity.\n"
                f"- {memory_signal}"
            )
        return (
            "- Frame the answer as a calm, structured response with a clear objective and meaningful next step.\n"
            "- Keep reasoning grounded in intent while leaving room for creativity and adaptation.\n"
            f"- {memory_signal}"
        )

    def _next_actions(self, question: str) -> str:
        lowered = question.lower()
        actions: list[str] = [
            "1. Capture the goal as a durable memory",
            "2. Extract the central constraints and assumptions",
            "3. Turn the result into a concrete next move",
        ]

        if any(word in lowered for word in ["project", "system", "build", "design"]):
            actions.insert(0, "1. Define the minimum viable architecture and clarify the memory layer")
        if any(word in lowered for word in ["research", "study", "analysis"]):
            actions.insert(0, "1. Gather the most relevant evidence and identify the dominant pattern")
        if any(word in lowered for word in ["code", "python", "software", "app"]):
            actions.insert(0, "1. Prototyping in small, testable components before scaling the system")
        return "\n".join(actions)

    def _build_plan(self, objective: str) -> list[dict[str, str]]:
        lower = objective.lower()
        steps = [
            {
                "phase": "Define the mission",
                "purpose": "Clarify the goal, context, and the exact outcome the system is trying to create.",
                "result": "A crisp mission statement with constraints and success signals.",
            },
            {
                "phase": "Map the environment",
                "purpose": "Identify what is already known, missing, or uncertain before taking action.",
                "result": "A structured summary of assumptions and knowledge gaps.",
            },
            {
                "phase": "Build the first useful draft",
                "purpose": "Create a tangible prototype or first version of the work.",
                "result": "A real artifact that can be evaluated, revised, and improved.",
            },
            {
                "phase": "Refine and iterate",
                "purpose": "Use feedback, memory, and reflection to improve quality and clarity.",
                "result": "A stronger final outcome built on evidence and adjustment.",
            },
        ]

        if any(word in lower for word in ["code", "python", "software", "app"]):
            steps[0]["purpose"] = "Clarify the user problem, required behavior, and the core technical constraints."
            steps[1]["purpose"] = "Audit the architecture, dependencies, and the minimal viable implementation path."
            steps[2]["purpose"] = "Write a working prototype that demonstrates the key interaction or workflow."
            steps[3]["purpose"] = "Improve the codebase through testing, clarity, and performance-focused iteration."

        if any(word in lower for word in ["research", "study", "analysis", "learn"]):
            steps[0]["purpose"] = "Define a sharp question and a clear success criterion for the research effort."
            steps[1]["purpose"] = "Collect evidence and classify it by relevance, quality, and novelty."
            steps[2]["purpose"] = "Synthesize the most important findings into a clear narrative and insight map."
            steps[3]["purpose"] = "Refine the answer, validate assumptions, and turn the insight into a useful takeaway."

        return steps
