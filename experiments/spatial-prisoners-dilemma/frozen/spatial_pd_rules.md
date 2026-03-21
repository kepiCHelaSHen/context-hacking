# Spatial Prisoner's Dilemma — Frozen Specification
# Source: Nowak & May (1992) "Evolutionary games and spatial chaos", Nature 359:826-829
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
ORIGINAL NOWAK & MAY (1992) RULES
================================================================================

GRID: N x N toroidal lattice (default N=100, so 10,000 cells).
AGENTS: Every cell is occupied. Each cell plays C (cooperate) or D (defect).

PAYOFF MATRIX (simplified):
  C vs C → 1 (mutual cooperation)
  C vs D → 0 (sucker's payoff)
  D vs C → b (temptation to defect, b > 1)
  D vs D → 0 (mutual defection)

  NOTE: This is the simplified Nowak & May payoff, NOT the standard
  T/R/P/S parameterization. Many LLMs generate the full 4-parameter
  version. The frozen spec uses only parameter b.

  Default b = 1.8 (produces the classic "kaleidoscope" spatial patterns).

  NOTE: b = 1.8 is the SPECIFIC value from Figure 2 of Nowak & May (1992).
  LLMs commonly generate b = 1.5, 2.0, or the full T/R/P/S matrix.
  All are WRONG for this specification.

NEIGHBORHOOD: Moore neighborhood (8 surrounding cells) PLUS SELF.
  Total neighborhood size = 9 (self + 8 neighbors).

  NOTE: Including SELF in the neighborhood is critical. Nowak & May
  explicitly include self-interaction. Omitting it changes the dynamics
  significantly. This is a common source of drift.

PAYOFF COMPUTATION:
  Each cell plays against all 9 neighbors (including self).
  Total payoff = sum of payoffs from 9 games.
  Cooperators playing against k cooperators get payoff = k.
  Defectors playing against k cooperators get payoff = b * k.

UPDATE RULE: SYNCHRONOUS DETERMINISTIC IMITATION.
  1. Every cell computes its total payoff.
  2. Every cell looks at all 9 cells in its neighborhood (including self).
  3. Every cell copies the strategy of the neighbor with the HIGHEST payoff.
  4. Ties broken by keeping current strategy.
  5. ALL updates happen SIMULTANEOUSLY (synchronous).

  NOTE: This is DETERMINISTIC imitation, not stochastic (Fermi function).
  Many ABM frameworks default to stochastic imitation. The frozen spec
  is deterministic: copy the best neighbor. Period.

  NOTE: Updates are SYNCHRONOUS. The new grid is computed from the old
  grid entirely, then swapped in one step. Asynchronous update produces
  fundamentally different dynamics.

INITIAL CONDITION:
  All cooperators EXCEPT a single defector placed at the center of the grid.

  NOTE: Nowak & May use this specific initial condition to demonstrate
  how a single defector can invade a cooperative population and create
  spatial structure. Random initial conditions produce different dynamics.

METRICS:
  - cooperation_rate: fraction of cells playing C (each generation)
  - spatial_clustering: fraction of cooperator-cooperator neighbor pairs
  - pattern_stability: Hamming distance between consecutive generations
  - defector_cluster_count: connected components of defectors

GENERATIONS: Run for 200 generations (default).

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

  GRID_SIZE: 100
  b: 1.8
  NEIGHBORHOOD: "moore_plus_self"  (9 cells)
  UPDATE_RULE: "synchronous_deterministic_imitation"
  INITIAL_CONDITION: "single_defector_center"
  GENERATIONS: 200
  PAYOFF_CC: 1
  PAYOFF_CD: 0
  PAYOFF_DC: b  (= 1.8)
  PAYOFF_DD: 0
