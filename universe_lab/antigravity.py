"""Calculate the upward force needed to produce a measurable lift."""

from __future__ import annotations

import argparse
import json


_EARTH_GRAVITY = 9.80665


def required_lift_force(mass_kg: float, lift_cm: float, time_s: float) -> dict[str, object]:
    """Estimate force for constant upward acceleration from rest over a target distance."""
    if not 0 < mass_kg <= 1_000_000:
        raise ValueError("mass_kg must be greater than 0 and at most 1,000,000")
    if not 0 < lift_cm <= 1_000_000:
        raise ValueError("lift_cm must be greater than 0 and at most 1,000,000")
    if not 0 < time_s <= 86_400:
        raise ValueError("time_s must be greater than 0 and at most 86,400")

    lift_m = lift_cm / 100
    acceleration = 2 * lift_m / time_s**2
    net_upward_force = mass_kg * acceleration
    weight = mass_kg * _EARTH_GRAVITY
    total_upward_force = weight + net_upward_force

    return {
        "experiment": "force threshold for a measurable lift",
        "model": "constant acceleration from rest: d = 0.5*a*t^2; F_net = m*a",
        "inputs": {"mass_kg": mass_kg, "lift_cm": lift_cm, "time_s": time_s},
        "earth_weight_newtons": weight,
        "net_upward_force_above_weight_newtons": net_upward_force,
        "total_upward_force_required_newtons": total_upward_force,
        "total_force_as_multiple_of_weight": total_upward_force / weight,
        "interpretation": (
            "The calculated force is a Newtonian benchmark for the stated motion. "
            "It does not show that mental intention produces this force."
        ),
        "measurement_note": (
            "A credible test needs calibrated sensors, randomized intention and "
            "control trials, blinding, and controls for vibration, airflow, heat, "
            "static charge, and magnetic fields."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mass-kg", type=float, default=0.01, help="Test mass in kilograms")
    parser.add_argument("--lift-cm", type=float, default=1.0, help="Target upward displacement in cm")
    parser.add_argument("--time-s", type=float, default=1.0, help="Time interval in seconds")
    args = parser.parse_args()
    result = required_lift_force(args.mass_kg, args.lift_cm, args.time_s)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
