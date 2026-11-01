"""Demonstrate sensitivity to initial conditions with the logistic map."""

from __future__ import annotations

import argparse
import json


def compare_nearby_trajectories(
    *,
    initial_value: float = 0.2,
    perturbation: float = 1e-12,
    parameter: float = 4.0,
    steps: int = 40,
) -> dict[str, object]:
    """Compare two logistic-map trajectories that start almost identically."""
    if not 0 < initial_value < 1:
        raise ValueError("initial_value must be strictly between 0 and 1")
    if not 0 < initial_value + perturbation < 1:
        raise ValueError("initial_value plus perturbation must be strictly between 0 and 1")
    if not 0 < parameter <= 4:
        raise ValueError("parameter must be in the interval (0, 4]")
    if not 1 <= steps <= 1000:
        raise ValueError("steps must be between 1 and 1000")

    first = initial_value
    second = initial_value + perturbation
    actual_initial_separation = abs(second - first)
    separation_at_10: float | None = None
    separation_at_20: float | None = None
    first_large_divergence_step: int | None = None

    for step in range(1, steps + 1):
        first = parameter * first * (1 - first)
        second = parameter * second * (1 - second)
        separation = abs(first - second)

        if step == 10:
            separation_at_10 = separation
        if step == 20:
            separation_at_20 = separation
        if first_large_divergence_step is None and separation > 0.1:
            first_large_divergence_step = step

    return {
        "experiment": "sensitivity to initial conditions",
        "equation": "x[n+1] = r * x[n] * (1 - x[n])",
        "parameter_r": parameter,
        "starting_values": [initial_value, initial_value + perturbation],
        "initial_separation": actual_initial_separation,
        "separation_after_10_steps": separation_at_10,
        "separation_after_20_steps": separation_at_20,
        "final_separation": abs(first - second),
        "first_step_with_separation_over_0_1": first_large_divergence_step,
        "steps_simulated": steps,
        "interpretation": (
            "A deterministic rule can produce trajectories that quickly become "
            "hard to predict when the starting value is slightly uncertain."
        ),
        "caveat": (
            "This is a numerical illustration of chaos, not evidence that the "
            "universe is random or that a physical law has been broken."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--steps", type=int, default=40, help="Number of iterations (1-1000)")
    args = parser.parse_args()
    print(json.dumps(compare_nearby_trajectories(steps=args.steps), indent=2))


if __name__ == "__main__":
    main()
