"""Command-line interface for MindForge."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .engine import MindForge


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="MindForge Agentic OS")
    parser.add_argument("command", choices=["ask", "remember", "plan", "reflect", "status"], help="Action to perform")
    parser.add_argument("text", nargs="?", help="Text for the command")
    parser.add_argument("--memory-file", default="~/.mindforge/memory.json", help="Path to the JSON memory file")
    return parser


def main() -> None:
    args = build_parser().parse_args()
    engine = MindForge(memory_path=Path(args.memory_file).expanduser())

    if args.command == "remember":
        if not args.text:
            raise SystemExit("Remember requires text to store.")
        memory = engine.remember(args.text, title="Memory", tags=["insight", "personal"], source="cli")
        print(json.dumps({"stored": True, "memory": memory}, indent=2))
        return

    if args.command == "ask":
        if not args.text:
            raise SystemExit("Ask requires a question.")
        print(engine.ask(args.text))
        return

    if args.command == "plan":
        if not args.text:
            raise SystemExit("Plan requires an objective.")
        print(json.dumps(engine.plan(args.text), indent=2))
        return

    if args.command == "reflect":
        if not args.text:
            raise SystemExit("Reflect requires a prompt.")
        print(engine.reflect(args.text))
        return

    print(json.dumps(engine.dashboard(), indent=2))


if __name__ == "__main__":
    main()
