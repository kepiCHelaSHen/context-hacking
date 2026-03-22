# Grover's Algorithm — CHP Experiment Report

## Summary
State-vector Grover simulation with phase-flip oracle, diffusion operator,
and sinusoidal amplitude profile. Success probability 0.9995 at k_opt=25
for N=1024. Quadratic speedup verified. 30/30 random targets found.

## False Positive Story
**Caught:** Oracle verified as PHASE FLIP (amplitude *= -1), not boolean return.
Diffusion operator present (inversion about mean). Overshoot test confirms
sinusoidal profile: P drops from 0.9995 at k=25 to 0.635 at k=35 — this is
impossible in classical search (classical P only increases with more queries).

## Key Results
| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| P(success) at k=25 | 0.9995 | > 0.90 | PASS |
| 30-target battery | all P=0.9995 | all > 0.90 | PASS |
| Overshoot k=35 | P=0.635 | < P at k=25 | sinusoidal CONFIRMED |
| Phase flip | verified | *= -1 | PASS |
| Diffusion | verified | inversion about mean | PASS |
| k_opt = floor(pi/4 * sqrt(1024)) | 25 | = 25 | EXACT |

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.98 |
| Scientific validity | 0.98 |
| Drift check | 0.98 |
