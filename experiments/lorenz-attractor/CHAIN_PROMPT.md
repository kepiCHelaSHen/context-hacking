# Lorenz Attractor — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Lorenz Attractor (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching Euler integration contamination
            and rounded constant drift in chaotic systems.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Equations: dx/dt = sigma*(y-x), dy/dt = x*(rho-z)-y, dz/dt = x*y-beta*z.
DD02 — Parameters: sigma=10.0, rho=28.0, beta=8.0/3.0 (NOT 2.667).
DD03 — Initial conditions: (1.0, 1.0, 1.0). NOT (0, 1, 0) from the paper.
DD04 — Integration: ADAPTIVE RK45 via scipy.integrate.solve_ivp.
DD05 — NOT Euler. NOT fixed-step RK4. ADAPTIVE step size required.
DD06 — Tolerances: rtol=1e-9, atol=1e-9 (tight for chaotic accuracy).
DD07 — Time span: [0, 50], 10,000 output points.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- Deterministic: no randomness in integration. Different ICs via perturbation.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/lorenz_rules.md — DO NOT MODIFY.
