# Spatial Prisoner's Dilemma — Chain Prompt

================================================================================
PROJECT IDENTITY
================================================================================

Name:       Spatial PD (CHP Showcase)
Purpose:    Nowak & May (1992) spatial PD with b-sweep.
            Demonstrate Prior-as-Detector on update order and payoff matrix drift.

================================================================================
CONFIRMED DESIGN DECISIONS
================================================================================

DD01 — Grid: 100x100 toroidal. (Nowak & May 1992)
DD02 — Payoff: simplified single-parameter b. CC=1, CD=0, DC=b, DD=0.
DD03 — b default: 1.8 (Figure 2 of Nowak & May 1992).
DD04 — Neighborhood: Moore + SELF = 9 cells. (NOT 8.)
DD05 — Update: SYNCHRONOUS DETERMINISTIC imitation. Copy highest-payoff neighbor.
DD06 — Initial condition: single defector at grid center.
DD07 — Ties: keep current strategy.

================================================================================
ARCHITECTURE RULES
================================================================================

- Pure library: NO print(), NO UI in spatial_pd.py.
- All randomness via seeded numpy.random.Generator (for random initial conditions).
- Deterministic imitation = no randomness in update rule itself.
- Structured logging via logging.getLogger(__name__).

================================================================================
FROZEN CODE
================================================================================

frozen/spatial_pd_rules.md — DO NOT MODIFY.
