"""Exponential Distribution — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_exponential_constants import *

def exp_pdf(lam, x):
    """f(x) = lam * e^(-lam*x) for x >= 0."""
    if x < 0:
        return 0.0
    return lam * math.exp(-lam * x)

def exp_cdf(lam, x):
    """F(x) = 1 - e^(-lam*x) for x >= 0."""
    if x < 0:
        return 0.0
    return 1.0 - math.exp(-lam * x)

def exp_survival(lam, x):
    """S(x) = P(X > x) = e^(-lam*x)."""
    if x < 0:
        return 1.0
    return math.exp(-lam * x)

def exp_mean(lam):
    """E[X] = 1/lam (NOT lam!)."""
    return 1.0 / lam

def exp_variance(lam):
    """Var(X) = 1/lam^2."""
    return 1.0 / lam**2

def memoryless_check(lam, s, t):
    """P(X > s+t | X > s) should equal P(X > t). Returns (conditional, marginal)."""
    conditional = exp_survival(lam, s + t) / exp_survival(lam, s)
    marginal = exp_survival(lam, t)
    return (conditional, marginal)

if __name__ == "__main__":
    print(f"lam={LAMBDA}, mean={exp_mean(LAMBDA)}, var={exp_variance(LAMBDA)}")
    print(f"P(X<=1) = {exp_cdf(LAMBDA, 1):.6f}")
    print(f"P(X<=2) = {exp_cdf(LAMBDA, 2):.6f}")
    print(f"P(X>3)  = {exp_survival(LAMBDA, 3):.6f}")
    cond, marg = memoryless_check(LAMBDA, MEMORYLESS_S, MEMORYLESS_T)
    print(f"Memoryless: P(X>5|X>2)={cond:.6f}, P(X>3)={marg:.6f}, match={abs(cond-marg)<1e-12}")
