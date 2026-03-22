"""
FAST pi computation - Chudnovsky formula with binary splitting.

The Chudnovsky formula:
  1/pi = 12 * sum_{k=0}^{inf} (-1)^k * (6k)! * (13591409 + 545140134*k)
                                / ((3k)! * (k!)^3 * 640320^(3k+3/2))

Each term gives ~14.18 digits, so 100k digits needs ~7050 terms.
Binary splitting makes this O(n * log(n)^2) with integer arithmetic.

No external libraries. Standard library only.
"""

import argparse
import math
import time
from decimal import Decimal, getcontext


# Chudnovsky constants
C = 640320
C3_OVER_24 = C ** 3 // 24  # 10939058860032000


def binary_split_chudnovsky(a: int, b: int) -> tuple:
    """Binary splitting for Chudnovsky series.
    Returns (P_ab, Q_ab, T_ab) where:
      P_ab = product of p(k) for k in [a, b)
      Q_ab = product of q(k) for k in [a, b)
      T_ab = the partial sum contribution
    """
    if b - a == 1:
        if a == 0:
            p_ab = 1
            q_ab = 1
        else:
            p_ab = (6 * a - 5) * (2 * a - 1) * (6 * a - 1)
            q_ab = a ** 3 * C3_OVER_24
        t_ab = p_ab * (13591409 + 545140134 * a)
        if a & 1:  # odd k: negative term
            t_ab = -t_ab
        return (p_ab, q_ab, t_ab)

    m = (a + b) // 2
    p_am, q_am, t_am = binary_split_chudnovsky(a, m)
    p_mb, q_mb, t_mb = binary_split_chudnovsky(m, b)

    p_ab = p_am * p_mb
    q_ab = q_am * q_mb
    t_ab = t_am * q_mb + p_am * t_mb
    return (p_ab, q_ab, t_ab)


def compute_pi_fast(digits: int) -> str:
    """Compute pi using Chudnovsky + binary splitting."""
    # Each term gives ~14.18 digits
    n_terms = max(10, digits // 14 + 100)

    p, q, t = binary_split_chudnovsky(0, n_terms)

    # pi = (Q * 426880 * sqrt(10005)) / T
    getcontext().prec = digits + 50

    q_dec = Decimal(q)
    t_dec = Decimal(t)
    sqrt_10005 = Decimal(10005).sqrt()
    pi = q_dec * 426880 * sqrt_10005 / t_dec

    return str(pi)[:digits + 2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"CHUDNOVSKY + BINARY SPLITTING for pi - target: {args.digits} digits")
    t0 = time.time()
    result = compute_pi_fast(args.digits)
    elapsed = time.time() - t0

    print(f"pi={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=chudnovsky_binary_splitting")
    print(f"time_seconds={elapsed:.2f}")
