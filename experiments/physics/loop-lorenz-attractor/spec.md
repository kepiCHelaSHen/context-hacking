# Lorenz Attractor — CHP Experiment Specification

## Research Question

Does the integration method affect the Lyapunov exponent estimate and attractor
topology at t=50? Can we detect Euler contamination from trajectory statistics?

## What to Build

1. `lorenz.py` — Lorenz system integrator + analysis
   - solve_ivp wrapper with RK45 and frozen tolerances
   - Lyapunov exponent estimation (Benettin algorithm)
   - Attractor bounds check
   - SDIC divergence measurement
   - All parameters from frozen/lorenz_rules.md

2. `run_experiment.py` — Experiment runner
   - Condition A: RK45 adaptive (frozen spec), 30 seeds of perturbed IC
   - Condition B: Fixed-step RK4 at dt=0.01, same ICs — comparison
   - Condition C: Fixed-step Euler at dt=0.01, same ICs — failure demo
   - Output: per-IC trajectory stats, Lyapunov estimates, divergence metrics

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — ODE definition, RK45 integration, basic trajectory
2. METRICS — Lyapunov exponent, bounds, SDIC, fixed-point check
3. COMPARISON — RK45 vs RK4 vs Euler at t=50
4. CONVERGENCE BATTERY — 30 perturbed ICs, sigma-gates on Lyapunov

## Expected False Positive

At Milestone 1, the Builder produces a trajectory using fixed-step Euler at dt=0.01.
For t < 20, it looks perfect — classic butterfly attractor. The Builder reports
"Lorenz attractor verified." But at t=50, the trajectory has diverged from the
true solution. The 30-IC convergence battery at Milestone 4 catches this: Euler
trajectories have inconsistent Lyapunov estimates (high variance) while RK45
estimates are tight (std < 0.15).
