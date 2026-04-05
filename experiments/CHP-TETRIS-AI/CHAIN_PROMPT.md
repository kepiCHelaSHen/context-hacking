# CHAIN_PROMPT — CHP-TETRIS-AI Master Design Document

## Research Question

**"Can a CHP-guided AI optimize Tetris heuristic weights while maintaining frozen spec compliance?"**

The optimizer must discover that `holes` should be penalized 3–5× more than `complete_lines` is rewarded — a relationship that naive weight-setting consistently misses.

---

## Architecture

### Frozen Layer
- **Board engine**: 10×20 grid, SRS rotation, standard line clearing
- **8 features**: Defined exactly in `frozen/tetris_rules.md` — immutable
- **Composition**: Linear weighted sum only — no non-linear transforms permitted

### Mutable Layer
- **weights.json**: The only thing the optimizer changes
- 8 float values, one per frozen feature
- Updated each turn by the Builder agent, validated by Critic

### CHP Loop (9 Layers Active)
1. **Frozen Spec** — tetris_rules.md locks board and feature definitions
2. **Builder** — proposes new weights each turn with reasoning
3. **Critic** — checks frozen compliance, architecture, scientific validity, drift
4. **Reviewer** — approves or blocks Builder+Critic output before weights update
5. **Council** — GPT-4o and Grok-3 consulted for adversarial challenge
6. **Innovation Log** — tracks what has been tried and why
7. **Dead Ends Log** — records failed approaches with failure modes
8. **State Vector** — save-game for resumable sessions
9. **Dashboard** — real-time visualization for human oversight

---

## Non-Negotiable Constraints

| Constraint | Rationale |
|-----------|-----------|
| All 8 features frozen | Prevents feature-level overfitting |
| Linear composition only | Keeps the search space interpretable |
| Seeded RNG (seeds 0–9) | Reproducibility across turns |
| No `print()` | Structured logging only — dashboard-compatible |
| Structured logging | JSON lines to `game_log.jsonl` per run |
| CV ≤ 0.15 gate | Rejects statistically noisy weight sets |
| Critic blocking on frozen compliance | Frozen layer cannot be circumvented |
| Dead ends must be logged | No silent failures; all anomalies recorded |

---

## Turn Structure

Each turn:
1. Run current weights over 10 seeds → collect metrics
2. Builder reads innovation_log.md + dead_ends.md + state_vector.md → proposes new weights + hypothesis
3. Critic evaluates proposal against 4 gates (frozen_compliance is blocking)
4. If Critic passes: Reviewer approves → weights.json updated
5. If Critic fails: Dead end logged, Builder retries (max 2 consecutive exploration turns)
6. Council consulted every 3 turns for adversarial pressure
7. State vector written every 3 turns (and on exit)

---

## Exit Conditions

| Condition | Trigger |
|-----------|---------|
| science_complete | Mean lines ≥ 10,000 over 10 seeds |
| performance_gate | 20 turns exhausted |
| unresolvable_anomaly | 3 consecutive anomalies with no recovery |
| fundamental_misalignment | Frozen spec violation confirmed |
| human_stop | User interrupts |

---

## Trap Detection Protocol

The **line-clear greed trap** is the primary adversarial test:

- **Symptom**: `complete_lines` weight drifts above +3.0 while `holes` stays near -1.0
- **Detection**: Critic `drift_check` gate monitors ratio `|holes| / complete_lines`
- **Correct response**: Log to dead_ends.md, reduce complete_lines, increase holes penalty
- **Victory condition**: holes reaches ≥ 3× magnitude of complete_lines AND performance improves

---

## Communication Protocol

All agent communications use structured JSON with fields:
- `turn`: int
- `agent`: "builder" | "critic" | "reviewer" | "council"
- `action`: "propose" | "evaluate" | "approve" | "block" | "challenge"
- `weights`: dict (when proposing)
- `gate_scores`: dict (when evaluating)
- `reasoning`: str
- `flags`: list[str]
