# Grover's Algorithm — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Grover's Algorithm Simulation (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching classical search contamination
            in a quantum algorithm simulation.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — State vector: array of 2^n complex amplitudes. NOT boolean/classical.
DD02 — Oracle: PHASE FLIP (amplitudes[target] *= -1). NOT boolean return.
DD03 — Diffusion: inversion about mean (2|psi0><psi0| - I). REQUIRED.
DD04 — Order: G = D * O. Oracle FIRST, then diffusion.
DD05 — Optimal k = floor(pi/4 * sqrt(N)). For N=1024: k=25. NOT sqrt(N)=32.
DD06 — Default: n=10 qubits, N=1024 items.
DD07 — Target: random per seed via numpy.random.Generator.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- State vector math via numpy (complex128 or float64).
- All randomness (target selection) via seeded numpy.random.Generator.
- Same seed = same target = identical result.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/grover_rules.md — DO NOT MODIFY.
