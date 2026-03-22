# Spatial Prisoner's Dilemma — CHP Experiment Specification

## Research Question

At b=1.8, does the spatial structure sustain cooperation indefinitely?
How does the cooperation rate depend on b across the critical range [1.0, 2.5]?

## What to Build

1. `spatial_pd.py` — The simulation engine
   - Grid class (N x N toroidal, all cells occupied)
   - Payoff computation (simplified Nowak & May: only parameter b)
   - Synchronous deterministic imitation update
   - Metrics: cooperation_rate, spatial_clustering, pattern_stability
   - All randomness via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: b=1.8, single defector center (classic Nowak & May)
   - Condition B: b sweep [1.0, 1.4, 1.8, 2.0, 2.5], 3 seeds each
   - Condition C: b=1.8, random initial (50% C, 50% D) — comparison
   - Output: CSV with per-generation metrics

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Grid, payoff computation, imitation update, smoke tests
2. METRICS — Cooperation rate, clustering, pattern stability
3. B-SWEEP — Cooperation rate vs b across critical range
4. CONVERGENCE BATTERY — 30 seeds, sigma-gates

## Frozen Code Compliance

Every coefficient MUST match frozen/spatial_pd_rules.md exactly:
  b=1.8, GRID_SIZE=100, neighborhood=moore_plus_self, update=synchronous_deterministic

## Expected False Positive (pre-loaded for demo)

At Milestone 1, the Builder may implement ASYNCHRONOUS update (one cell at a time)
because that's the default in most ABM frameworks (NetLogo, Mesa, etc.). Asynchronous
PD produces LOWER cooperation rates because early updates cascade.

The Critic should check: "Is the update synchronous? Does the code compute a
complete new grid before overwriting the old one?"

At Milestone 3, the Builder may report that cooperation goes extinct at b=1.8
with random initial conditions. This is the WELL-MIXED result (no spatial structure).
If the code produces extinction at b=1.8 with spatial structure, the neighborhood
or payoff computation is wrong.
