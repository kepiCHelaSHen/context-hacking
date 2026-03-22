# sqrt(2) (Newton's Method) — Innovation Log

---

## Turn 1 / VALIDATION
- Result: sqrt(2) computed to 10,000 digits via Newton's method (Babylonian)
- LLM ceiling: 16 digits. CHP: 10,000 digits. Multiplier: 625x.
- Algorithm: x_{n+1} = (x_n + 2/x_n) / 2, starting from x_0 = 1.5
- Iterations: 14 (quadratic convergence: each iteration doubles correct digits)
- Computation time: 0.04s for 10,000 digits
- FALSE POSITIVE CAUGHT: Frozen reference sqrt2_constants.py contained
  LLM-hallucinated digits after position 50. First 50 digits were correct
  (OEIS A002193), but digits 51-1000 were fabricated. Detected when
  Newton's method output failed to match frozen reference at position 52.
  Both Newton's method and Decimal.sqrt() agreed on the correct value.
  Fixed frozen reference with verified digits.
- This is a META-LEVEL false positive: CHP caught bad data in its own
  frozen spec. The algorithm is the real ground truth.
- Gate scores: G1=1.0* G2=1.0 G3=1.0 G4=1.0
  (*G1 originally failed due to corrupted frozen ref, fixed and re-verified)
