"""
OMEGA Sentinel — sqrt(2) to 1,000,000 digits via Integer Newton.

Newton's method with pure integer arithmetic:
  x represents sqrt(2) * 10^N (a large integer)
  x_{n+1} = (x + 2 * 10^(2N) / x) / 2

Quadratic convergence: ~20 iterations for 1M digits (2^20 > 10^6).
Each iteration is one integer division of ~N-digit numbers.

Python's int uses GMP with sub-quadratic algorithms,
making this dramatically faster than Decimal at 1M scale.

Standard library only. No mpmath.
"""

import argparse
import sys
import time
from decimal import Decimal, getcontext

sys.set_int_max_str_digits(0)


def compute_sqrt2(digits: int) -> str:
    """Compute sqrt(2) to `digits` decimal digits using integer Newton."""
    precision = digits + 100
    scale = 10 ** precision
    two_scaled = 2 * scale * scale  # 2 * 10^(2*precision)

    # Initial guess: 1.5 * 10^precision
    x = 15 * (10 ** (precision - 1))

    iterations = 0
    prev = 0
    while x != prev:
        prev = x
        x = (x + two_scaled // x) // 2
        iterations += 1
        print(f"  Newton iteration {iterations}", flush=True)

    # Convert to string
    s = str(x)
    result = s[0] + "." + s[1:digits + 1]
    return result, iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=1000000)
    args = parser.parse_args()

    print(f"OMEGA SENTINEL: sqrt(2) to {args.digits:,} digits (integer Newton)")
    t0 = time.time()
    result, iterations = compute_sqrt2(args.digits)
    total = time.time() - t0

    with open("experiments/omega_sentinel_1M/figures/sqrt2_1M.txt", "w") as f:
        f.write(result)

    print(f"sqrt2={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=integer_newton")
    print(f"iterations={iterations}")
    print(f"time_seconds={total:.2f}")
    print(f"chars_written={len(result)}")
