# Schelling Segregation Model — Frozen Specification
# Source: Schelling (1971) "Dynamic Models of Segregation", Journal of Mathematical Sociology
# Extended: CHP Dynamic-Tolerance variant (2025)
#
# THIS FILE IS FROZEN. No agent may modify it.
# All implementation must match these rules exactly.

================================================================================
ORIGINAL SCHELLING (1971) RULES
================================================================================

GRID: N x N toroidal grid (default N=50, so 2500 cells).
AGENTS: Two types (A and B), each occupying one cell. Some cells empty.
DENSITY: 0.90 (90% of cells occupied).
RATIO: 50/50 split between A and B agents.

NEIGHBORHOOD: Moore neighborhood (8 surrounding cells).

TOLERANCE THRESHOLD: 0.375
  An agent is SATISFIED if at least 37.5% of its neighbors (occupied cells
  only) are of the same type.
  An agent is DISSATISFIED if fewer than 37.5% of neighbors are same-type.

  NOTE: This is the SPECIFIC Schelling threshold. LLMs commonly generate
  0.3, 0.33, or 0.5 — all are WRONG for the original model. The frozen
  value is 0.375. Any deviation is specification drift.

UPDATE RULE (each step):
  1. Identify all dissatisfied agents.
  2. Each dissatisfied agent moves to a random empty cell.
  3. Movement is SIMULTANEOUS within a step (all moves computed from the
     same pre-move state, then applied together).

  NOTE: Many ABM tutorials implement SEQUENTIAL (one agent at a time)
  updates. The original Schelling uses SIMULTANEOUS. This affects dynamics.

CONVERGENCE: The model runs until no agent is dissatisfied, or until
  a maximum number of steps (default 500).

METRICS:
  - Segregation index (Moran's I or mean same-type neighbor fraction)
  - Number of steps to convergence
  - Number of dissatisfied agents per step
  - Cluster count (connected components of same type)

================================================================================
CHP DYNAMIC-TOLERANCE EXTENSION (2025)
================================================================================

MODIFICATION: Agents update their tolerance based on local experience.

TOLERANCE UPDATE RULE (applied after each move step):
  For each agent:
    current_same_fraction = (same-type neighbors) / (total occupied neighbors)
    if current_same_fraction > tolerance + 0.1:
      # Agent is in a very homogeneous area — tolerance increases (becomes
      # more open to diversity because they feel "safe")
      tolerance += 0.005
    elif current_same_fraction < tolerance - 0.1:
      # Agent is in a very diverse area — tolerance decreases (becomes
      # more tribal because they feel "threatened")
      tolerance -= 0.005
    tolerance = clamp(tolerance, 0.1, 0.9)

  KEY PARAMETERS (frozen):
    tolerance_update_rate: 0.005
    tolerance_comfort_margin: 0.1
    tolerance_min: 0.1
    tolerance_max: 0.9
    initial_tolerance: 0.375 (matches original Schelling)

PREDICTION:
  The dynamic-tolerance model produces PARTIAL MIXING at equilibrium
  (segregation index ~0.5-0.7) rather than the near-complete segregation
  (index ~0.8-0.95) of the original model. This is because agents in
  homogeneous clusters gradually increase their tolerance, eventually
  accepting more diverse neighborhoods.

  LLMs that generate from priors will produce near-complete segregation
  (the textbook result). The Critic should flag this as specification drift
  if the dynamic-tolerance extension is enabled.

================================================================================
EXACT COEFFICIENTS (for drift detection)
================================================================================

These values MUST match the implementation exactly:

  GRID_SIZE: 50
  DENSITY: 0.90
  TYPE_RATIO: 0.50
  TOLERANCE_DEFAULT: 0.375
  TOLERANCE_UPDATE_RATE: 0.005
  TOLERANCE_COMFORT_MARGIN: 0.1
  TOLERANCE_MIN: 0.1
  TOLERANCE_MAX: 0.9
  NEIGHBORHOOD: "moore"  (8 cells)
  UPDATE_ORDER: "simultaneous"
  MAX_STEPS: 500
