# Grover's Algorithm — CHP Experiment Specification

## Research Question

Does the simulated Grover's algorithm achieve the theoretical quadratic speedup?
How does success probability vary with iteration count (the sinusoidal profile)?

## What to Build

1. `grover.py` — State-vector quantum simulation
   - State vector: array of 2^n complex amplitudes
   - Hadamard initialization to equal superposition
   - Oracle: phase flip on target state (amplitude *= -1)
   - Diffusion: inversion about the mean (2|psi0><psi0| - I)
   - Iteration loop: apply G = D * O exactly k times
   - Measurement: |amplitude[target]|^2
   - All target indices via seeded numpy.random.Generator

2. `run_experiment.py` — Experiment runner
   - Condition A: Grover at k_opt=25 (N=1024), 30 seeds (random targets)
   - Condition B: Amplitude evolution curve (k=0..50, single target)
   - Condition C: N sweep [64, 256, 1024, 4096], verify k_opt = floor(pi/4*sqrt(N))
   - Output: per-seed success probability, amplitude curves

3. `tests/test_milestone_battery.py` — Sigma-gated test battery

## Milestones

1. FOUNDATION — State vector, Hadamard, oracle (phase flip), measurement
2. DIFFUSION — Inversion about mean, full Grover iteration G = D * O
3. VERIFICATION — Success probability vs iteration count, optimal k
4. CONVERGENCE BATTERY — 30 random targets, sigma-gates

## Expected False Positive

At Milestone 1, the Builder may implement the oracle as a BOOLEAN function
(returns True if target found) instead of a PHASE FLIP (multiplies amplitude
by -1). A boolean oracle with classical search will find the target in ~N/2
attempts on average. The Critic checks: "Does the iteration count scale as
sqrt(N) or as N?"

At Milestone 2, the Builder may omit the diffusion operator or reverse the
order (apply diffusion before oracle). Without diffusion, the oracle just
flips one phase and nothing accumulates — success probability stays ~1/N
regardless of iterations. The Critic checks the amplitude evolution curve:
it should be sinusoidal, not flat.
