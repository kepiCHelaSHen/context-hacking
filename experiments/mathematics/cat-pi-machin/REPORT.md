# Pi (Machin's Formula) — CHP Experiment Report

## Summary
Computed pi to 10,000 decimal digits using Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239), with the arctan Taylor series and Python's `decimal` module. The computation runs in 0.36 seconds, exceeding the LLM digit-recall ceiling by 667x. Verified against OEIS A000796 frozen reference (1000-digit exact match). Zero false positives.

## False Positive Story
No false positives were encountered in the implementation, but three common prior errors were deliberately avoided during algorithm selection. Leibniz series (pi/4 = 1 - 1/3 + 1/5 - ...) converges far too slowly for 10,000 digits. Monte Carlo estimation is a fundamentally wrong approach (statistical, not exact). Using `math.pi` provides only 15-16 float digits. Machin's formula (1706) was selected as the correct prior: it converges quickly due to the small arguments (1/5 and 1/239) and is exact to arbitrary precision. The choice of algorithm is itself a prior-selection problem, and selecting Machin over Leibniz avoids a performance false positive where the code would be "correct" but impractically slow.

## Key Results
| Metric | Value |
|--------|-------|
| Algorithm | Machin's formula: pi/4 = 4*arctan(1/5) - arctan(1/239) |
| Digits computed | 10,000 |
| Computation time | 0.36s |
| LLM ceiling | ~15 digits |
| CHP multiplier | 667x |
| Precision buffer | digits + 50 (Decimal context) |
| Convergence threshold | 10^-(digits+40) |
| Priors avoided | Leibniz (slow), Monte Carlo (wrong), math.pi (float) |
| False positives | 0 |
| Reference | OEIS A000796 (1000 digits, exact match) |

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 1.00 |
| Scientific validity | 1.00 |
| Drift check | 1.00 |
