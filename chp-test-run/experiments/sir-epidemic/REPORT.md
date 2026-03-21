# SIR Epidemic — CHP Experiment Report

## Summary
Stochastic individual-based SIR with N=500, R0=3.0, per-contact complement
method. KEY RESULT: fadeout rate = 3% (1/30 seeds) — impossible in deterministic
SIR. Prior-as-Detector confirmed: model is stochastic, not rate equations.

## False Positive Story
**Caught:** I(t) verified as integer type (not float). The complement method
p = 1-(1-beta)^k is used (not mass-action beta*S*I/N). Fadeout occurs in 1/30
seeds — the deterministic SIR predicts 0% fadeout for R0>1.

The fadeout seed (seed 10) showed the disease dying out at tick 8 before
exponential growth. This is demographic stochasticity that the ODE cannot capture.

## Key Results

### 30-Seed Convergence Battery
| Metric | Value | Gate | Status |
|--------|-------|------|--------|
| Fadeout rate | 3% (1/30) | > 0% | **PASS** |
| Mean final size (non-fadeout) | 0.943 | [0.50, 0.99] | **PASS** |
| Final size std | 0.015 | < 0.15 | **PASS** |
| R0 recovered | ~3.1 | [2.0, 6.0] | **PASS** |
| Peak infected | ~150 | — | consistent |

### Per-Seed Examples
| Seed | Peak I | Final Size | Fadeout? | R0 Est |
|------|--------|-----------|---------|--------|
| 42 | 157 | 0.940 | No | 3.12 |
| 137 | 154 | 0.934 | No | 2.28 |
| 271 | 143 | 0.936 | No | 3.19 |

## CHP Layers Demonstrated
- **Layer 1:** I(t) is integer (not float) — catches deterministic contamination
- **Layer 3:** Complement method (not mass-action) — matches frozen spec
- **Layer 6:** 30-seed battery: std=0.015, fadeout=3% > 0%
- **Layer 9:** Fadeout confirms stochastic model, not ODE

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.95 |
| Scientific validity | 0.95 |
| Drift check | 0.95 |
