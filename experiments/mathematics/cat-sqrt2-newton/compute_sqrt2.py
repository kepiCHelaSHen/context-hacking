"""
CHP Math Sprint — Experiment 3: sqrt(2) via Newton's Method (Babylonian)
Algorithm: x_{n+1} = (x_n + 2/x_n) / 2
Quadratic convergence: doubles correct digits each iteration.
Standard library only: decimal module for arbitrary precision.
"""

import argparse
import time
from decimal import Decimal, getcontext


def compute_sqrt2(digits: int, verbose: bool = False) -> tuple:
    """Compute sqrt(2) to `digits` decimal digits using Newton's method.

    Returns (result_string, iteration_count, iteration_log).
    """
    getcontext().prec = digits + 50
    two = Decimal(2)
    x = Decimal("1.5")  # initial guess
    prev = Decimal(0)
    iterations = 0
    log_lines = []

    while x != prev:
        prev = x
        x = (x + two / x) / 2
        iterations += 1
        if verbose:
            # Estimate correct digits by counting matching chars
            x_str = str(x)
            p_str = str(prev)
            match = 0
            for a, b in zip(x_str, p_str):
                if a == b:
                    match += 1
                else:
                    break
            log_lines.append(f"Iteration {iterations:3d}: ~{match} matching digits")

    return str(x)[:digits + 2], iterations, log_lines


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compute sqrt(2) via Newton's method")
    parser.add_argument("--digits", type=int, default=100)
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    t0 = time.time()
    result, iterations, log_lines = compute_sqrt2(args.digits, verbose=True)
    elapsed = time.time() - t0

    print(f"result={result}")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=newton_raphson")
    print(f"iterations={iterations}")
    print(f"time_seconds={elapsed:.2f}")

    if args.verbose or True:
        print(f"\n--- Convergence log ---")
        for line in log_lines:
            print(line)
