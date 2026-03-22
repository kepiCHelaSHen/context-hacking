# Spatial Prisoner's Dilemma — Dead Ends Log

---

## DEAD END 1 — Asynchronous update order

**What was attempted**: Builder implemented cell updates one at a time (asynchronous
random sweep), which is the default in NetLogo and Mesa ABM frameworks.

**Result**: Asynchronous update produces cascading effects where early-updated cells
influence the payoffs of later-updated cells within the same generation. This
reduces cooperation rate by ~15% compared to synchronous and breaks the deterministic
spatial patterns that are the key finding of Nowak & May (1992).

**Why this is a dead end**: The frozen spec requires SYNCHRONOUS DETERMINISTIC update.
Compute the entire new grid from the old grid, then swap. No cell sees another cell's
update within the same generation.

**Do NOT repeat**: Any update scheme that modifies the grid during payoff computation
or imitation within a single generation.

---

## DEAD END 2 — Standard T/R/P/S payoff matrix

**What was attempted**: Builder generated the full 4-parameter Prisoner's Dilemma
payoff matrix (T=5, R=3, P=1, S=0 or similar) instead of the simplified Nowak & May
single-parameter version.

**Result**: The Critic flagged this as specification drift. Nowak & May (1992) use
a simplified payoff where only parameter b matters: DC=b, CC=1, CD=DD=0. The
4-parameter version has different dynamics at the same effective temptation level.

**Why this is a dead end**: The single-parameter b is what makes the Nowak & May
model elegant and its results interpretable. Introducing 4 parameters adds degrees
of freedom that obscure the spatial structure effect.

**Do NOT repeat**: Using T/R/P/S parameterization. Use only parameter b.

---

## DEAD END 3 — Excluding self from neighborhood

**What was attempted**: Builder implemented Moore neighborhood with 8 cells only,
excluding self from payoff computation and imitation.

**Result**: Without self-inclusion, a lone cooperator surrounded by 8 cooperators
gets payoff 8 (correct), but a lone defector surrounded by 8 cooperators gets
payoff 8b. With self-inclusion, the cooperator gets payoff 9 and the defector
gets 8b. The threshold for defector invasion changes: without self, any b>1
invades; with self, invasion requires b > 9/8 = 1.125.

**Why this is a dead end**: Nowak & May (1992) explicitly include self in the
neighborhood (size 9, not 8). This is stated in the paper and affects the
critical b values for all phase transitions.

**Do NOT repeat**: Neighborhood size 8. Must be 9 (self + 8 Moore neighbors).
