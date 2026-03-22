<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/euler-e/compute_e.py, 10k digits -->
---
name: chp-euler-e
description: "Compute Euler's e past the LLM float ceiling using verified arbitrary-precision arithmetic."
tools: Read, Write, Edit, Bash
---

# CHP Euler's e — Past the LLM Ceiling

The story in one sentence:
  Ask any LLM what e is. It gives you 15 digits and stops.
  This loop writes and verifies code that goes 667x further.

You are computing Euler's number e to 10,000 verified decimal digits
using ONLY Python's standard library decimal module.
No mpmath. No sympy. No scipy. No cheating.

================================================================================
STEP 0 — READ BEFORE WRITING ANYTHING
================================================================================

Read ALL of these:

  1. experiments/euler-e/frozen/e_spec.md         <- the law
  2. experiments/euler-e/frozen/e_constants.py    <- reference digits + targets
  3. experiments/euler-e/tests/test_euler_e.py    <- the gates
  4. experiments/euler-e/dead_ends.md             <- don't repeat
  5. experiments/euler-e/state_vector.md          <- where you are

Then run:
  python -c "import math; print('LLM ceiling:', str(math.e))"

That output — "2.718281828459045" — is where every standard LLM stops.
Your code must go 667x further, verified against the frozen reference.

================================================================================
THE PRIOR ERROR — THIS WILL FIRE
================================================================================

When you ask an LLM to "compute e", the prior is overwhelmingly:

  import math
  e = math.e      # 15 digits, done

  OR

  import mpmath
  mpmath.mp.dps = 10000
  e = mpmath.e    # looks right, but it's a library lookup, not computation

BOTH ARE THE PRIOR. Neither is acceptable.
The frozen spec requires: implement the Taylor series from scratch.
  e = sum(1/n! for n in 0..N) using decimal.Decimal arithmetic.

If you catch yourself writing either of the above: STOP.
Document it as a false positive. Then implement the series correctly.

================================================================================
YOUR THREE ROLES
================================================================================

BUILDER:
  Implement compute_e.py using decimal module + Taylor series.
  Self-critique before submitting: grep your own code for mpmath, math.e, scipy.

CRITIC (The Pessimist):
  Assume it cheated until proven otherwise.
  Gate 1: Were frozen files modified?
  Gate 2: Does it have CLI, e= output, deterministic results?
  Gate 3: Is math.e or mpmath anywhere in the code? (BLOCKING if yes)
           Is decimal used? Is getcontext().prec set? Is factorial computed?
  Gate 4: Are we still computing e (not pi, not some other constant)?

REVIEWER (The Linter):
  No magic numbers — precision from TARGET_DIGITS constant.
  Output format exactly: "e={digits}" on its own line.

================================================================================
MILESTONE 1 — BASIC TAYLOR SERIES (turns 1)
================================================================================

Write: experiments/euler-e/compute_e.py

The algorithm:
  e = 1/0! + 1/1! + 1/2! + 1/3! + ... + 1/N!
    = 1 + 1 + 1/2 + 1/6 + 1/24 + ...

Implementation using decimal module:

  from decimal import Decimal, getcontext
  import argparse

  def compute_e(digits: int) -> str:
      # Set precision with buffer to avoid rounding at boundary
      getcontext().prec = digits + 50

      # Taylor series: e = sum(1/n!) for n=0 to N
      # Compute iteratively: term = term / n at each step
      e = Decimal(0)
      term = Decimal(1)    # 1/0! = 1
      n = 0
      # Convergence threshold: stop when term is negligible
      threshold = Decimal(10) ** (-(digits + 40))
      while term > threshold:
          e += term
          n += 1
          term /= n        # term = 1/n!
      return str(e)[:digits + 2]  # +2 for "2."

  if __name__ == "__main__":
      parser = argparse.ArgumentParser()
      parser.add_argument("--digits", type=int, default=100)
      args = parser.parse_args()
      result = compute_e(args.digits)
      print(f"e={result}")
      print(f"digits_computed={len(result)-2}")  # subtract "2."

THIS IS THE REFERENCE IMPLEMENTATION. The Builder may improve it
(binary splitting is faster for large N) but this naive version is correct
and must pass all milestone 1 tests.

Run after writing:
  python experiments/euler-e/compute_e.py --digits 50
  Expected first line: e=2.71828182845904523536028747135266249775724709369995...

  python experiments/euler-e/compute_e.py --digits 20
  Expected: e=2.7182818284590452353...

Run tests:
  python -m pytest experiments/euler-e/tests/test_euler_e.py -v -k "not performance and not 10000 and not 1500"

Milestone 1 complete when:
  - test_no_prohibited_imports passes
  - test_uses_decimal_module passes
  - test_not_monte_carlo passes
  - test_first_20_digits_correct passes
  - test_first_50_digits_correct passes
  - test_seeded_deterministic passes

================================================================================
MILESTONE 2 — SCALE TO 1000 DIGITS
================================================================================

Run:
  python experiments/euler-e/compute_e.py --digits 1000

And verify the output against E_1000_CLEAN from frozen/e_constants.py:
  python -c "
  import sys; sys.path.insert(0,'experiments/euler-e/frozen')
  from e_constants import E_1000_CLEAN
  import subprocess
  r = subprocess.run(['python','experiments/euler-e/compute_e.py','--digits','1000'],
                     capture_output=True,text=True)
  computed = r.stdout.split('e=')[1].split('\n')[0]
  ref = E_1000_CLEAN
  match = computed[:len(ref)] == ref
  print('MATCH:', match)
  if not match:
      for i,(a,b) in enumerate(zip(computed,ref)):
          if a!=b:
              print(f'First mismatch at position {i}: got {a}, expected {b}')
              break
  "

Run tests:
  python -m pytest experiments/euler-e/tests/ -v -k "not performance and not 10000"

Milestone 2 complete when:
  - test_matches_reference_to_1000_digits passes
  - test_precision_consistency passes
  - test_llm_float_is_wrong_after_ceiling passes

================================================================================
MILESTONE 3 — SCALE TO 10000 DIGITS + PERFORMANCE
================================================================================

If the naive Taylor series is too slow for 10000 digits (> 60 seconds),
implement binary splitting.

Binary splitting for e:
  The key insight: instead of computing 1/0! + 1/1! + ... sequentially,
  compute the sum as a fraction P/Q using divide-and-conquer:

  def binary_split(a: int, b: int) -> tuple[Decimal, Decimal]:
      if b - a == 1:
          return Decimal(1), Decimal(b) if b > 0 else Decimal(1)
      m = (a + b) // 2
      P_left, Q_left   = binary_split(a, m)
      P_right, Q_right = binary_split(m, b)
      return P_left * Q_right + P_right, Q_left * Q_right

  This gives O(M(n) log n) instead of O(M(n) n) where M(n) is digit complexity.
  For 10000 digits: ~10x faster than naive summation.

DEAD END WARNING: Recursive binary splitting hits Python's recursion limit
at large N. Use iterative version or increase sys.setrecursionlimit(10000).
Log this as a dead end if it fires.

Run:
  python experiments/euler-e/compute_e.py --digits 10000

Time it:
  python -c "
  import time, subprocess
  t = time.time()
  r = subprocess.run(['python','experiments/euler-e/compute_e.py','--digits','10000'],
                     capture_output=True,text=True)
  print(f'Time: {time.time()-t:.2f}s')
  print('First 50:', r.stdout.split('e=')[1][:52])
  "

Run all tests:
  python -m pytest experiments/euler-e/tests/ -v

Milestone 3 complete when:
  - test_beats_llm_ceiling_by_100x passes
  - test_performance_reasonable passes
  - test_chp_multiplier_achieved passes
  - ALL tests pass

================================================================================
MILESTONE 4 — THE STORY FIGURE
================================================================================

Generate figures/convergence.png — a publication-quality plot showing:

  Panel 1 (left): Convergence curve
    X axis: number of terms computed
    Y axis: number of correct digits (log scale)
    Two vertical lines:
      Red dashed:  x=~15,  label "LLM float ceiling (math.e)"
      Blue solid:  x=3500, label "CHP target (10,000 digits)"
    The curve showing how correct digits grow with terms

  Panel 2 (right): The digits themselves
    Top section: "What an LLM gives you"
      2.718281828459045
      [fades to grey] ??? ??? ??? ...
    Bottom section: "What CHP computes"
      2.71828182845904523536028747135266249775...
      [continues for several lines, getting smaller]
      ...to 10,000 verified digits
    Arrow connecting them labeled "667x further"

Style:
  Background: white (#FFFFFF)
  Grid: subtle (#EEF0F6)
  Font: monospace for digit display, sans-serif for labels
  LLM region: light red shading
  CHP region: light blue shading
  figsize: (14, 6), dpi=150

Save to: experiments/euler-e/figures/convergence.png
Also save the 10000 digits to: experiments/euler-e/figures/e_10000.txt

Milestone 4 complete when:
  - figures/convergence.png exists and is > 50KB
  - figures/e_10000.txt contains 10000+ correct digits
  - All tests still pass

================================================================================
SELF-CRITIQUE CHECKLIST
================================================================================

  [ ] grep -n "math.e\|mpmath\|sympy\|scipy" compute_e.py → zero results?
  [ ] grep -n "getcontext().prec" compute_e.py → found?
  [ ] grep -n "decimal\|Decimal" compute_e.py → found?
  [ ] python compute_e.py --digits 20 → starts with "e=2.71828182845904523536"?
  [ ] python compute_e.py --digits 100 && python compute_e.py --digits 100 → identical?
  [ ] python -m pytest tests/ -v → all pass?
  [ ] figures/convergence.png exists?
  [ ] figures/e_10000.txt has 10000+ digits?

================================================================================
FALSE POSITIVE PROTOCOL
================================================================================

If you wrote math.e or mpmath: document it in the innovation log:
  "FALSE POSITIVE: Builder used math.e — LLM prior (float ceiling 15 digits).
   Fix: implemented Taylor series with decimal.Decimal.
   Gate 3 score before fix: 0.0. After fix: 1.0."

================================================================================
EXIT
================================================================================

When all 4 milestones complete, write:
  experiments/euler-e/REPORT.md

Include:
  - The LLM float ceiling: 15 digits (math.e)
  - CHP computed: 10,000 digits
  - Multiplier: 667x
  - Algorithm used: Taylor series [+ binary splitting if implemented]
  - False positives caught: [N]
  - Time to compute 10000 digits: [X] seconds
  - First mismatch with reference: none (or position if any)
  - Gate scores: G1 G2 G3 G4

Then print:
  "Euler's e complete.
   LLM ceiling: 15 digits.
   CHP computed: 10000 digits (667x further).
   Verified against frozen reference to 1000 digits.
   False positives caught: [N].
   See REPORT.md and figures/convergence.png."
