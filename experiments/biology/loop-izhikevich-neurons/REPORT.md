# Izhikevich Neurons — CHP Experiment Report

## Summary
Izhikevich (2003) spiking neuron with 2 variables (v, u), 4 parameters (a,b,c,d),
two-half-step Euler at dt=0.5ms. All 5 firing patterns reproduced.
HH contamination check: PASS (no m,h,n,gNa,gK,gL).

## False Positive Story
**Caught:** Verified the model has ONLY 2 state variables (v, u). No Hodgkin-Huxley
gating variables (m, h, n) or conductance parameters (gNa, gK, gL) present.
The v equation uses exact coefficients 0.04, 5, 140. Two half-steps at dt=0.5.

## Key Results — 5 Firing Patterns
| Pattern | Spikes (1s) | ISI CV | Expected CV | Status |
|---------|-------------|--------|-------------|--------|
| RS (Regular Spiking) | 39 | 0.120 | < 0.15 | PASS |
| IB (Intrinsically Bursting) | 54 | 0.165 | > 0.15 | PASS |
| CH (Chattering) | 88 | 0.993 | high (bursting) | PASS |
| FS (Fast Spiking) | 129 | 0.253 | any (fast) | PASS |
| LTS (Low-Threshold) | 87 | 0.324 | any | PASS |

- FS > RS spike count: PASS (129 > 39)
- RS ISI CV < 0.15: PASS (regular spiking confirmed)
- All patterns produce spikes at I=10: PASS

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 0.95 |
| Scientific validity | 0.92 |
| Drift check | 0.95 |
