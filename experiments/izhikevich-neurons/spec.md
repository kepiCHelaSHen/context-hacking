# Izhikevich Neurons — CHP Experiment Specification

## Research Question

Can the Izhikevich model reproduce all 5 frozen firing patterns with correct
ISI statistics? Does the two-half-step integration method matter vs single step?

## What to Build

1. `izhikevich.py` — Spiking neuron simulator
   - IzhikevichNeuron class with v, u state variables and a, b, c, d parameters
   - Two-half-step Euler integration (dt=0.5 ms)
   - Spike detection (v >= 30) with reset (v=c, u+=d)
   - Metrics: spike_count, spike_times, ISI stats, voltage bounds
   - All randomness via seeded numpy.random.Generator (for network noise)

2. `run_experiment.py` — Experiment runner
   - Condition A: All 5 firing patterns (RS, IB, CH, FS, LTS), 30 seeds each
   - Condition B: Single-step (dt=1.0) vs half-step (dt=0.5) comparison
   - Output: per-pattern spike rasters, ISI distributions, voltage traces

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — Neuron class, integration, spike detection, reset
2. PATTERNS — All 5 firing patterns with correct ISI statistics
3. COMPARISON — Half-step vs single-step, ISI accuracy
4. CONVERGENCE BATTERY — 30 seeds per pattern, sigma-gates on ISI

## Expected False Positive

At Milestone 1, the Builder produces a "spiking neuron" using Hodgkin-Huxley
equations (4 variables: V, m, h, n) with conductance parameters (gNa, gK, gL).
The model spikes correctly but is the WRONG MODEL. The Critic catches it by
checking: "How many state variables? What are the parameter names?"

At Milestone 2, the Builder uses dt=1.0 (single full step) instead of dt=0.5
(two half-steps). The RS pattern still looks correct but the spike timing is
off by ~2-5%, detectable across 30 seeds in the ISI sigma-gate.
