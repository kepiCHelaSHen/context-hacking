"""Effect Size — CHP Statistics Sprint.  All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_effect_size_constants import *


def pooled_sd(s1, n1, s2, n2):
    """Correct pooled standard deviation, weighted by degrees of freedom.

    SD_pooled = √( ((n₁−1)·s₁² + (n₂−1)·s₂²) / (n₁ + n₂ − 2) )

    This is NOT the same as √((s₁² + s₂²)/2) unless n₁ = n₂.
    """
    return math.sqrt(((n1 - 1) * s1**2 + (n2 - 1) * s2**2)
                     / (n1 + n2 - 2))


def cohens_d(m1, m2, sd_pooled):
    """Cohen's d = (M₁ − M₂) / SD_pooled.

    Positive when m1 > m2.
    """
    return (m1 - m2) / sd_pooled


def eta_squared(ss_between, ss_total):
    """Eta-squared: proportion of total variance explained by the grouping.

    η² = SS_between / SS_total
    """
    return ss_between / ss_total


def d_category(d):
    """Classify |d| into Cohen's conventional categories.

    |d| < 0.2  →  not reported (returns "negligible" here)
    |d| ≥ 0.2  →  "small"
    |d| ≥ 0.5  →  "medium"
    |d| ≥ 0.8  →  "large"
    """
    abs_d = abs(d)
    if abs_d >= 0.8:
        return "large"
    if abs_d >= 0.5:
        return "medium"
    if abs_d >= 0.2:
        return "small"
    return "negligible"


if __name__ == "__main__":
    print("Effect Size — Cohen's d Demo\n")
    print(f"  Group 1: M={M1}, SD={S1}, n={N1}")
    print(f"  Group 2: M={M2}, SD={S2}, n={N2}")
    sd = pooled_sd(S1, N1, S2, N2)
    d = cohens_d(M1, M2, sd)
    print(f"\n  SD_pooled (correct)  = {sd:.6f}")
    print(f"  Cohen's d (correct)  = {d:.6f}  [{d_category(d)}]")
    sd_wrong = math.sqrt((S1**2 + S2**2) / 2)
    d_wrong = cohens_d(M1, M2, sd_wrong)
    print(f"\n  SD_pooled (wrong)    = {sd_wrong:.6f}")
    print(f"  Cohen's d (wrong)    = {d_wrong:.6f}  [{d_category(d_wrong)}]")
    eta = eta_squared(SS_BETWEEN, SS_TOTAL)
    print(f"\n  η² = {SS_BETWEEN}/{SS_TOTAL} = {eta:.4f}")
