# Agent-Based Lotka-Volterra — Innovation Log

---

## Expected Build Sequence

Turn 1: Foundation — agents, grid, movement, eating, reproduction (Milestone 1)
  → Watch for: ODE variables (alpha/beta), population-level equations (Dead End 1)
Turn 2: Metrics — counts, extinction detection, oscillation period (Milestone 2)
  → Watch for: smooth trajectories (ODE contamination)
Turn 3: Extinction experiment — rate vs population size (Milestone 3)
  → EXPECTED FALSE POSITIVE: 0% extinction = ODE dynamics, not agent-based
  → Watch for: premature "stable" conclusion from <200 ticks (Dead End 3)
Turn 4: Convergence battery — 30 seeds (Milestone 4)
