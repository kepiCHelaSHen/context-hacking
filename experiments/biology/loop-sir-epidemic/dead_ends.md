# Stochastic SIR Epidemic — Dead Ends Log

---

## DEAD END 1 — Deterministic SIR rate equations

**What was attempted**: Builder generated dS/dt = -beta*S*I/N, dI/dt = beta*S*I/N - gamma*I,
discretized as S(t+1) = S(t) - beta*S(t)*I(t)/N, etc.

**Result**: Smooth epidemic curve, fadeout rate = 0%, final size exactly matching
the analytical solution (1 - exp(-R0 * final_size)). No demographic stochasticity.

**Why this is a dead end**: The frozen spec requires INDIVIDUAL agents with
STOCHASTIC transitions. The rate equation is a mean-field approximation that
misses fadeout, which is the entire scientific point of the stochastic model.

**Do NOT repeat**: Any implementation where infection count I(t) is a float
or computed from a rate equation. I(t) must be an integer count of discrete agents.

---

## DEAD END 2 — Per-tick transmission rate instead of per-contact probability

**What was attempted**: Builder computed infection probability as
p_infect = beta * n_infected / N (the mass-action rate). This is the
deterministic approximation.

**Result**: At small N, this gives different results than the per-contact
complement method: p = 1 - (1-beta)^k. The mass-action rate underestimates
infection probability when an agent contacts multiple infected individuals.

**Why this is a dead end**: The frozen spec explicitly requires the COMPLEMENT
method: p_escape = (1 - BETA)^(number of I contacts), p_infect = 1 - p_escape.
The mass-action approximation is a different model with different fadeout
probabilities.

**Do NOT repeat**: Using beta * S * I / N or any mass-action rate formula.
Use the per-contact complement method only.

---

## DEAD END 3 — Variable contacts per tick (Poisson-distributed)

**What was attempted**: Builder drew the number of contacts from a Poisson
distribution with mean K=10, rather than using exactly K=10 contacts per tick.

**Result**: Poisson-distributed contacts add an extra source of stochasticity
that inflates fadeout rates and changes the effective R0. The model no longer
matches the frozen parameters.

**Why this is a dead end**: The frozen spec says CONTACTS_PER_TICK = 10 (fixed).
Not "mean 10." Each agent contacts exactly 10 others per tick. Stochasticity
comes from WHICH 10 agents are contacted and whether transmission occurs, not
from the number of contacts.

**Do NOT repeat**: Drawing contact count from any distribution. Use exactly K=10.
