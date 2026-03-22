# Schelling Segregation — CHP Experiment Specification

## Research Question

Does the CHP Dynamic-Tolerance extension produce partial mixing rather than
complete segregation? At what tolerance update rate does the transition occur?

## What to Build

1. `schelling.py` — The simulation engine
   - Grid class (N x N toroidal)
   - Agent class (type, position, tolerance)
   - Step function (simultaneous update)
   - Dynamic tolerance update (per frozen/schelling_rules.md)
   - Metrics: segregation index, cluster count, dissatisfied count
   - All randomness via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: Original Schelling (fixed tolerance 0.375)
   - Condition B: Dynamic tolerance (tolerance_update_rate = 0.005)
   - 30 seeds each, 500 steps
   - Output: CSV with per-step metrics

3. `tests/test_schelling.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Grid, agents, step function, smoke tests
2. METRICS — Segregation index, cluster count, convergence detection
3. DYNAMIC TOLERANCE — Extension implementation, comparison experiment
4. CONVERGENCE BATTERY — 30 seeds, sigma-gates, false-positive check

## Frozen Code Compliance

Every coefficient in schelling.py MUST match frozen/schelling_rules.md exactly:
  GRID_SIZE=50, DENSITY=0.90, TOLERANCE_DEFAULT=0.375, etc.

The Critic will verify by diffing the implementation against the frozen spec.

## Expected False Positive (pre-loaded for demo)

At Milestone 3, the Builder may report "dynamic tolerance produces near-complete
segregation (index ~0.85)" — this matches the TEXTBOOK Schelling result but is
WRONG for the dynamic-tolerance extension. The correct result is partial mixing
(index ~0.5-0.7).

If the Builder reports segregation > 0.80 with dynamic tolerance enabled, the
Critic should flag: "This matches the prior (textbook Schelling) not the spec
(dynamic tolerance). Check tolerance_update_rate implementation."

The most likely error: applying tolerance updates BEFORE the move step instead
of AFTER, which means tolerance changes don't affect the current step's moves
and the model degenerates to standard Schelling.
