"""Central Limit Theorem — CHP Statistics Sprint.  All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_clt_constants import *


def sampling_se(sigma, n):
    """Standard error of the mean: SE = σ / √n.

    The sampling distribution of x̄ has standard deviation σ/√n,
    NOT σ.  This shrinks with increasing sample size.
    """
    return sigma / math.sqrt(n)


def clt_applies(has_finite_mean, has_finite_variance):
    """Check whether CLT (Lindeberg-Lévy) applies.

    BOTH conditions must hold:
      1. Finite mean  (μ exists)
      2. Finite variance  (σ² exists)

    Returns False for Cauchy (no finite mean, no finite variance).
    """
    return bool(has_finite_mean and has_finite_variance)


def uniform_mean(a, b):
    """Mean of Uniform(a, b): μ = (a + b) / 2."""
    return (a + b) / 2.0


def uniform_variance(a, b):
    """Variance of Uniform(a, b): σ² = (b − a)² / 12."""
    return (b - a) ** 2 / 12.0


def sampling_distribution_params(mu, sigma, n):
    """Parameters of the CLT sampling distribution of x̄.

    Returns (mean, standard_error) = (μ, σ/√n).
    """
    return (mu, sigma / math.sqrt(n))


if __name__ == "__main__":
    print("Central Limit Theorem -- Sampling Distribution Demo\n")
    print(f"  Population: Uniform(0, 1)")
    print(f"  mu    = {MU_UNIFORM}")
    print(f"  var   = {VAR_UNIFORM:.10f}  (1/12)")
    print(f"  sigma = {SIGMA_UNIFORM:.10f}")
    print()
    for n in (30, 100):
        se = sampling_se(SIGMA_UNIFORM, n)
        print(f"  n = {n:>3d}:  SE = sigma/sqrt(n) = {se:.10f}")
    print()
    print(f"  Cauchy: finite mean = {CAUCHY_HAS_MEAN}, "
          f"finite variance = {CAUCHY_HAS_VARIANCE}")
    print(f"  CLT applies to Cauchy? {clt_applies(CAUCHY_HAS_MEAN, CAUCHY_HAS_VARIANCE)}")
