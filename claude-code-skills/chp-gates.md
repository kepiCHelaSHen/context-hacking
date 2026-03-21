---
name: chp-gates
description: "Run sigma-gated verification: execute simulation across N seeds, check all thresholds from config.yaml. Use after code is written and tests pass."
tools: Read, Bash
---

## sigma-Gate Protocol

1. Read `config.yaml` for `gates.anomaly_checks` definitions.
2. Run the simulation across N seeds (read `gates.seeds` from config, default 3).
3. For EACH seed, check ALL thresholds.
4. Compute std across seeds for each metric.
5. Report results.

## Check criteria

For each anomaly_check in config.yaml:
  - Read the metric name, operator, and threshold
  - Evaluate: does the metric pass for ALL seeds?

Variance check:
  - For each metric, compute std across seeds
  - If std > sigma_threshold (default 0.15): flag STOCHASTIC_INSTABILITY

## Output format

```
SEED RESULTS:
  Seed 42:  [metric1]=X.XX (PASS/FAIL), [metric2]=X.XX (PASS/FAIL)
  Seed 137: [metric1]=X.XX (PASS/FAIL), [metric2]=X.XX (PASS/FAIL)
  Seed 271: [metric1]=X.XX (PASS/FAIL), [metric2]=X.XX (PASS/FAIL)

VARIANCE:
  [metric1] std=X.XXXX (PASS/FAIL, threshold=0.15)

RESULT: PASS / ANOMALY
```

If ANOMALY: log it and suggest fixes.
If STOCHASTIC_INSTABILITY: force one VALIDATION turn before continuing.
