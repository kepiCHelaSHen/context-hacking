"""
OMEGA Sentinel — e to 1,000,000 digits via Binary Splitting.

e = sum_{k=0}^{N} 1/k!

Binary splitting computes this as a single fraction P/Q using integer
arithmetic, then does ONE final division at full precision.

The key insight: Python's integers use GMP-backed arithmetic, which has
sub-quadratic multiplication (Karatsuba/Toom-Cook/FFT). This makes
binary splitting O(n * log(n)^2 * log(log(n))) vs O(n^2) for naive Decimal.

Standard library only. No mpmath.
"""

import argparse
import math
import sys
import time
# No Decimal needed — pure integer arithmetic avoids O(n^2) Decimal conversion

sys.set_int_max_str_digits(0)  # Lift Python 3.11+ int->str limit


def binary_split_e(a: int, b: int) -> tuple:
    """Binary splitting for e = sum(1/k!).
    Returns (P, Q) such that sum_{k=a}^{b-1} 1/k! = P/Q.
    """
    if b - a == 1:
        if a == 0:
            return (1, 1)
        return (1, a)
    m = (a + b) // 2
    p_l, q_l = binary_split_e(a, m)
    p_r, q_r = binary_split_e(m, b)
    return (p_l * q_r + p_r, q_l * q_r)


def compute_e(digits: int) -> str:
    """Compute e to `digits` decimal digits."""
    # Estimate terms needed: n! > 10^digits when n ~ digits*ln(10)/ln(n)
    # Conservative: digits * 3.5 / log10(digits)
    n_terms = max(100, int(digits * 3.5 / math.log10(max(digits, 10))) + 200)
    print(f"  Binary splitting e: {n_terms} terms...", flush=True)

    t0 = time.time()
    p, q = binary_split_e(0, n_terms)
    split_time = time.time() - t0
    print(f"  Integer splitting done: {split_time:.1f}s", flush=True)

    # Final division as pure integer arithmetic (avoid Decimal O(n^2) conversion)
    t0 = time.time()
    # Compute p/q * 10^(digits+50) as integer, then format
    int_result = p * (10 ** (digits + 50)) // q
    div_time = time.time() - t0
    print(f"  Integer division done: {div_time:.1f}s", flush=True)

    s = str(int_result)
    # e = 2.71828... so first digit is '2', then '.'
    result = s[0] + "." + s[1:digits + 1]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=1000000)
    args = parser.parse_args()

    print(f"OMEGA SENTINEL: e to {args.digits:,} digits (binary splitting)")
    t0 = time.time()
    result = compute_e(args.digits)
    total = time.time() - t0

    # Write digits to file
    with open("experiments/omega_sentinel_1M/figures/e_1M.txt", "w") as f:
        f.write(result)

    print(f"e={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=binary_splitting_taylor")
    print(f"time_seconds={total:.2f}")
    print(f"chars_written={len(result)}")
