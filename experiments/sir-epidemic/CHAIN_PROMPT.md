# Stochastic SIR Epidemic — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Stochastic SIR Epidemic (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching deterministic contamination
            in a stochastic epidemic model.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Individual agents: each person is a discrete object with state S/I/R.
DD02 — Infection: per-contact complement method. p = 1 - (1-beta)^k_infected.
DD03 — NOT mass-action: do NOT use beta * S * I / N.
DD04 — Fixed contacts: exactly K=10 per tick, NOT Poisson-distributed.
DD05 — Recovery: per-tick probability gamma=0.10.
DD06 — Permanent immunity: R → R forever. No waning.
DD07 — Parameters: FROZEN in frozen/sir_rules.md.
DD08 — I(t) is always an INTEGER. Never a float.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI.
- All randomness via seeded numpy.random.Generator.
- Same seed = identical output.
- Structured logging.

================================================================================
FROZEN CODE
================================================================================

frozen/sir_rules.md — DO NOT MODIFY.
