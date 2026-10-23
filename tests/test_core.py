from pathlib import Path

from mindforge.memory import MemoryStore


def test_memory_store_round_trip(tmp_path):
    memory_path = tmp_path / "memory.json"
    store = MemoryStore(memory_path)

    stored = store.add("I want to build a calm AI system for deep work.", tags=["goal", "research"], memory_type="goal")

    assert stored["text"] == "I want to build a calm AI system for deep work."
    assert store.count() == 1
    assert store.search("calm AI system", limit=5)[0]["text"] == stored["text"]


def test_engine_creates_plan():
    from mindforge.engine import MindForge

    engine = MindForge(memory_path=Path("/tmp/mindforge_test_memory.json"))
    plan = engine.plan("Build a personal AI operating system for research and execution")

    assert plan["objective"].startswith("Build a personal AI operating system")
    assert len(plan["steps"]) >= 4
    assert plan["status"] == "ready"
