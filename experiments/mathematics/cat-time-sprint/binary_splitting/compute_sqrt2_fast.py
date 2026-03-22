"""
FAST sqrt(2) computation - Newton's method with integer arithmetic.

Instead of using Decimal (which has Python overhead per operation),
we work with pure integers:
  Maintain x as a large integer representing sqrt(2) * 10^N.
  Newton step: x = (x + 2 * 10^(2N) / x) / 2

This avoids all Decimal overhead. Python's int has GMP-backed
fast multiplication, making each iteration much faster.

No external libraries. Standard library only.
"""

import argparse
import sys
import time
from decimal import Decimal, getcontext

# Python 3.11+ limits int->str conversion to 4300 digits by default
sys.set_int_max_str_digits(200000)


def compute_sqrt2_fast(digits: int) -> str:
    """Compute sqrt(2) to `digits` decimal digits using integer Newton's method."""
    # Work with integers: x represents sqrt(2) * 10^(digits+50)
    precision = digits + 50
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

    # Convert to string with decimal point
    s = str(x)
    result = s[0] + "." + s[1:digits + 1]
    return result, iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"INTEGER NEWTON for sqrt(2) - target: {args.digits} digits")
    t0 = time.time()
    result, iterations = compute_sqrt2_fast(args.digits)
    elapsed = time.time() - t0

    print(f"sqrt2={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=integer_newton")
    print(f"iterations={iterations}")
    print(f"time_seconds={elapsed:.2f}")
