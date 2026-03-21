# Schelling Segregation — Dead Ends Log

---

## DEAD END 1 — Sequential update order produces different dynamics

**What was attempted**: Builder implemented agent moves one-at-a-time (sequential),
which is the common ABM tutorial pattern.

**Result**: Sequential update produces higher segregation than simultaneous because
early movers change the landscape for later movers, creating cascading segregation.
Segregation index was 0.92 (sequential) vs 0.85 (simultaneous).

**Why this is a dead end**: The frozen spec (Schelling 1971) uses SIMULTANEOUS
updates. Sequential update is a different model with different dynamics. The result
cannot be compared to the theoretical predictions.

**Do NOT repeat**: Implementing sequential (one-agent-at-a-time) update order.

---

## DEAD END 2 — Textbook tolerance of 0.33 instead of 0.375

**What was attempted**: Builder used tolerance threshold 0.33 (one-third), which
is the most commonly cited value in ABM textbook implementations.

**Result**: The Critic flagged this as specification drift. The frozen spec says
0.375 (three-eighths). The difference produces measurably different segregation
dynamics (lower tolerance = less segregation = weaker effect).

**Why this is a dead end**: 0.33 is the LLM prior. 0.375 is the frozen spec.
This is exactly the Prior-as-Detector pattern: the model generated from what it
remembered, not from what the spec says.

**Do NOT repeat**: Using any tolerance value other than 0.375 unless explicitly
varied in an experiment condition.
