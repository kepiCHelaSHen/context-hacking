# Euler's e — CHP Experiment Report

## Summary
Computed Euler's number e to 10,000 decimal digits using the Taylor series expansion e = sum(1/n!) with Python's `decimal` module for arbitrary precision. The computation runs in 0.11 seconds, exceeding the LLM digit-recall ceiling by a factor of 667x. All 17 tests pass with 0 false positives. Verified against OEIS A001113 frozen reference (1000-digit exact match).

## False Positive Story
No false positives were encountered. The Taylor series for e converges rapidly and was implemented correctly from the start. The frozen reference (OEIS A001113, 1000 digits) matched the computed output exactly, confirming both the algorithm and the reference data. This experiment serves as a clean baseline: the algorithm is straightforward, the convergence is fast, and there is no opportunity for prior contamination since LLMs cannot recall more than ~15 digits of e from training data.

## Key Results
| Metric | Value |
|--------|-------|
| Algorithm | Taylor series: e = sum(1/n!) |
| Digits computed | 10,000 |
| Computation time | 0.11s |
| LLM ceiling | ~15 digits |
| CHP multiplier | 667x |
| Precision buffer | digits + 50 (Decimal context) |
| Convergence threshold | 10^-(digits+40) |
| Tests | 17/17 pass |
| False positives | 0 |
| Reference | OEIS A001113 (1000 digits, exact match) |

## Gate Scores
| Gate | Score |
|------|-------|
| Frozen compliance | 1.00 |
| Architecture | 1.00 |
| Scientific validity | 1.00 |
| Drift check | 1.00 |
