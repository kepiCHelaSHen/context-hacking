# Schelling Segregation — Innovation Log

---

(The CHP loop will append entries here as it builds the simulation.
Each turn records: what was built, critic scores, anomaly results,
metric deltas, dead ends avoided, and what next turn should focus on.)

## Expected Build Sequence

Turn 1: Foundation — grid, agents, step function (Milestone 1)
Turn 2: Metrics — segregation index, cluster count (Milestone 2)
Turn 3: Dynamic tolerance extension (Milestone 3)
  → EXPECTED FALSE POSITIVE HERE: Builder generates textbook segregation
    (index ~0.85) instead of the dynamic-tolerance partial mixing (~0.5-0.7).
    The Critic should catch this as Prior-as-Detector drift.
Turn 4: Convergence battery — 30 seeds, sigma-gates (Milestone 4)
