# Agent-Based Lotka-Volterra — Dead Ends Log

---

## DEAD END 1 — Discrete-time Lotka-Volterra difference equations

**What was attempted**: Builder generated the discrete-time equivalent of the
Lotka-Volterra ODEs: X(t+1) = X(t) + alpha*X(t) - beta*X(t)*Y(t), etc.

**Result**: Smooth sinusoidal population curves with zero extinction across all
seeds. This is the ODE prior, not the agent-based spec.

**Why this is a dead end**: The frozen spec requires individual agents with energy,
spatial position, and stochastic encounters. Difference equations produce the
mean-field approximation which misses demographic stochasticity — the entire point
of the agent-based model.

**Do NOT repeat**: Any implementation using population-level equations (difference
or differential). Every agent must be an individual object with energy state.

---

## DEAD END 2 — Global encounter (well-mixed)

**What was attempted**: Builder implemented predator-prey encounters as a
population-level probability (p_encounter = prey_density * predator_density)
without spatial structure.

**Result**: Well-mixed encounters produce different oscillation dynamics than
spatial encounters. The global model has faster predator-prey phase lags and
different extinction thresholds because predators can "see" all prey, not just
prey in their grid cell.

**Why this is a dead end**: The frozen spec requires spatial encounters: a predator
eats a prey only if they share the same grid cell. This creates local depletion
zones that affect oscillation dynamics.

**Do NOT repeat**: Any encounter mechanism that doesn't check spatial co-location.

---

## DEAD END 3 — Reporting "stable oscillations" from first 50 ticks only

**What was attempted**: Builder ran 50 ticks, observed oscillations, and reported
"stable oscillations confirmed."

**Result**: At 50 ticks, the system appears stable. By tick 200-400, demographic
stochasticity causes amplitude drift. By tick 500, predator extinction occurs in
10-25% of runs. The "stable oscillation" finding was a PREMATURE CONCLUSION.

**Why this is a dead end**: Short runs mask late-time extinction. The frozen spec
requires 500 ticks precisely to capture the extinction dynamics that the ODE
cannot predict. Any conclusion about stability from <200 ticks is unreliable.

**Do NOT repeat**: Drawing stability conclusions from runs shorter than 500 ticks.
