"""
NAIVE sqrt(2) computation — Newton's method with Python Decimal.
Newton's method has quadratic convergence so it only needs ~17 iterations
for 100k digits. But each iteration does a 100k-digit Decimal division
which is O(n^2) with Python's decimal module.

This one might actually complete (Newton only needs ~17 iterations),
but it will be much slower than the integer-arithmetic version.
"""

import argparse
import time
from decimal import Decimal, getcontext


def compute_sqrt2_naive(digits: int) -> tuple:
    getcontext().prec = digits + 50
    two = Decimal(2)
    x = Decimal("1.5")
    prev = Decimal(0)
    iterations = 0
    while x != prev:
        prev = x
        x = (x + two / x) / 2
        iterations += 1
        print(f"  [naive sqrt2] iteration {iterations}", flush=True)
    return str(x)[:digits + 2], iterations


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"NAIVE Newton's method for sqrt(2) — target: {args.digits} digits")
    t0 = time.time()
    result, iterations = compute_sqrt2_naive(args.digits)
    elapsed = time.time() - t0

    print(f"sqrt2={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=naive_newton_decimal")
    print(f"iterations={iterations}")
    print(f"time_seconds={elapsed:.2f}")
