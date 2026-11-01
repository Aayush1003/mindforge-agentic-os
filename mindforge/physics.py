"""Small, reproducible experiments for comparing physical models."""

from __future__ import annotations

import math


def _simulate_pendulum(
    *,
    initial_angle: float,
    length: float,
    duration: float,
    timestep: float,
    gravity: float,
    linearized: bool,
) -> list[float]:
    def acceleration(angle: float) -> float:
        restoring_angle = angle if linearized else math.sin(angle)
        return -(gravity / length) * restoring_angle

    angle = initial_angle
    velocity = 0.0
    samples = [angle]
    steps = round(duration / timestep)

    for _ in range(steps):
        def derivative(state_angle: float, state_velocity: float) -> tuple[float, float]:
            return state_velocity, acceleration(state_angle)

        k1_angle, k1_velocity = derivative(angle, velocity)
        k2_angle, k2_velocity = derivative(
            angle + timestep * k1_angle / 2,
            velocity + timestep * k1_velocity / 2,
        )
        k3_angle, k3_velocity = derivative(
            angle + timestep * k2_angle / 2,
            velocity + timestep * k2_velocity / 2,
        )
        k4_angle, k4_velocity = derivative(
            angle + timestep * k3_angle,
            velocity + timestep * k3_velocity,
        )

        angle += timestep * (k1_angle + 2 * k2_angle + 2 * k3_angle + k4_angle) / 6
        velocity += timestep * (
            k1_velocity + 2 * k2_velocity + 2 * k3_velocity + k4_velocity
        ) / 6
        samples.append(angle)

    return samples


def run_pendulum_experiment() -> dict[str, object]:
    """Compare a small-angle model with nonlinear dynamics at a 90-degree swing."""
    initial_angle = math.pi / 2
    length = 1.0
    duration = 10.0
    timestep = 0.01
    gravity = 9.81

    reference = _simulate_pendulum(
        initial_angle=initial_angle,
        length=length,
        duration=duration,
        timestep=timestep,
        gravity=gravity,
        linearized=False,
    )
    small_angle = _simulate_pendulum(
        initial_angle=initial_angle,
        length=length,
        duration=duration,
        timestep=timestep,
        gravity=gravity,
        linearized=True,
    )
    errors = [abs(predicted - observed) for predicted, observed in zip(small_angle, reference)]
    return {
        "experiment": "large-angle pendulum model comparison",
        "conditions": {
            "initial_angle_degrees": 90,
            "length_m": length,
            "duration_s": duration,
            "gravity_m_s2": gravity,
            "timestep_s": timestep,
        },
        "equations": {
            "nonlinear_reference": "theta'' = -(g/L) * sin(theta)",
            "small_angle_approximation": "theta'' = -(g/L) * theta",
        },
        "small_angle_mean_absolute_error_degrees": math.degrees(sum(errors) / len(errors)),
        "small_angle_max_absolute_error_degrees": math.degrees(max(errors)),
        "conclusion": (
            "The small-angle approximation diverges at a 90-degree swing; "
            "its assumptions matter when predicting physical behavior."
        ),
        "scope": "A numerical model comparison, not a discovery or violation of physical laws.",
    }
