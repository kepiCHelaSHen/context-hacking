# Spatial Prisoner's Dilemma — CHP Experiment Report

## Summary
Nowak & May (1992) spatial PD built in 3 turns. Synchronous deterministic
imitation on 100x100 toroidal grid with b=1.8. Cooperation survives at 0.41
with spatial structure (would go extinct in well-mixed). 30-seed battery:
mean=0.410, std=0.017, sigma-gate PASS.

## False Positive Story
**Caught:** The single_defector_center initial condition produces IDENTICAL
results across all seeds (coop=0.558) because the update rule is DETERMINISTIC
— no randomness in imitation, only in random initial conditions. This is
correct behavior (not a bug) but reveals that single-defector experiments are
seed-independent. The 30-seed battery must use random_half initial conditions
to test stochastic variation.

## Key Results

### b-Sweep (cooperation vs temptation)
| b | Cooperation Rate | Interpretation |
|---|-----------------|----------------|
| 1.0 | 0.986 | Near-universal cooperation (low temptation) |
| 1.4 | 0.902 | Cooperation dominates |
| 1.8 | 0.389 | Coexistence (the Nowak & May regime) |
| 2.0 | 0.000 | Defection dominates |
| 2.5 | 0.000 | Complete defection |

### 30-Seed Convergence Battery (b=1.8, random initial)
- Mean cooperation: **0.410**
- Std: **0.017** (sigma-gate PASS, < 0.15)
- Range: [0.2, 0.8] — PASS

### CHP Layers Demonstrated
- **Layer 1 (Prior-as-Detector):** b=1.8 and neighborhood=9 verified against frozen spec
- **Layer 3 (Frozen Code):** Simplified payoff (NOT T/R/P/S), synchronous update
- **Layer 6 (sigma-Gates):** 30 seeds, std=0.017 < 0.15 threshold

## Final Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.95 |
| Scientific validity | 0.92 |
| Drift check | 0.95 |
