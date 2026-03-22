"""
OMEGA Sentinel — pi to 1,000,000 digits via Chudnovsky + Binary Splitting.

The Chudnovsky formula (1988):
  1/pi = 12 * sum_{k=0}^{inf} (-1)^k * (6k)! * (13591409 + 545140134*k)
                                / ((3k)! * (k!)^3 * 640320^(3k+3/2))

Each term gives ~14.18 digits. For 1M digits: ~70,530 terms.
Binary splitting keeps everything in integer arithmetic until the
final division + square root.

This is the same algorithm used by y-cruncher and other world-record
pi computation programs.

Standard library only. No mpmath.
"""

import argparse
import math
import sys
import time

sys.set_int_max_str_digits(0)

C = 640320
C3_OVER_24 = C ** 3 // 24  # 10939058860032000


def binary_split_chudnovsky(a: int, b: int) -> tuple:
    """Binary splitting for Chudnovsky series.
    Returns (P_ab, Q_ab, T_ab).
    """
    if b - a == 1:
        if a == 0:
            p_ab = 1
            q_ab = 1
        else:
            p_ab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
            q_ab = a ** 3 * C3_OVER_24
        t_ab = p_ab * (13591409 + 545140134 * a)
        if a & 1:
            t_ab = -t_ab
        return (p_ab, q_ab, t_ab)

    m = (a + b) // 2
    p_am, q_am, t_am = binary_split_chudnovsky(a, m)
    p_mb, q_mb, t_mb = binary_split_chudnovsky(m, b)

    p_ab = p_am * p_mb
    q_ab = q_am * q_mb
    t_ab = t_am * q_mb + p_am * t_mb
    return (p_ab, q_ab, t_ab)


def compute_pi(digits: int) -> str:
    """Compute pi to `digits` decimal digits using Chudnovsky + binary splitting."""
    n_terms = max(10, digits // 14 + 100)
    print(f"  Chudnovsky: {n_terms} terms...", flush=True)

    t0 = time.time()
    p, q, t = binary_split_chudnovsky(0, n_terms)
    split_time = time.time() - t0
    print(f"  Integer splitting done: {split_time:.1f}s", flush=True)

    # pi = (Q * 426880 * sqrt(10005)) / T
    # For sqrt(10005), we need arbitrary precision.
    # Compute sqrt(10005) via integer Newton: isqrt(10005 * 10^(2N))
    prec = digits + 100
    t0 = time.time()

    # Integer sqrt of 10005 * 10^(2*prec)
    print(f"  Computing isqrt(10005 * 10^{2*prec})...", flush=True)
    n = 10005 * (10 ** (2 * prec))
    # Python 3.8+ has math.isqrt for integer square root
    sqrt_10005_int = math.isqrt(n)
    sqrt_time = time.time() - t0
    print(f"  isqrt done: {sqrt_time:.1f}s", flush=True)

    # pi = Q * 426880 * sqrt_10005 / T (all as integers scaled by 10^prec)
    t0 = time.time()
    # numerator = Q * 426880 * sqrt_10005_int  (this is scaled by 10^prec)
    # denominator = T
    # pi * 10^prec = Q * 426880 * sqrt_10005_int / T
    numerator = q * 426880 * sqrt_10005_int
    pi_int = numerator // t  # t is negative for the series sum, handle sign
    if pi_int < 0:
        pi_int = -pi_int
    div_time = time.time() - t0
    print(f"  Final integer division done: {div_time:.1f}s", flush=True)

    s = str(pi_int)
    # pi = 3.14159... — find where the decimal point goes
    # pi_int represents pi * 10^prec, so first digit is '3'
    result = s[0] + "." + s[1:digits + 1]
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=1000000)
    args = parser.parse_args()

    print(f"OMEGA SENTINEL: pi to {args.digits:,} digits (Chudnovsky + binary splitting)")
    t0 = time.time()
    result = compute_pi(args.digits)
    total = time.time() - t0

    with open("experiments/omega_sentinel_1M/figures/pi_1M.txt", "w") as f:
        f.write(result)

    print(f"pi={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=chudnovsky_binary_splitting")
    print(f"time_seconds={total:.2f}")
    print(f"chars_written={len(result)}")
