"""Bootstrap — CHP Statistics Sprint.  All constants from frozen spec."""
import sys, math, random, statistics
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_bootstrap_constants import *


def bootstrap_resample(data, rng=None):
    """Draw a resample WITH replacement, same size as the original data.

    Parameters
    ----------
    data : sequence
        Original sample.
    rng  : random.Random, optional
        Random number generator (for reproducibility).

    Returns
    -------
    list
        Bootstrap resample of len(data) drawn WITH replacement.
    """
    n = len(data)
    if rng is None:
        rng = random.Random()
    # random.choices draws WITH replacement — this is the critical step
    return rng.choices(data, k=n)


def bootstrap_stat(data, stat_fn, B, seed=42):
    """Compute a statistic on B bootstrap resamples.

    Parameters
    ----------
    data    : sequence — original sample
    stat_fn : callable — e.g. statistics.mean
    B       : int — number of bootstrap replicates
    seed    : int — RNG seed for reproducibility

    Returns
    -------
    list of float — B bootstrap statistics
    """
    rng = random.Random(seed)
    results = []
    for _ in range(B):
        resample = bootstrap_resample(data, rng=rng)
        results.append(stat_fn(resample))
    return results


def bootstrap_se(boot_stats):
    """Standard error = standard deviation of the bootstrap statistics."""
    return statistics.stdev(boot_stats)


def bootstrap_ci_percentile(boot_stats, alpha=0.05):
    """Percentile confidence interval from bootstrap statistics.

    Parameters
    ----------
    boot_stats : list of float — B bootstrap statistics
    alpha      : float — significance level (default 0.05 for 95 % CI)

    Returns
    -------
    (lower, upper) — percentile-based CI bounds
    """
    sorted_stats = sorted(boot_stats)
    B = len(sorted_stats)
    lo_idx = int(math.floor((alpha / 2) * B))
    hi_idx = int(math.floor((1 - alpha / 2) * B)) - 1
    # Clamp to valid range
    lo_idx = max(0, min(lo_idx, B - 1))
    hi_idx = max(0, min(hi_idx, B - 1))
    return (sorted_stats[lo_idx], sorted_stats[hi_idx])


def p_any_repeat(n):
    """Probability that a bootstrap resample of size n contains at least one
    repeated element.

    P(any repeat) = 1 − n! / n^n
    """
    return 1.0 - math.factorial(n) / (n ** n)


if __name__ == "__main__":
    print("Bootstrap — Resampling Demo\n")
    print(f"  Data          = {list(DATA)}")
    print(f"  n             = {N}")
    print(f"  Original mean = {ORIGINAL_MEAN}")
    print(f"  Sample var    = {SAMPLE_VAR}")
    print(f"  Theoretical SE= {THEORETICAL_SE}")
    print()

    B = 10_000
    boot = bootstrap_stat(DATA, statistics.mean, B)
    se = bootstrap_se(boot)
    lo, hi = bootstrap_ci_percentile(boot)
    print(f"  B             = {B}")
    print(f"  Bootstrap SE  = {se:.4f}  (theoretical ~ {THEORETICAL_SE})")
    print(f"  95% CI        = [{lo:.4f}, {hi:.4f}]")
    print()
    print(f"  P(any repeat), n=5 = {p_any_repeat(5):.4f}  (expected {P_ANY_REPEAT})")
    print(f"  Distinct bootstrap samples (n=5) = {N_DISTINCT_BOOTSTRAP}")
