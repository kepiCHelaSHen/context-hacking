---
name: chp-gates
description: "Invoke before any merge. Runs sigma-gated verification across multiple seeds."
---

## sigma-Gate Protocol

1. Read config.yaml for anomaly_checks definitions.
2. Run the simulation/test across N seeds (default 3).
3. For each seed, check ALL thresholds.
4. Compute std across seeds for each metric.
5. If std > sigma_threshold (default 0.15): flag STOCHASTIC_INSTABILITY.
6. If any seed fails any bound check: ANOMALY — do not merge.
7. Report: per-seed values, std, pass/fail per check.
