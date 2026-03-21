# Stochastic SIR Epidemic — CHP Experiment Specification

## Research Question

What is the fadeout probability at R0=3.0 with N=500 and I(0)=5?
How does fadeout scale with N across [100, 200, 500, 1000, 5000]?

## What to Build

1. `sir_model.py` — Stochastic individual-based SIR engine
   - Agent list with discrete S/I/R states
   - Per-contact transmission using complement method: p = 1-(1-beta)^k
   - Fixed contacts per tick (K=10, drawn uniformly)
   - Per-tick recovery with probability gamma
   - Metrics: peak, final size, fadeout detection, R0 inference
   - All randomness via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: Default (N=500, I0=5, R0=3.0), 30 seeds
   - Condition B: N sweep [100, 200, 500, 1000, 5000], 10 seeds each
   - Condition C: R0 sweep [1.2, 2.0, 3.0, 5.0], 10 seeds each
   - Output: per-seed summary CSV + per-tick epidemic curves

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Agents, contact sampling, infection, recovery
2. METRICS — Peak, final size, fadeout detection, R0 inference
3. FADEOUT EXPERIMENT — Rate vs N and R0
4. CONVERGENCE BATTERY — 30 seeds, sigma-gates

## Expected False Positive

At Milestone 2, the Builder may report "fadeout rate = 0% across 30 seeds" at
default parameters. This matches the deterministic SIR prediction (R0=3.0 always
produces an epidemic). The stochastic model predicts 5-15% fadeout.

If fadeout = 0%: check for deterministic contamination. Is each agent a discrete
individual? Or did the Builder generate the dS/dt rate equations?

The telltale: if I(t) is a float (e.g., 4.7 infected), it's deterministic.
In the stochastic model, I(t) is always an integer count of discrete agents.
