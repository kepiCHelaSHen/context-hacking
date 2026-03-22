"""
CHP Math Sprint — Experiment 2: Pi via Machin's Formula (1706)
Algorithm: pi/4 = 4*arctan(1/5) - arctan(1/239)
arctan(1/x) = 1/x - 1/(3x^3) + 1/(5x^5) - 1/(7x^7) + ...
Standard library only: decimal module for arbitrary precision.
"""

import argparse
import time
from decimal import Decimal, getcontext


def arctan_series(x: int, digits: int) -> Decimal:
    """Compute arctan(1/x) where x is a positive integer, using Taylor series.

    arctan(1/x) = 1/x - 1/(3*x^3) + 1/(5*x^5) - ...
    """
    getcontext().prec = digits + 50
    x_sq = Decimal(x * x)
    power = Decimal(1) / Decimal(x)  # (1/x)^1
    result = power
    threshold = Decimal(10) ** (-(digits + 40))
    k = 3
    sign = -1
    while True:
        power /= x_sq  # (1/x)^(2i+1) via dividing by x^2 each step
        term = power / k
        if term < threshold:
            break
        result += sign * term
        k += 2
        sign *= -1
    return result


def compute_pi(digits: int) -> str:
    """Compute pi to `digits` decimal digits using Machin's formula."""
    getcontext().prec = digits + 50
    # pi/4 = 4*arctan(1/5) - arctan(1/239)
    pi = 4 * (4 * arctan_series(5, digits) - arctan_series(239, digits))
    return str(pi)[:digits + 2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute pi via Machin's formula")
    parser.add_argument("--digits", type=int, default=100)
    args = parser.parse_args()

    t0 = time.time()
    result = compute_pi(args.digits)
    elapsed = time.time() - t0

    print(f"result={result}")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=machin_formula")
    print(f"time_seconds={elapsed:.2f}")
