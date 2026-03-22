"""
NAIVE e computation — Taylor series with Python Decimal.
This is the O(n^2) approach that works fine at 10k digits
but becomes painfully slow at 100k due to Decimal arithmetic overhead.

CHP expects this to be killed by the kill switch, demonstrating
dead-end detection and forcing algorithm upgrade to binary splitting.
"""

import argparse
import time
from decimal import Decimal, getcontext


def compute_e_naive(digits: int) -> str:
    """Compute e = sum(1/n!) using Decimal arithmetic.
    O(n^2) due to n multiplications of n-digit Decimal numbers.
    """
    getcontext().prec = digits + 50
    e = Decimal(0)
    term = Decimal(1)
    threshold = Decimal(10) ** (-(digits + 40))
    n = 1
    terms = 0
    while term > threshold:
        e += term
        term /= n
        n += 1
        terms += 1
        if terms % 5000 == 0:
            print(f"  [naive e] {terms} terms computed...", flush=True)
    return str(e)[:digits + 2], terms


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"NAIVE Taylor series for e — target: {args.digits} digits")
    print(f"WARNING: O(n^2) Decimal arithmetic. This will be slow at 100k.")
    t0 = time.time()
    result, terms = compute_e_naive(args.digits)
    elapsed = time.time() - t0

    print(f"e={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=naive_taylor_series")
    print(f"terms={terms}")
    print(f"time_seconds={elapsed:.2f}")
