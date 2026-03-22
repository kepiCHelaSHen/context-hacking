"""Poisson Distribution — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_poisson_constants import *


def poisson_pmf(lam, k):
    """P(X=k) = (λ^k * e^(-λ)) / k!"""
    return (lam ** k * math.exp(-lam)) / math.factorial(k)


def poisson_cdf(lam, k):
    """P(X≤k) = sum of P(X=i) for i = 0..k."""
    return sum(poisson_pmf(lam, i) for i in range(k + 1))


def poisson_mean(lam):
    """Mean of Poisson distribution = λ."""
    return lam


def poisson_var(lam):
    """Variance of Poisson distribution = λ (same as mean!)."""
    return lam


def is_overdispersed(mean, variance, threshold=1.5):
    """Return True if variance/mean exceeds threshold → Poisson invalid."""
    if mean == 0:
        return variance > 0
    return (variance / mean) > threshold


if __name__ == "__main__":
    print(f"lam = {LAMBDA}")
    for k in range(6):
        print(f"  P(X={k}) = {poisson_pmf(LAMBDA, k):.12f}")
    print(f"  P(X<=2)  = {poisson_cdf(LAMBDA, 2):.12f}")
    print(f"  Mean     = {poisson_mean(LAMBDA)}")
    print(f"  Variance = {poisson_var(LAMBDA)}")
    print(f"  Overdispersed (mean=3, var=9)? {is_overdispersed(3.0, 9.0)}")
