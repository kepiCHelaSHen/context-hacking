"""
NAIVE pi computation — Machin's formula with Python Decimal.
Same O(n^2) problem as naive e — arctan series with Decimal division
at 100k precision is extremely slow.
"""

import argparse
import time
from decimal import Decimal, getcontext


def arctan_series_naive(x: int, digits: int) -> Decimal:
    """Compute arctan(1/x) using Taylor series with Decimal."""
    getcontext().prec = digits + 50
    x_sq = Decimal(x * x)
    power = Decimal(1) / Decimal(x)
    result = power
    threshold = Decimal(10) ** (-(digits + 40))
    k = 3
    sign = -1
    terms = 0
    while True:
        power /= x_sq
        term = power / k
        if term < threshold:
            break
        result += sign * term
        k += 2
        sign *= -1
        terms += 1
        if terms % 5000 == 0:
            print(f"  [naive pi arctan(1/{x})] {terms} terms...", flush=True)
    return result


def compute_pi_naive(digits: int) -> str:
    getcontext().prec = digits + 50
    pi = 4 * (4 * arctan_series_naive(5, digits) - arctan_series_naive(239, digits))
    return str(pi)[:digits + 2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"NAIVE Machin formula for pi — target: {args.digits} digits")
    print(f"WARNING: O(n^2) Decimal arithmetic. This will be slow at 100k.")
    t0 = time.time()
    result = compute_pi_naive(args.digits)
    elapsed = time.time() - t0

    print(f"pi={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=naive_machin_decimal")
    print(f"time_seconds={elapsed:.2f}")
