# SIMSIV v2 Replication — CHP Experiment Specification

## Research Question

Can the CHP protocol reproduce the North vs Bowles/Gintis result (p<0.0001)
from a frozen specification, catching the same false positive (n=3 interaction
effect) and arriving at the same conclusion (institutions win at scale)?

## What to Build (on top of v1)

1. `models/clan/band.py` — Band wrapping Society (composition)
2. `models/clan/clan_config.py` — ClanConfig (trade/raid parameters)
3. `models/clan/clan_society.py` — Band registry + interaction scheduling
4. `models/clan/clan_simulation.py` — Experiment wrapper + CSV export
5. `engines/clan_base.py` — ClanEngine: per-band ticks + inter-band dispatch
6. `engines/clan_trade.py` — Positive-sum trade engine
7. `engines/clan_raiding.py` — Bowles raiding with coalition defense
8. `engines/clan_selection.py` — Fst, selection coefficients, fission, extinction
9. `metrics/clan_collectors.py` — Inter-band metrics

## Milestones

1. FOUNDATION — Band, ClanSociety, ClanEngine scaffold
2. TRADE — Inter-band trade with trust and outgroup_tolerance
3. RAIDING — Bowles coalition defense, scarcity-driven raids
4. SELECTION — Fst, selection coefficients, fission, extinction, migration
5. METRICS — ClanMetricsCollector with 100+ metrics
6. SIMULATION WRAPPER — ClanSimulation with per-band Config
7. 4-BAND EXPERIMENT — 2 Free + 2 State, 200yr, 3 seeds (PILOT)
   → EXPECTED FALSE POSITIVE HERE: n=3 may show interaction effect
8. N=10 REPLICATION — Replicate any positive finding at n=10
   → If it dies: log dead end, move to n=20
9. 20-BAND EXPERIMENT — 10 Free + 10 State, the definitive test
10. CONVERGENCE — 6 seeds, sigma-gates, report

## Sigma-Gates

  inter_band_violence_rate in [0.02, 0.15]
  trade_volume_per_band in [0.10, 0.40]
  cooperation > 0.25
  aggression < 0.70
  population > 0
  std across seeds < 0.15

## Expected False Positive

At Milestone 7, the Builder runs n=3 seeds and may find an interaction effect
(raiding x institutions) of +0.03 to +0.05. This appears to support Bowles.

THE CRITIC MUST SAY: "Replicate at n=10."

At n=10, the effect will vanish (p > 0.90). This is the known false positive
from the original SIMSIV build (Dead End 7 in the frozen spec).

The loop must then scale to 20 bands (Milestone 9) where the real result
emerges: North wins, p < 0.0001.

## Why This Experiment Matters

This is CHP's proof of REPRODUCIBILITY. The original SIMSIV v2 was built in
11 turns over one session. This replication uses the formalized CHP protocol
with pre-loaded dead ends. If it arrives at the same result faster and
cleaner, the protocol is validated at production scale.

The false positive catch (n=3 → n=10 kill) is the centerpiece demo. It proves
the protocol's self-correction capability on a REAL scientific question, not
a textbook exercise.
