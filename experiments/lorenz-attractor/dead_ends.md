# Lorenz Attractor — Dead Ends Log

---

## DEAD END 1 — Fixed-step Euler integration

**What was attempted**: Builder generated x += sigma*(y-x)*dt with dt=0.01.

**Result**: Trajectory looks correct for t < 20 (classic butterfly). At t > 30,
Euler error accumulates exponentially due to chaos (Lyapunov exponent ~0.9).
By t=50, trajectory has diverged from true solution and may go unbounded.
Lyapunov exponent estimate varies wildly across perturbations (std > 0.3).

**Why this is a dead end**: Euler is O(dt) per step. For chaotic systems,
error grows as exp(lambda * t) * O(dt), so total error at t=50 is
exp(0.9 * 50) * 0.01 = astronomical. No fixed-step Euler can produce accurate
Lorenz trajectories at t=50 regardless of dt.

**Do NOT repeat**: Any integration with a variable named `dt` at a fixed value.

---

## DEAD END 2 — beta = 2.667 (rounded)

**What was attempted**: Builder used beta = 2.667 instead of 8/3 exactly.

**Result**: Rounding beta from 2.666666... to 2.667 changes the attractor topology
subtly. The Lyapunov exponent shifts to ~0.912 (vs 0.906 at exact 8/3). The
difference is small but detectable across 30 perturbations and constitutes
specification drift from the frozen value.

**Why this is a dead end**: The frozen spec says beta = 8.0/3.0 in Python
(which gives float64 2.6666666666666665). Any truncation is drift.

**Do NOT repeat**: Hardcoding beta as a decimal literal. Use 8.0/3.0.

---

## DEAD END 3 — Initial conditions (0, 1, 0) from Lorenz's paper

**What was attempted**: Builder used x0=0, y0=1, z0=0, which is the original
Lorenz (1963) initial condition.

**Result**: The Critic flagged this as specification drift. The frozen spec uses
IC = (1.0, 1.0, 1.0) for consistency. Different ICs produce different transient
behavior (first ~5 time units), affecting the Lyapunov estimation window.

**Why this is a dead end**: The LLM generated from the paper's prior (Lorenz 1963)
instead of the frozen spec. This is exactly the Prior-as-Detector pattern.

**Do NOT repeat**: Using any IC other than (1.0, 1.0, 1.0) for the base trajectory.
