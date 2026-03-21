# Izhikevich Neurons — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Izhikevich Spiking Neurons (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching Hodgkin-Huxley contamination
            when the spec requires the simpler Izhikevich (2003) model.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Model: Izhikevich (2003). TWO variables only: v, u.
DD02 — NOT Hodgkin-Huxley. No gNa, gK, gL. No m, h, n gating variables.
DD03 — Equations: v' = 0.04*v^2 + 5*v + 140 - u + I. Exact coefficients.
DD04 — Integration: two half-steps at dt=0.5 ms (per Izhikevich 2003).
DD05 — Reset: if v >= 30: v = c, u += d.
DD06 — 5 firing patterns: RS, IB, CH, FS, LTS with frozen (a,b,c,d) tuples.
DD07 — Duration: 1000 ms, 2000 steps.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- Deterministic given same parameters (constant I, no noise by default).
- Optional noise via seeded numpy.random.Generator.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/izhikevich_rules.md — DO NOT MODIFY.
