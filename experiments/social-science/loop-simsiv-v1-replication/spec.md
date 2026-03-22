# SIMSIV v1 Replication — CHP Experiment Specification

## Research Question

Can the CHP protocol reproduce a calibrated 35-trait agent-based model of human
social evolution from a frozen specification, hitting all 9 anthropological
calibration targets?

## Scale

This is the largest CHP experiment by an order of magnitude:
  - 9 simulation engines (Environment, Resources, Conflict, Mating,
    Reproduction, Mortality, Pathology, Institutions, Reputation)
  - 35 heritable traits with h²-weighted inheritance
  - ~257 tunable configuration parameters
  - ~130 metrics per tick
  - Target: ~8,000-10,000 lines of code

## What to Build

1. `models/agent.py` — Agent dataclass with 35 traits + non-heritable state
2. `models/society.py` — Population container with event system
3. `models/environment.py` — Seasonal cycles, scarcity shocks
4. `config.py` — ~257 parameters with defaults
5. `simulation.py` — Annual tick orchestrator (12 steps)
6. `engines/resources.py` — 8-phase resource distribution
7. `engines/conflict.py` — Violence, coalitions, deterrence
8. `engines/mating.py` — Female choice, male competition, pair bonds
9. `engines/reproduction.py` — h²-weighted inheritance, birth
10. `engines/mortality.py` — Aging, health decay, disease
11. `engines/institutions.py` — Norm enforcement, institutional drift
12. `engines/reputation.py` — Gossip, trust, beliefs, skills
13. `engines/pathology.py` — Conditions, trauma, epigenetics
14. `metrics/collectors.py` — ~130 metrics per tick
15. `autosim/` — Calibration engine (simulated annealing against 9 targets)

## Milestones

1. AGENT MODEL — 35 traits, life stages, non-heritable state
2. SOCIETY + ENVIRONMENT — Population container, events, seasons
3. RESOURCES — 8-phase distribution with cooperation sharing
4. CONFLICT — Violence, coalitions, cross-sex dynamics
5. MATING — Female choice, male competition, pair bonding
6. REPRODUCTION — h²-weighted inheritance, mutation
7. MORTALITY — Aging, health decay, childhood mortality
8. INSTITUTIONS — Norm enforcement, property rights, drift
9. REPUTATION — Gossip, trust decay, beliefs, skills
10. PATHOLOGY — Conditions, trauma, epigenetics
11. MIGRATION — Emigration/immigration
12. METRICS — ~130 metrics per tick
13. INTEGRATION — Full 12-step tick, smoke tests
14. CALIBRATION — AutoSIM: simulated annealing against 9 targets
15. VALIDATION — 10 seeds x 200yr, held-out score >= 0.90
16. EXPERIMENTS — 11 scenarios (FREE_COMPETITION through EMERGENT_INSTITUTIONS)

## Sigma-Gates

  population > 200 (no collapse)
  cooperation_selection > 0 (cooperation selected for)
  aggression_selection < 0 (aggression selected against)
  mean_cooperation > 0.3
  mean_aggression < 0.6
  std across 10 seeds < 0.15 for all primary metrics
  calibration_score >= 0.85
  zero collapses across 10 validation seeds

## Expected False Positives

1. **Trait inheritance**: Builder generates simple average instead of h²-weighted
   midparent with mutation. Critic checks: are h² values from the frozen spec
   used in the inheritance formula?

2. **Resource distribution**: Builder generates single-phase allocation instead
   of the frozen 8-phase pipeline. Critic checks: are cooperation sharing,
   tool bonuses, and taxation all present?

3. **Conflict engine**: Builder generates simple random fights instead of the
   full coalition + deterrence + third-party punishment system. Critic checks:
   does aggression have 5 fitness cost channels?

4. **Institutional drift**: Builder generates fixed institutions instead of
   emergent drift. Critic checks: does law_strength self-organize from 0
   in EMERGENT_INSTITUTIONS scenario?

## Why This Experiment Matters

This is the CHP protocol's ultimate test. If it can build a 10,000-line
calibrated scientific simulation from a frozen spec — hitting 9 anthropological
benchmarks with score >= 0.85 — the protocol is proven at production scale.

The original SIMSIV took 27 deep-dive sessions over ~2 weeks. With CHP's
dead-end avoidance and structured verification, the replication should be
faster and produce cleaner code.
