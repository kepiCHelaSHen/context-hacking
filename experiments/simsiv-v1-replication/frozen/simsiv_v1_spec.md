# SIMSIV v1 Band Simulator — Frozen Specification
# Source: SIMSIV CHAIN_PROMPT.md (authoritative design document)
# Paper: BIORXIV/2026/711970 (submitted, under review at JASSS)
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

SIMSIV is a calibrated agent-based model of band-level human social evolution.
500 agents with 35 heritable traits compete for resources, mates, and status
across annual time steps. All social patterns EMERGE from rules — never hardwired.

Calibrated against 9 anthropological benchmarks from Hadza, !Kung, and Ache
ethnographic data. Best calibration score: 1.000 (Run 3, 816 experiments).
Held-out validation: 10 seeds x 200yr, mean score 0.934, zero collapses.

================================================================================
SCALE
================================================================================

  Population: 500 agents (default)
  Generations: 200 (default)
  Time step: annual (1 year per tick)
  Random seed: supported — same seed = identical results

================================================================================
AGENT MODEL — 35 HERITABLE TRAITS
================================================================================

All float [0.0, 1.0]. Inherited via h²-weighted midparent + mutation sigma=0.05.

PHYSICAL PERFORMANCE (6):
  physical_strength h²=0.60, endurance h²=0.50, physical_robustness h²=0.50,
  pain_tolerance h²=0.45, longevity_genes h²=0.25, disease_resistance h²=0.40

COGNITIVE (4):
  intelligence_proxy h²=0.65, emotional_intelligence h²=0.40,
  impulse_control h²=0.50, conscientiousness h²=0.49

TEMPORAL (1):
  future_orientation h²=0.40

PERSONALITY (4):
  risk_tolerance h²=0.48, novelty_seeking h²=0.40,
  anxiety_baseline h²=0.40, mental_health_baseline h²=0.40

SOCIAL ARCHITECTURE (9):
  aggression_propensity h²=0.44, cooperation_propensity h²=0.40,
  dominance_drive h²=0.50, group_loyalty h²=0.42,
  outgroup_tolerance h²=0.40, empathy_capacity h²=0.35,
  conformity_bias h²=0.35, status_drive h²=0.50,
  jealousy_sensitivity h²=0.45

REPRODUCTIVE BIOLOGY (5):
  fertility_base h²=0.50, sexual_maturation_rate h²=0.60,
  maternal_investment h²=0.35, paternal_investment_preference h²=0.45,
  attractiveness_base h²=0.50

PSYCHOPATHOLOGY SPECTRUM (6):
  psychopathy_tendency h²=0.50, mental_illness_risk h²=0.40,
  cardiovascular_risk h²=0.40, autoimmune_risk h²=0.30,
  metabolic_risk h²=0.35, degenerative_risk h²=0.30

================================================================================
NON-HERITABLE STATE (per agent)
================================================================================

  health, reputation, current_resources, current_tools, current_prestige_goods
  prestige_score, dominance_score
  Beliefs (5 dims): hierarchy_belief, cooperation_norm, violence_acceptability,
    tradition_adherence, kinship_obligation — float [-1, +1]
  Skills (4 domains): foraging_skill, combat_skill, social_skill, craft_skill — [0, 1]
  faction_id, neighborhood_ids, reputation_ledger
  trauma_score, epigenetic_stress_load, active_conditions
  life_stage: CHILDHOOD / YOUTH / PRIME / MATURE / ELDER

================================================================================
9 ENGINE TICK ORDER
================================================================================

Each annual tick runs these in order:

  1. Environment — seasonal cycles, scarcity shocks, epidemics
  2. Resources — 8-phase distribution: base, intelligence bonus, cooperation
     sharing, tool bonus, prestige, taxation, storage, Gini computation
  3. Conflict — violence, deterrence, coalitions, third-party punishment
  4. Mating — female choice, male competition, pair bonds, EPC, jealousy
  5. Reproduction — h²-weighted inheritance, birth, infant survival
  6. Mortality — aging, health decay, childhood mortality, disease
  7. Migration — emigration/immigration (if enabled)
  8. Pathology — conditions, trauma, epigenetic stress
  9. Institutions — norm enforcement, property rights, institutional drift

  Plus: Reputation (gossip, trust, beliefs, skills, factions),
        Faction detection, neighborhood refresh, metrics collection

================================================================================
ARCHITECTURE RULES
================================================================================

  - Pure library: NO UI, NO print(). All IO at edges.
  - Tick returns data: sim.tick() returns pure state dict.
  - Models know nothing about engines. No circular imports.
  - All randomness via numpy.random.Generator seeded from config.
  - Events are dicts: {type, year, agent_ids, description, outcome}
  - Bounded events: society._event_window holds last 500 (rolling).
  - Structured logging: logging.getLogger(__name__).

================================================================================
CALIBRATION TARGETS (9 benchmarks)
================================================================================

  1. Population stability: no collapse over 200yr (0/20 collapses)
  2. Cooperation selected for: positive selection coefficient
  3. Aggression selected against: negative selection coefficient
  4. Violence rate in ethnographic range (Hadza/!Kung)
  5. Fertility rate in ethnographic range
  6. Mortality rate matches life table data
  7. Resource Gini in observed range
  8. Mating system dynamics match scenario
  9. Institutional emergence from zero

  AutoSIM best score: 1.000 (all 9 targets hit)
  Held-out validation: mean 0.934 across 10 seeds

================================================================================
KEY EMERGENT FINDINGS (from v1)
================================================================================

  - Cooperation and intelligence reliably selected for
  - Aggression reliably selected against (5 fitness cost channels)
  - ENFORCED_MONOGAMY reduces violence 37%, unmated males 65%
  - STRONG_STATE reduces Gini 40%, violence 49%
  - Law strength self-organizes 0 → 0.83 in EMERGENT_INSTITUTIONS
  - Resource scarcity produces highest cooperation
  - Cooperation trait is a robust emergent attractor (max sensitivity r=0.20)

================================================================================
CONFIG — ~257 TUNABLE PARAMETERS
================================================================================

See config.py for the full list. Key groups:
  Scale, Agent init, Mating system, Reproduction, Resources,
  Conflict, Mortality, Institutions, Beliefs, Skills, Pathology,
  Migration, Factions, Proximity

All parameters have documented defaults with scientific justification.
