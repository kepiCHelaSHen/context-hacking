# Agent-Based Lotka-Volterra — CHP Experiment Specification

## Research Question

What is the predator extinction probability at default parameters over 500 ticks?
How does it depend on initial population size?

## What to Build

1. `lotka_volterra.py` — Agent-based predator-prey engine
   - Prey and Predator agent classes with energy, position, reproduction
   - Grid with toroidal wrapping and random movement
   - Encounter/eating mechanics (one prey per predator per tick)
   - Metrics: prey_count, predator_count, extinction flags, oscillation stats
   - All randomness via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: Default parameters (200 prey, 50 predators), 30 seeds
   - Condition B: Small population (50 prey, 15 predators), 30 seeds
   - Condition C: Large population (800 prey, 200 predators), 30 seeds
   - 500 ticks each, output: per-tick CSV + extinction summary

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Agents, grid, movement, eating, reproduction, death
2. METRICS — Population counts, extinction detection, oscillation period
3. EXTINCTION EXPERIMENT — Extinction rate vs population size
4. CONVERGENCE BATTERY — 30 seeds, sigma-gates

## Expected False Positive

At Milestone 2, the Builder may report "no extinctions observed in 30 seeds"
at default parameters. This matches the ODE prior (Lotka-Volterra ODEs predict
eternal oscillation). The frozen spec predicts 10-25% predator extinction rate
at N=200/50 over 500 ticks.

If extinction rate = 0% at default N: check for ODE contamination. Is the model
truly agent-based with individual energy and stochastic encounters? Or did the
Builder generate discrete-time Lotka-Volterra difference equations?

The telltale sign: if population trajectories are smooth curves (ODE), not
jagged noisy lines (agent-based), the implementation is wrong.
