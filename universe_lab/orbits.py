"""Explore Kepler's third law through a scale-change experiment."""

from __future__ import annotations

import argparse
import json


def compare_orbit_scales(radius_factor: float = 4.0) -> dict[str, object]:
    """Calculate how orbital period changes when orbital radius is scaled."""
    if not 0 < radius_factor <= 1_000_000:
        raise ValueError("radius_factor must be greater than 0 and at most 1,000,000")

    period_factor = radius_factor ** 1.5
    return {
        "experiment": "Kepler's third law scale relation",
        "equation": "T^2 / a^3 = 4*pi^2 / (G*M)",
        "assumption": "Newtonian gravity with the same central mass M",
        "orbital_radius_scale_factor": radius_factor,
        "orbital_period_scale_factor": period_factor,
        "interpretation": (
            f"Scaling orbital radius by {radius_factor:g} scales the period "
            f"by {period_factor:g}; specifically, T is proportional to a^(3/2)."
        ),
        "caveat": (
            "This is a consequence of the idealized two-body model, not a "
            "complete description of every orbit."
        ),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--radius-factor",
        type=float,
        default=4.0,
        help="Orbital radius scale factor, greater than 0 and at most 1,000,000",
    )
    args = parser.parse_args()
    print(json.dumps(compare_orbit_scales(args.radius_factor), indent=2))


if __name__ == "__main__":
    main()
