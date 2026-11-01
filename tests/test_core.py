from pathlib import Path
from http.server import ThreadingHTTPServer
import json
import threading
from urllib.error import HTTPError
from urllib.request import urlopen

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


def test_pendulum_experiment_shows_small_angle_model_error():
    from mindforge.physics import run_pendulum_experiment

    result = run_pendulum_experiment()

    assert result["conditions"]["initial_angle_degrees"] == 90
    assert result["small_angle_mean_absolute_error_degrees"] > 1
    assert result["small_angle_max_absolute_error_degrees"] > result[
        "small_angle_mean_absolute_error_degrees"
    ]


def test_ramanujan_pi_series_converges_rapidly():
    from decimal import Decimal

    from mindforge.ramanujan import ramanujan_pi_demo

    result = ramanujan_pi_demo(terms=2)
    estimates = result["estimates"]

    assert len(estimates) == 2
    assert Decimal(estimates[0]["absolute_error"]) < Decimal("0.000001")
    assert Decimal(estimates[1]["absolute_error"]) < Decimal(estimates[0]["absolute_error"])


def test_logistic_map_experiment_reports_divergence():
    from universe_lab.chaos import compare_nearby_trajectories

    result = compare_nearby_trajectories()

    assert result["first_step_with_separation_over_0_1"] is not None
    assert result["separation_after_20_steps"] > result["initial_separation"]
    assert result["final_separation"] > result["separation_after_20_steps"]


def test_kepler_orbit_scale_matches_three_halves_power_law():
    from universe_lab.orbits import compare_orbit_scales

    result = compare_orbit_scales(4)

    assert result["orbital_period_scale_factor"] == 8


def test_lift_force_calculator_uses_newtonian_motion():
    from universe_lab.antigravity import required_lift_force

    result = required_lift_force(mass_kg=0.01, lift_cm=1, time_s=1)

    assert result["net_upward_force_above_weight_newtons"] == 0.0002
    assert result["total_upward_force_required_newtons"] > result["earth_weight_newtons"]


def test_local_web_interface_serves_page_and_validates_api_inputs():
    from universe_lab.web import UniverseLabHandler

    server = ThreadingHTTPServer(("127.0.0.1", 0), UniverseLabHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base_url = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(base_url) as response:
            page = response.read().decode("utf-8")
            assert response.status == 200
            assert "You’re outside." in page
            assert "Land on the glowing target." in page
            assert 'id="physics-game"' in page
            assert 'id="launch-rover"' in page
            assert "Use my measurement" in page

        with urlopen(f"{base_url}/api/orbits?radius_factor=4") as response:
            result = json.loads(response.read())
            assert result["orbital_period_scale_factor"] == 8

        try:
            urlopen(f"{base_url}/api/chaos?steps=not-a-number")
        except HTTPError as error:
            assert error.code == 400
            assert "must be a number" in json.loads(error.read())["error"]
        else:
            raise AssertionError("Invalid API input should return HTTP 400")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
