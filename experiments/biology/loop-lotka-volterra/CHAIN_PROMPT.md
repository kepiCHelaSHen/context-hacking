# Agent-Based Lotka-Volterra — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Agent-Based Lotka-Volterra (CHP Showcase)
Purpose:    Demonstrate Prior-as-Detector catching ODE contamination in an
            agent-based predator-prey model.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Individual agents: each prey/predator is a discrete object with energy.
DD02 — Spatial: 50x50 toroidal grid, 4-connected random movement.
DD03 — Encounter: predator eats prey in same cell only. One prey per predator per tick.
DD04 — Reproduction: asexual fission at energy threshold. Energy split equally.
DD05 — Death: predators starve at energy <= 0. Prey die only from predation.
DD06 — Parameters: FROZEN in frozen/lotka_volterra_rules.md.
DD07 — NO ODE variables (alpha, beta, gamma, delta). This is agent-based.

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

frozen/lotka_volterra_rules.md — DO NOT MODIFY.
