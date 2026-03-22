<!-- STATUS: run | DATE: 2026-03-21 | OUTPUT: experiments/euler-e, pi-machin, sqrt2-newton -->
---
name: chp-math-sprint
description: "One-hour sprint: compute e, pi, sqrt(2) past the LLM float ceiling using verified arbitrary-precision arithmetic."
tools: Read, Write, Edit, Bash
---

# CHP Math Sprint — Forcing LLMs Past Their Own Ceiling

The core insight:
  Standard LLMs cap at 15-16 significant digits (float64 ceiling).
  CHP forces the LLM to write VERIFIED CODE that goes arbitrarily further.
  The frozen spec is mathematical truth. The sigma gates are proof checking.

This sprint runs 3 experiments in sequence:
  1. Euler's e      — Taylor series         — target: 10,000 digits
  2. Pi             — Machin formula        — target: 10,000 digits
  3. sqrt(2)        — Newton's method       — target: 10,000 digits

Total wall time target: under 60 minutes.
Each experiment: 2-3 turns max. Move fast. The protocol is tight.

================================================================================
BEFORE ANYTHING — VERIFY THE STARTING POINT
================================================================================

Run this first. This is the LLM float ceiling we are beating:

  python3 -c "
  import math
  print('=== LLM FLOAT CEILING ===')
  print(f'e      = {math.e}')
  print(f'pi     = {math.pi}')
  print(f'sqrt2  = {math.sqrt(2)}')
  print(f'digits = ~15-16 for all three')
  print('=== CHP TARGET: 10,000 digits each ===')
  "

Save that output. It is the starting line.

================================================================================
RULES FOR ALL THREE EXPERIMENTS
================================================================================

1. Standard library ONLY: decimal, math (not math.e/math.pi/math.sqrt),
   fractions, itertools. Nothing else.

2. Every computation uses decimal.Decimal with getcontext().prec set FIRST.

3. Output format for all three scripts:
     result={digits}
     digits_computed={N}
     algorithm={name}
     time_seconds={t}

4. CLI: python compute_X.py --digits N

5. All values verified against frozen reference before claiming milestone done.

6. FALSE POSITIVE PROTOCOL:
   If you catch yourself using math.e, math.pi, math.sqrt, mpmath, or **0.5:
   STOP. Document it. Implement the algorithm from scratch. Log it.

================================================================================
EXPERIMENT 1: EULER'S e
================================================================================

Read first:
  experiments/euler-e/frozen/e_constants.py
  experiments/euler-e/tests/test_euler_e.py

Write: experiments/euler-e/compute_e.py

Algorithm — Taylor series:
  e = sum(1/n!) for n = 0, 1, 2, ...
  = 1 + 1 + 1/2 + 1/6 + 1/24 + ...

  from decimal import Decimal, getcontext
  import argparse, time

  def compute_e(digits: int) -> str:
      getcontext().prec = digits + 50
      e = Decimal(0)
      term = Decimal(1)
      threshold = Decimal(10) ** (-(digits + 40))
      n = 1
      while term > threshold:
          e += term
          term /= n
          n += 1
      return str(e)

  if __name__ == "__main__":
      parser = argparse.ArgumentParser()
      parser.add_argument("--digits", type=int, default=100)
      args = parser.parse_args()
      t0 = time.time()
      result = compute_e(args.digits)
      elapsed = time.time() - t0
      print(f"result={result[:args.digits+2]}")
      print(f"digits_computed={args.digits}")
      print(f"algorithm=taylor_series")
      print(f"time_seconds={elapsed:.2f}")

Verify e:
  python3 -c "
  import sys; sys.path.insert(0,'experiments/euler-e/frozen')
  from e_constants import E_1000_CLEAN
  import subprocess
  r = subprocess.run(['python3','experiments/euler-e/compute_e.py','--digits','1000'],
                     capture_output=True,text=True)
  out = r.stdout
  val = [l for l in out.split('\n') if l.startswith('result=')][0][7:]
  match = val[:len(E_1000_CLEAN)] == E_1000_CLEAN
  print('1000-digit match:', match)
  if not match:
      for i,(a,b) in enumerate(zip(val,E_1000_CLEAN)):
          if a!=b: print(f'First mismatch at position {i}'); break
  "

Run tests:
  python3 -m pytest experiments/euler-e/tests/test_euler_e.py -v -x

Scale to 10,000:
  python3 experiments/euler-e/compute_e.py --digits 10000

Save the output digits to:
  experiments/euler-e/figures/e_10000.txt

Experiment 1 DONE when:
  - Tests pass (especially test_no_prohibited_imports, test_first_50_digits_correct)
  - 10,000 digits computed
  - Time logged

Log in experiments/euler-e/innovation_log.md:
  Turn 1 / VALIDATION
  Result: e computed to 10000 digits
  LLM ceiling: 15 digits. CHP: 10000 digits. Multiplier: 667x.
  False positives caught: [N]
  Time: [X]s
  Gate scores: G1=1.0 G2=[x] G3=[x] G4=1.0

================================================================================
EXPERIMENT 2: PI via MACHIN'S FORMULA
================================================================================

Read first:
  experiments/pi-machin/frozen/pi_constants.py

Write: experiments/pi-machin/compute_pi.py

Algorithm — Machin's formula (1706):
  pi/4 = 4 * arctan(1/5) - arctan(1/239)

  arctan(x) as series:
  arctan(x) = x - x^3/3 + x^5/5 - x^7/7 + ...
  For x = 1/5 or 1/239: converges very fast (small x)

  Implementation:
  def arctan_series(x: Decimal, digits: int) -> Decimal:
      """Compute arctan(1/x) where x is an integer, using series."""
      # arctan(1/x) = 1/x - 1/(3x^3) + 1/(5x^5) - ...
      getcontext().prec = digits + 10
      x2 = Decimal(x * x)     # x^2
      term = Decimal(1) / x   # first term = 1/x
      result = term
      threshold = Decimal(10) ** (-(digits + 5))
      k = 3
      sign = -1
      while abs(term) > threshold:
          term /= x2           # term = term / x^2
          result += sign * term / k
          k += 2
          sign *= -1
      return result

  def compute_pi(digits: int) -> str:
      getcontext().prec = digits + 50
      pi = 4 * (4 * arctan_series(5, digits) - arctan_series(239, digits))
      return str(pi)[:digits + 2]

  NOTE: arctan_series takes an INTEGER x and computes arctan(1/x).
  The formula uses x=5 and x=239.
  DO NOT use math.pi, mpmath.pi, or any pre-computed value.

Verify pi:
  python3 -c "
  import sys; sys.path.insert(0,'experiments/pi-machin/frozen')
  from pi_constants import PI_1000_CLEAN, DIGIT_CHECKPOINTS
  import subprocess
  r = subprocess.run(['python3','experiments/pi-machin/compute_pi.py','--digits','50'],
                     capture_output=True,text=True)
  val = [l for l in r.stdout.split('\n') if l.startswith('result=')][0][7:]
  expected = '3.' + DIGIT_CHECKPOINTS[50]
  match = val[:52] == expected[:52]
  print('50-digit match:', match)
  print('Got:     ', val[:52])
  print('Expected:', expected[:52])
  "

Run at scale:
  python3 experiments/pi-machin/compute_pi.py --digits 10000

PRIOR ERRORS TO WATCH FOR:
  - Using Leibniz series (1 - 1/3 + 1/5 - ...): too slow, will time out
  - Using math.pi: float only
  - Monte Carlo: completely wrong approach for this
  - Wrong Machin formula signs: pi/4 = 4*arctan(1/5) MINUS arctan(1/239)
    LLM prior: sometimes writes PLUS. That gives wrong answer.
    Gate 3 catches it immediately — first digits will be wrong.

Save digits to: experiments/pi-machin/figures/pi_10000.txt

Log in experiments/pi-machin/innovation_log.md

================================================================================
EXPERIMENT 3: SQRT(2) via NEWTON'S METHOD
================================================================================

Read first:
  experiments/sqrt2-newton/frozen/sqrt2_constants.py

Write: experiments/sqrt2-newton/compute_sqrt2.py

Algorithm — Newton's method (Babylonian method):
  To compute sqrt(2):
  Start with x_0 = 1.5 (initial guess)
  Iterate: x_{n+1} = (x_n + 2/x_n) / 2
  Each iteration DOUBLES the number of correct digits.
  For 10,000 digits: only ~14 iterations needed.

  Implementation:
  def compute_sqrt2(digits: int) -> str:
      getcontext().prec = digits + 50
      two = Decimal(2)
      x = Decimal("1.5")    # initial guess
      # iterate until precision reached
      prev = Decimal(0)
      while x != prev:
          prev = x
          x = (x + two / x) / 2
      return str(x)[:digits + 2]

  NOTE on convergence detection:
  When x == prev at current precision, we have converged.
  This works because Decimal arithmetic is exact at the set precision.
  The loop typically runs only 14-16 times for 10,000 digits.

PRIOR ERRORS TO WATCH FOR:
  - math.sqrt(2): float only
  - 2 ** 0.5: float only
  - Decimal(2).sqrt(): this is ALLOWED as a check but you must implement
    Newton's method explicitly — the frozen spec requires showing the algorithm
  - Using too few iterations: if converged too early, digits will be wrong
    Gate 3 catches this — first mismatch will appear early
  - Wrong initial guess: 1.0 causes slow convergence, 2.0 diverges,
    1.5 is the standard starting point
  - Decimal(2) ** Decimal("0.5"): this is the ** 0.5 prior in disguise

Verify sqrt2:
  python3 -c "
  import sys; sys.path.insert(0,'experiments/sqrt2-newton/frozen')
  from sqrt2_constants import SQRT2_1000_CLEAN, DIGIT_CHECKPOINTS
  import subprocess
  r = subprocess.run(['python3','experiments/sqrt2-newton/compute_sqrt2.py','--digits','50'],
                     capture_output=True,text=True)
  val = [l for l in r.stdout.split('\n') if l.startswith('result=')][0][7:]
  expected = '1.' + DIGIT_CHECKPOINTS[50]
  match = val[:52] == expected[:52]
  print('50-digit match:', match)
  print('Got:     ', val[:52])
  print('Expected:', expected[:52])
  "

Run at scale:
  python3 experiments/sqrt2-newton/compute_sqrt2.py --digits 10000

Log iterations count — should be ~14 for 10,000 digits.
This is the MOST dramatic demonstration: quadratic convergence.
Show the iteration-by-iteration digit count in the output:
  Iteration  1: ~2 digits
  Iteration  2: ~4 digits
  Iteration  4: ~8 digits
  Iteration  7: ~64 digits
  Iteration 14: ~16384 digits (more than enough)

Save digits to: experiments/sqrt2-newton/figures/sqrt2_10000.txt
Save iteration log to: experiments/sqrt2-newton/figures/convergence_log.txt

================================================================================
GENERATE THE MASTER FIGURE
================================================================================

After all three experiments complete, generate:
  experiments/figures/math_sprint_summary.png

Layout: 3-column figure, one per constant

Each column contains:
  Top: Constant name + algorithm name
  Middle: Convergence visualization
    - For e: bar showing 15 digits (red) vs 10000 digits (blue)
    - For pi: same bar comparison
    - For sqrt2: iteration count (14 iterations!) vs digit count achieved
  Bottom: First 50 digits displayed in monospace
          with the first 15 highlighted (LLM ceiling) and
          the rest in a different color (CHP territory)

Style:
  White background, clean grid
  Red = LLM float ceiling
  Blue = CHP computed
  Font: monospace for digits, sans-serif for labels
  figsize: (18, 8), dpi=150

Code:
  import matplotlib.pyplot as plt
  import matplotlib.patches as mpatches
  from pathlib import Path
  import sys

  sys.path.insert(0, 'experiments/euler-e/frozen')
  sys.path.insert(0, 'experiments/pi-machin/frozen')
  sys.path.insert(0, 'experiments/sqrt2-newton/frozen')
  from e_constants import E_1000_CLEAN, LLM_FLOAT_VALUE as E_LLM
  from pi_constants import PI_1000_CLEAN, LLM_FLOAT_VALUE as PI_LLM
  from sqrt2_constants import SQRT2_1000_CLEAN, LLM_FLOAT_VALUE as SQRT2_LLM

  # Load computed values
  e_10k    = Path('experiments/euler-e/figures/e_10000.txt').read_text().strip()
  pi_10k   = Path('experiments/pi-machin/figures/pi_10000.txt').read_text().strip()
  s2_10k   = Path('experiments/sqrt2-newton/figures/sqrt2_10000.txt').read_text().strip()

  fig, axes = plt.subplots(2, 3, figsize=(18, 8))
  fig.patch.set_facecolor('white')
  constants = [
      ('e', E_LLM, e_10k, 'Taylor series\n(10,000 digits)', '#1D4ED8'),
      ('pi', PI_LLM, pi_10k, "Machin's formula\n(10,000 digits)", '#065F46'),
      ('sqrt(2)', SQRT2_LLM, s2_10k, "Newton's method\n(~14 iterations)", '#991B1B'),
  ]

  for col, (name, llm_val, chp_val, algo, color) in enumerate(constants):
      # Row 0: bar comparison
      ax = axes[0, col]
      ax.barh(['LLM (float64)', 'CHP (decimal)'], [15, 10000],
              color=['#FCA5A5', color], height=0.4)
      ax.set_xlabel('Correct digits')
      ax.set_title(f'{name}  —  {algo}', fontsize=11, fontweight='bold', color=color)
      ax.axvline(x=15, color='#FCA5A5', linestyle='--', alpha=0.5)
      ax.set_xlim(0, 11000)
      ax.spines['top'].set_visible(False)
      ax.spines['right'].set_visible(False)
      ax.text(10000, 1, '667x', ha='right', va='center',
              fontsize=10, color=color, fontweight='bold')

      # Row 1: digit display
      ax2 = axes[1, col]
      ax2.axis('off')
      llm_part = llm_val        # 15-16 digits
      chp_part = chp_val[:52]   # first 50 digits from CHP

      ax2.text(0.05, 0.85, 'LLM gives you:', fontsize=9,
               color='#6B7280', transform=ax2.transAxes)
      ax2.text(0.05, 0.72, llm_val + '...', fontsize=9,
               color='#EF4444', fontfamily='monospace', transform=ax2.transAxes)
      ax2.text(0.05, 0.55, 'CHP computes:', fontsize=9,
               color='#6B7280', transform=ax2.transAxes)
      ax2.text(0.05, 0.42, chp_part[:26], fontsize=8,
               color=color, fontfamily='monospace', transform=ax2.transAxes)
      ax2.text(0.05, 0.30, chp_part[26:52] + '...', fontsize=8,
               color=color, fontfamily='monospace', transform=ax2.transAxes)
      ax2.text(0.05, 0.14, '...to 10,000 verified digits',
               fontsize=8, color='#9CA3AF', transform=ax2.transAxes)

  fig.suptitle('CHP Math Sprint — Forcing LLMs Past Their Float Ceiling',
               fontsize=14, fontweight='bold', y=1.02)

  Path('experiments/figures').mkdir(exist_ok=True)
  plt.tight_layout()
  plt.savefig('experiments/figures/math_sprint_summary.png',
              dpi=150, bbox_inches='tight', facecolor='white')
  print('Saved: experiments/figures/math_sprint_summary.png')

================================================================================
SUMMARY TABLE — WRITE THIS WHEN DONE
================================================================================

Write experiments/MATH_SPRINT_RESULTS.md:

  # CHP Math Sprint Results

  | Constant | LLM ceiling | CHP computed | Multiplier | Algorithm | Time | False positives |
  |---|---|---|---|---|---|---|
  | e        | 15 digits   | 10,000       | 667x       | Taylor series | Xs | N |
  | pi       | 15 digits   | 10,000       | 667x       | Machin formula | Xs | N |
  | sqrt(2)  | 16 digits   | 10,000       | 625x       | Newton (14 iter) | Xs | N |

  ## Key finding
  Three different mathematical constants. Three different algorithms.
  Same result: CHP-verified code consistently computes 600-700x further
  than the LLM's own float precision, with every digit verified against
  a published reference frozen in the spec.

  The false positives tell the real story:
  - e: Builder used math.e (LLM prior). Caught by test_no_prohibited_imports.
  - pi: Builder used [Leibniz/Monte Carlo/math.pi]. Caught by Gate 3.
  - sqrt(2): Builder used math.sqrt / ** 0.5. Caught by Gate 3.

  In every case: the LLM's instinct was to use a shortcut that caps at 15 digits.
  In every case: the frozen spec forced the correct algorithm.
  In every case: the sigma gate verified the result.

================================================================================
TIMING TARGETS
================================================================================

  Experiment 1 (e):       < 15 minutes total, < 30s to compute 10k digits
  Experiment 2 (pi):      < 15 minutes total, < 60s to compute 10k digits
  Experiment 3 (sqrt2):   < 10 minutes total, < 5s to compute 10k digits (Newton!)
  Summary figure:         < 5 minutes
  Total target:           < 45 minutes

If any experiment takes > 20 minutes: switch to Exploration mode,
log a dead end, simplify the approach.

================================================================================
ORDER OF OPERATIONS
================================================================================

1. Run the LLM ceiling check (python3 -c "import math...")
2. Write compute_e.py — run — verify — tests
3. Write compute_pi.py — run — verify
4. Write compute_sqrt2.py — run — verify
5. Generate summary figure
6. Write MATH_SPRINT_RESULTS.md

Do not skip steps. Do not move to the next experiment until the current
one verifies against the frozen reference.

================================================================================
DONE
================================================================================

Print when all three complete:

  "=== CHP MATH SPRINT COMPLETE ==="
  "e:      10,000 digits computed. 667x LLM ceiling."
  "pi:     10,000 digits computed. 667x LLM ceiling."
  "sqrt2:  10,000 digits computed. 625x LLM ceiling."
  "Total false positives caught: [N]"
  "Total time: [X] minutes"
  "See: experiments/figures/math_sprint_summary.png"
  "See: experiments/MATH_SPRINT_RESULTS.md"
