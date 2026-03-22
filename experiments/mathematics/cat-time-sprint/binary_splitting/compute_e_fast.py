"""
FAST e computation — Binary Splitting with integer arithmetic.
e = sum(1/n!) computed as P/Q where P and Q are large integers.

Binary splitting computes e = P(0,N)/Q(0,N) where:
  P(a,b) and Q(a,b) are defined recursively on the interval [a,b).
  Q(a,b) = Q(a,m) * Q(m,b)  where m = (a+b)//2
  P(a,b) = P(a,m)*Q(m,b) + P(m,b)

This avoids all Decimal division until the final step,
making it O(n * log(n)^2) instead of O(n^2).

No external libraries. Standard library only.
"""

import argparse
import time
from decimal import Decimal, getcontext


def binary_split_e(a: int, b: int) -> tuple:
    """Binary splitting for e = sum(1/n!).
    Returns (P, Q) where the partial sum over [a, b) equals P/Q.

    Base case: for interval [a, a+1):
      term = 1/a! contributes: P=1, Q=a (for a>0), or P=1, Q=1 (for a=0)

    Actually, we compute:
      sum_{k=a}^{b-1} 1/k! = P(a,b) / Q(a,b)
    where Q(a,b) = product of k for k in [a..b-1] (with 0! = 1)
    """
    if b - a == 1:
        if a == 0:
            return (1, 1)  # 1/0! = 1
        else:
            return (1, a)  # 1/a! partial: numerator=1, factor=a
    m = (a + b) // 2
    p_left, q_left = binary_split_e(a, m)
    p_right, q_right = binary_split_e(m, b)
    return (p_left * q_right + p_right, q_left * q_right)


def compute_e_fast(digits: int) -> str:
    """Compute e to `digits` decimal digits using binary splitting."""
    # Need about digits * log(10)/log(digits) terms, but ~3.5*digits/log10(digits) works
    # For safety, use a generous estimate
    import math
    n_terms = max(100, int(digits * 3.5 / math.log10(max(digits, 10))) + 100)

    # Binary split to get P/Q as integers
    p, q = binary_split_e(0, n_terms)

    # Now compute P/Q to the required precision using Decimal
    getcontext().prec = digits + 50
    result = Decimal(p) / Decimal(q)
    return str(result)[:digits + 2]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--digits", type=int, default=100000)
    args = parser.parse_args()

    print(f"BINARY SPLITTING for e - target: {args.digits} digits")
    t0 = time.time()
    result = compute_e_fast(args.digits)
    elapsed = time.time() - t0

    print(f"e={result[:60]}...")
    print(f"digits_computed={args.digits}")
    print(f"algorithm=binary_splitting_taylor")
    print(f"time_seconds={elapsed:.2f}")
