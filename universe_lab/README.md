# Universe Lab

Small, bounded math experiments: reproducible calculations, measurable outputs,
and clear notes about what each result does and does not establish.

## Interactive web interface

From the repository root, run:

```powershell
python -m universe_lab.web
```

Open `http://127.0.0.1:8765` in a browser. The interface lets you adjust inputs
and run the experiments on this machine. By default, the server binds to
localhost only; use `--port` to choose another local port.

## Co-op game: teach the rover

The web interface opens with a playable rover game. Adjust the power slider,
watch the predicted stopping distance, and launch the rover toward the glowing
target. Earn points for landing within 3 cm; choose another target to keep
playing. The game starts with a 35 cm sample calibration so it can be played
immediately.

To bring in the human side, make a soft paper ball, gently roll it across a
clear, flat floor, measure how far it travels, enter that distance, and select
**Use my measurement**. The simulated rover then uses your observation to
estimate how far a given push travels.

This is a simplified demonstration, not AI training: it assumes the same object,
surface, and a similar gentle push, and the measurement only affects that run.
Keep the test area clear of breakables and roll the paper ball rather than
throwing it. No measurement is sent anywhere.

## Experiment 1: deterministic chaos

Run from the repository root:

```powershell
python -m universe_lab.chaos
```

The logistic map

```text
x[n+1] = r * x[n] * (1 - x[n])
```

is iterated twice with `r = 4` and starting values `0.2` and `0.200000000001`.
The script reports how quickly the trajectories separate. The rule is
deterministic; sensitivity to tiny differences limits long-term prediction.

This illustrates one mathematical idea, not a new physical law or a solution
to every open question about the universe. The iteration is bounded, and
`--steps` can set a limit from 1 to 1000.

## Experiment 2: orbital scale law

Run:

```powershell
python -m universe_lab.orbits
```

Kepler's third law gives `T^2 / a^3 = 4*pi^2 / (G*M)` for an idealized orbit
around a fixed central mass. The default experiment scales orbital radius by
four and calculates the resulting period scale factor, eight. Change the
radius multiplier with `--radius-factor`; it is bounded to keep inputs finite.

## Experiment 3: force needed for a lift

Run:

```powershell
python -m universe_lab.antigravity
```

By default, this estimates the force needed to raise a 10 g test mass by 1 cm
in 1 second from rest. Change the scenario with `--mass-kg`, `--lift-cm`, and
`--time-s`. It uses elementary Newtonian mechanics as a benchmark; it is not
evidence that a person can create lift through intention. A real test would
need calibrated sensors, randomized blinded control trials, and controls for
ordinary disturbances such as vibration and airflow.

The four known fundamental interactions are gravity, electromagnetism, the
strong nuclear interaction, and the weak nuclear interaction. Quantum mechanics
is a framework used to describe physical systems, not a fifth force. No
reproducible evidence currently establishes thought alone as a source of
antigravity. The brain affects the physical world through known pathways,
including neural signals controlling muscles and tools; a claim of an
additional direct force needs a measurable, independently repeatable result.
