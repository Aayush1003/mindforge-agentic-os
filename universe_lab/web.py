"""Serve the local Universe Lab interface and experiment API."""

from __future__ import annotations

import argparse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

from .antigravity import required_lift_force
from .chaos import compare_nearby_trajectories
from .orbits import compare_orbit_scales
from mindforge.ramanujan import ramanujan_pi_demo


_PAGE = Path(__file__).with_name("web") / "index.html"


class UniverseLabHandler(BaseHTTPRequestHandler):
    """Handle a static app page and read-only local experiment endpoints."""

    def do_GET(self) -> None:
        request = urlsplit(self.path)
        if request.path == "/":
            self._send(200, _PAGE.read_bytes(), "text/html; charset=utf-8")
            return

        try:
            query = parse_qs(request.query, strict_parsing=True)
            result = self._experiment(request.path, query)
        except ValueError as error:
            self._send_json(400, {"error": str(error)})
            return

        if result is None:
            self._send_json(404, {"error": "Not found"})
            return
        self._send_json(200, result)

    @staticmethod
    def _experiment(path: str, query: dict[str, list[str]]) -> dict[str, object] | None:
        def number(name: str, default: float) -> float:
            values = query.get(name)
            if values is None:
                return default
            if len(values) != 1:
                raise ValueError(f"{name} must be provided once")
            try:
                return float(values[0])
            except ValueError as error:
                raise ValueError(f"{name} must be a number") from error

        if path == "/api/chaos":
            steps = number("steps", 40)
            if not steps.is_integer():
                raise ValueError("steps must be an integer")
            return compare_nearby_trajectories(steps=int(steps))
        if path == "/api/orbits":
            return compare_orbit_scales(number("radius_factor", 4))
        if path == "/api/antigravity":
            return required_lift_force(
                mass_kg=number("mass_kg", 0.01),
                lift_cm=number("lift_cm", 1),
                time_s=number("time_s", 1),
            )
        if path == "/api/ramanujan":
            terms = number("terms", 3)
            if not terms.is_integer():
                raise ValueError("terms must be an integer")
            return ramanujan_pi_demo(terms=int(terms))
        return None

    def _send_json(self, status: int, data: dict[str, object]) -> None:
        payload = json.dumps(data).encode("utf-8")
        self._send(status, payload, "application/json; charset=utf-8")

    def _send(self, status: int, payload: bytes, content_type: str) -> None:
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(payload)

    def log_message(self, format: str, *args: object) -> None:
        print(f"[Universe Lab] {self.address_string()} - {format % args}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="127.0.0.1", help="Bind address (defaults to localhost)")
    parser.add_argument("--port", type=int, default=8765, help="Port to serve on")
    args = parser.parse_args()
    if not 0 < args.port < 65536:
        parser.error("--port must be between 1 and 65535")

    server = ThreadingHTTPServer((args.host, args.port), UniverseLabHandler)
    print(f"Universe Lab is running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping Universe Lab.")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
