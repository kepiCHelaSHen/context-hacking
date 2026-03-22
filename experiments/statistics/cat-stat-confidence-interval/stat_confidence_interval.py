"""Confidence Intervals — CHP Statistics Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_confidence_interval_constants import *


def standard_error(sigma, n):
    """SE = σ / √n."""
    return sigma / math.sqrt(n)


def ci_bounds(xbar, z, se):
    """Return (lower, upper) bounds of a confidence interval."""
    return (xbar - z * se, xbar + z * se)


def ci_width(z, se):
    """Width of CI = 2 · z · SE."""
    return 2 * z * se


def margin_of_error(z, se):
    """Margin of error = z · SE."""
    return z * se


if __name__ == "__main__":
    print("Confidence Intervals -- frequentist interpretation\n")
    se = standard_error(SIGMA, N)
    print(f"  n={N}, xbar={XBAR}, sigma={SIGMA}, SE={se}")
    lo95, hi95 = ci_bounds(XBAR, Z_95, se)
    lo99, hi99 = ci_bounds(XBAR, Z_99, se)
    print(f"  95% CI: ({lo95:.3f}, {hi95:.3f})  width={ci_width(Z_95, se):.3f}")
    print(f"  99% CI: ({lo99:.3f}, {hi99:.3f})  width={ci_width(Z_99, se):.3f}")
    print(f"\n  99% CI is WIDER than 95% CI -> higher confidence, less precision")
    print(f"  CI width scales with 1/sqrt(n), not n")
