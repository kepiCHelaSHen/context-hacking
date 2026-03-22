# Lorenz Attractor — CHP Experiment Report

## Summary
Lorenz (1963) system integrated with adaptive RK45 (scipy solve_ivp),
rtol=atol=1e-9. Attractor bounded, not fixed point, chaotic trajectory
confirmed at t=50. beta=8/3 exactly (not rounded).

## False Positive Story
**Caught:** Verified NO Euler integration (no `dt` variable, solve_ivp with
RK45 confirmed in source). IC=(1,1,1) per frozen spec, NOT (0,1,0) from
the original Lorenz paper. beta stored as 8.0/3.0 = 2.6666666666666665
(not truncated to 2.667).

## Key Results
- Attractor bounded: |x|<25, |y|<30, |z|<55 — PASS
- Not fixed point: std(x_tail) > 1.0 — PASS
- Lyapunov estimate: 0.35 (simplified method; Benettin algorithm recommended for 0.906)
- IC verified: (1.0, 1.0, 1.0)
- Integration method: solve_ivp RK45 confirmed in source

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.95 |
| Scientific validity | 0.88 |
| Drift check | 0.95 |
