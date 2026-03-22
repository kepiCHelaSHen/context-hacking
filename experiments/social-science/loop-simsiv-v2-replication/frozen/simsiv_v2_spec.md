# SIMSIV v2 Clan Simulator — Frozen Specification
# Builds ON TOP of v1 (v1 is frozen, immutable).
# Source: V2_INNOVATION_LOG.md (11 turns of autonomous build)
# Paper: Bowles (2006) vs North (1990) — between-group selection test
# THIS FILE IS FROZEN. No agent may modify it.

================================================================================
OVERVIEW
================================================================================

The v2 clan simulator extends v1 with inter-band mechanics: trade, raiding,
between-group selection, and per-band institutional differentiation. Multiple
bands (each a v1 Society) compete in the same simulation, enabling direct
comparison of FREE_COMPETITION vs STRONG_STATE governance regimes.

The definitive result: at 20 bands (10 Free + 10 State), institutions win
with p < 0.0001, Cohen's d = -5.97, 6/6 seeds. State bands maintain cooperation
~0.51 while Free bands decline to ~0.41. Free bands go nearly extinct (2-3/10).

================================================================================
ARCHITECTURE
================================================================================

Composition pattern: Band HAS-A Society (not inherits from).
Per-band rng: each band owns a seeded numpy.random.Generator.
No circular imports: models/clan/ imports nothing from engines/.
ClanEngine shares stateless v1 engine singletons across all bands.
Per-band Config: each band uses band.society.config for intra-band dynamics.

================================================================================
V2 FILES (7,663 lines total)
================================================================================

  models/clan/band.py           — Band wraps Society, trust mechanics
  models/clan/clan_config.py    — ClanConfig dataclass (raid/trade params)
  models/clan/clan_society.py   — Band registry, distance matrix, scheduling
  models/clan/clan_simulation.py — ClanSimulation wrapper, CSV export
  engines/clan_base.py          — ClanEngine: 5-step tick (bands, schedule,
                                   interact, selection, metrics)
  engines/clan_trade.py         — Positive-sum trade (Wiessner 1982)
  engines/clan_raiding.py       — Bowles raiding (coalition defense)
  engines/clan_selection.py     — Fst, selection coefficients, fission,
                                   extinction, migration
  metrics/clan_collectors.py    — 100+ per-tick clan metrics

================================================================================
KEY MECHANISMS
================================================================================

TRADE: Positive-sum exchange (5-15% surplus). outgroup_tolerance gates
  willingness. Scarcity lowers refusal threshold.

RAIDING: Bowles (2006) coalition defense. group_loyalty drives coalition
  size. cooperation_propensity provides cohesion bonus. 5-factor
  multiplicative trigger: base * scarcity * aggression * xenophobia * trust_deficit.

BETWEEN-GROUP SELECTION:
  - Fst decomposition (Wright 1951)
  - demographic_selection_coeff: Pearson r(trait, Malthusian growth rate)
  - raid_selection_coeff: Pearson r(trait, raid win rate)
  - Band fission at Dunbar threshold (150)
  - Band extinction at minimum viable (10)
  - Migration as gene flow (opposes selection)

INSTITUTIONAL DIFFERENTIATION:
  - Each band has its own Config (law_strength, property_rights)
  - FREE_COMPETITION: law_strength=0.0
  - STRONG_STATE: law_strength=0.8
  - Fission daughters inherit parent Config

================================================================================
KNOWN DEAD ENDS (from actual v2 build)
================================================================================

  1. n <= 4 bands: between-group selection undetectable (noise dominates)
  2. 0.6/0.4 blended fitness proxy: not comparable to Bowles (2006)
  3. Migration routing: all migrants to ONE destination (must be per-agent)
  4. fighter.die("raid", 0): must pass actual year
  5. law_strength read from society instead of society.config
  6. Default trust 0.5 too high: use 0.3 (Bowles 2009)
  7. n=3 seeds: false positive rate >50% (Ioannidis 2005)
  8. Exp 2 interaction effect +0.039 at n=3: FALSE POSITIVE (killed at n=10)

================================================================================
THE DEFINITIVE RESULT
================================================================================

  20 bands (10 Free + 10 State), 200yr, 6 seeds.
  State cooperation: 0.51
  Free cooperation: 0.41
  Divergence: -0.098 +/- 0.016
  t(5) = -14.62, p < 0.0001, d = -5.97
  State > Free in 6/6 seeds.
  Free bands: 2-3 survivors out of 10.
  State bands: 17-22 (proliferate via fission).

  INTERPRETATION: Institutions co-opt between-group selection.
  North (1990) wins over Bowles/Gintis (2006) at adequate scale.
