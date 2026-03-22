"""Bonferroni Correction — CHP Statistics Sprint.  All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_bonferroni_constants import *


def bonferroni_threshold(alpha, m):
    """Bonferroni-adjusted significance level: α / m."""
    return alpha / m


def bonferroni_reject(p_values, alpha):
    """Apply Bonferroni correction and return list of bools (True = reject).

    Reject H_i when p_i < α / m, where m = len(p_values).
    """
    thresh = bonferroni_threshold(alpha, len(p_values))
    return [p < thresh for p in p_values]


def bh_reject(p_values, alpha):
    """Benjamini-Hochberg procedure — return list of bools (True = reject).

    1. Sort p-values (keeping original indices).
    2. Find largest k where p_(k) ≤ (k / m) · α.
    3. Reject all hypotheses with rank ≤ k.
    """
    m = len(p_values)
    indexed = sorted(enumerate(p_values), key=lambda x: x[1])

    # Find largest k satisfying p_(k) ≤ (k/m) · α  (1-indexed rank)
    largest_k = 0
    for rank_minus_1, (orig_idx, p) in enumerate(indexed):
        k = rank_minus_1 + 1                       # 1-indexed rank
        if p <= (k / m) * alpha:
            largest_k = k

    # Reject all hypotheses with rank ≤ largest_k
    rejected = [False] * m
    for rank_minus_1, (orig_idx, p) in enumerate(indexed):
        if rank_minus_1 + 1 <= largest_k:
            rejected[orig_idx] = True
    return rejected


def count_rejections(reject_list):
    """Count the number of True entries in a rejection list."""
    return sum(reject_list)


if __name__ == "__main__":
    print("Bonferroni Correction vs Benjamini-Hochberg — Demo\n")
    print(f"  m = {M} tests,  alpha = {ALPHA}")
    print(f"  p-values: {list(P_VALUES)}\n")

    thresh = bonferroni_threshold(ALPHA, M)
    bonf = bonferroni_reject(P_VALUES, ALPHA)
    bh = bh_reject(P_VALUES, ALPHA)

    print(f"  Bonferroni threshold : {thresh}")
    print(f"  Bonferroni rejections: {count_rejections(bonf)}  {bonf}")
    print(f"  BH rejections        : {count_rejections(bh)}  {bh}")
    print(f"\n  BH discovers {count_rejections(bh) - count_rejections(bonf)} "
          f"more true effects than Bonferroni")
