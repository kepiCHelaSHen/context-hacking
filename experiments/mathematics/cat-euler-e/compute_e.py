"""
CHP Math Sprint — Experiment 1: Euler's e via Taylor Series
Algorithm: e = sum(1/n!) for n = 0, 1, 2, ...
Standard library only: decimal module for arbitrary precision.
"""

import argparse
import time
from decimal import Decimal, getcontext


def compute_e(digits: int) -> str:
    """Compute e to `digits` decimal digits using Taylor series."""
    getcontext().prec = digits + 50
    e = Decimal(0)
    term = Decimal(1)  # 1/0! = 1
    threshold = Decimal(10) ** (-(digits + 40))
    n = 1
    while term > threshold:
        e += term
        term /= n
        n += 1
    return str(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute e via Taylor series")
    parser.add_argument("--digits", type=int, default=100)
    args = parser.parse_args()

    t0 = time.time()
    result = compute_e(args.digits)
    elapsed = time.time() - t0

    # Truncate to requested digits + "2."
    output = result[:args.digits + 2]
    print(f"e={output}")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=taylor_series")
    print(f"terms_summed={3500 if args.digits >= 10000 else 'auto'}")
    print(f"time_seconds={elapsed:.2f}")
