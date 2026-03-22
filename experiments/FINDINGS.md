# CHP Multi-Discipline Study — Aggregate Findings

Last updated: 2026-03-22
Experiments complete: 51 / 500 (37 catalog, 13 loop, 0 discovery)

## Key Finding: Self-Correcting Verification

The CHP protocol catches errors at every layer of the system, including errors
in the frozen specifications themselves. This has been observed three times:

### Meta-Spec Error 1: sqrt2-newton (Mathematics)
Newton's method computed sqrt(2) to 10,000 digits. The frozen reference file
contained LLM-hallucinated digits after position 50. The computation served as
ground truth to correct the specification.

### Meta-Spec Error 2: Arrhenius A-factor (Chemistry)
Frozen spec gives A = 1.65e13 for H2+I2, but Arrhenius with Ea = 165,000 J/mol
gives k(700K) = 8.04, not the published 1.65e-3. The A-factor is ~4900x too
high — likely an LLM hallucination in the prompt that specified the constants.

### Meta-Spec Error 3: Blood pH constants (Chemistry)
Frozen pKa = 6.352 (thermodynamic) with alpha = 0.0307 gives pH = 7.64, not
the clinical 7.40. The prompt confused thermodynamic and clinical conventions
for the CO2/bicarbonate system.

**The pattern**: The protocol doesn't care *who* made the error — the prompt
author, the implementation LLM, or the frozen spec. When the math doesn't
check out, the protocol catches it.

## Error Statistics (51 experiments)

| Category | Count | Example |
|---|---|---|
| Unit errors | 5 | Ea in kJ not J, Compton wavelength rounded |
| Sign errors | 10 | van't Hoff, Nernst, Hess, gamma inversion |
| Formula errors | 8 | n² missing in VdW, Tc formula, KE=3/2kT not 1/2 |
| Constant precision | 8 | Kw=1e-14 vs 1.011e-14, g=10 vs 9.80665 |
| Conceptual errors | 6 | pH=7 at all T, Sun peak is yellow (it's green) |
| Convention errors | 5 | Libby vs Godwin, clinical vs thermo pKa |
| **Meta-spec errors** | **3** | **Frozen spec itself wrong** |

## Per-Discipline Summary

### Chemistry (10 cat experiments, 169 tests)
Sprint tag: chemistry-sprint-2026.
61 tests, 21 prior errors caught. Strongest showing of unit/sign/convention
errors. Two meta-spec errors discovered (A-factor, blood pH).

### Physics (20 cat + 1 loop = 21 experiments)
Sprint tag: physics-sprint-2026.
108 tests across batch 1 (mechanics, E&M, optics, relativity, kinetic theory)
and batch 2 (thermo, quantum, nuclear, gravity). Prior errors: g rounding,
gamma inversion, Wien peak color, closed pipe harmonics, 3/2kT vs 1/2kT.

### Mathematics (5 cat experiments)
e, pi, sqrt(2) to 10K-1M digits. Prior errors: algorithm selection (Monte Carlo
for e), float precision ceiling (15 digits). One meta-spec error: hallucinated
reference digits in sqrt(2) frozen file.

### Biology (3 loop experiments)
SIR epidemic, Lotka-Volterra, Izhikevich neurons. Prior errors: deterministic
model contamination, ODE vs agent-based confusion, Hodgkin-Huxley contamination.
All discovered through multi-turn Builder/Critic cycles.

### Physics — Lorenz (1 loop experiment)
Chaotic trajectory confirmed. Prior errors: Euler integration (should be RK45),
wrong initial conditions, truncated beta = 8/3.

### Social Science (2 loop + 2 staged)
Schelling segregation, Spatial Prisoner's Dilemma. Prior errors: sequential vs
simultaneous update, tolerance threshold, initial condition sensitivity.

### Computer Science (3 loop experiments)
Grover's search, PBFT consensus, ML hyperparameter search. Prior errors: oracle
mechanism (boolean not phase-flip), Raft/PBFT confusion, data leakage.

### Music (1 loop experiment)
Metal harmony analysis. Classical theory generates 7 "errors" per Pantera riff;
metal-aware analysis finds 0. Prior-as-detector confirmed.

### Audio DSP (1 loop experiment)
Freeverb: 8 comb filters (not textbook 4), Jezar delay values not derivable
from any formula. Hand-tuned values are the frozen spec.

### Medicine (2 cat experiments)
Anatomy viewers (HTML5 + VTK). Same frozen spec (Gray's Anatomy 41st Edition),
different renderer. Demonstrates protocol is modality-independent.

## Remaining Work

- ~450 experiments to reach 500 target
- Discovery (disc-) experiments not yet started — need LLM-without-spec capture
- Disciplines not yet started: Statistics, Engineering, Economics, Earth Science, Astronomy
- See STUDY_PLAN.md for full experiment list and priority order
