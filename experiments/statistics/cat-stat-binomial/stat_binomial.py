"""Binomial Distribution — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_binomial_constants import *


def binom_coeff(n, k):
    """C(n, k) — number of ways to choose k from n."""
    return math.comb(n, k)


def binom_pmf(n, k, p):
    """P(X = k) for X ~ Binomial(n, p).  Exact computation."""
    return math.comb(n, k) * p**k * (1 - p)**(n - k)


def binom_mean(n, p):
    """E[X] = n * p."""
    return n * p


def binom_var(n, p):
    """Var(X) = n * p * (1 - p)."""
    return n * p * (1 - p)


def normal_approx_valid(n, p):
    """Return True iff the normal approximation to Binomial(n, p) is valid.

    Rule of thumb: np >= 5  AND  n(1-p) >= 5.
    """
    return n * p >= 5 and n * (1 - p) >= 5


if __name__ == "__main__":
    print(f"Scenario 1: n={N1}, p={P1}, k={K1}")
    print(f"  P(X={K1}) = {binom_pmf(N1, K1, P1):.15f}")
    print(f"  Normal approx valid? {normal_approx_valid(N1, P1)}")
    print(f"Scenario 2: n={N2}, p={P2}")
    print(f"  P(X=0) = {binom_pmf(N2, 0, P2):.15f}")
    print(f"  P(X=1) = {binom_pmf(N2, 1, P2):.15f}")
    print(f"  Normal approx valid? {normal_approx_valid(N2, P2)}")
