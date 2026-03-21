---
name: chp-mode
description: "Check and manage the current CHP mode (Validation vs Exploration)."
---

## Mode Protocol

Read state_vector.md to determine current mode.

### VALIDATION mode
- Every claim needs a literature citation.
- Critic is a hard blocker — NEEDS_IMPROVEMENT = no commit.
- Council runs BEFORE build.
- Full multi-seed anomaly detection required.

### EXPLORATION mode
- State a falsifiable hypothesis instead of a citation.
- Critic is advisory — log issues but don't block.
- Reversion Protocol is ACTIVE:
  - If anomaly check fails: git checkout to last passing tag.
  - Do NOT patch broken exploration code. Revert and try differently.
- Max 3 consecutive Exploration turns. Then forced return to Validation.

### Switching
- No improvement for 5 turns → suggest Exploration.
- Exploration anomaly → execute Reversion Protocol.
- 3 Exploration turns with no improvement → EXIT 2.
