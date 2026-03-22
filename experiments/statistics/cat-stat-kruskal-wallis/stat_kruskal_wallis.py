"""Kruskal-Wallis Test — CHP Statistics Sprint."""
import sys
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_kruskal_wallis_constants import *


def rank_all(groups):
    """Assign combined ranks across all groups, return rank-sum per group.

    Handles ties by assigning average rank to tied values.
    Returns a list of rank sums, one per group.
    """
    # Flatten with group index
    tagged = []
    for gi, group in enumerate(groups):
        for val in group:
            tagged.append((val, gi))
    tagged.sort(key=lambda x: x[0])

    n = len(tagged)
    ranks = [0.0] * n

    # Assign ranks, averaging over ties
    i = 0
    while i < n:
        j = i
        while j < n and tagged[j][0] == tagged[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0  # average of 1-based ranks i+1..j
        for idx in range(i, j):
            ranks[idx] = avg_rank
        i = j

    # Sum ranks per group
    rank_sums = [0.0] * len(groups)
    for idx, (val, gi) in enumerate(tagged):
        rank_sums[gi] += ranks[idx]

    return rank_sums


def kruskal_wallis_h(groups):
    """Compute the Kruskal-Wallis H statistic (without tie correction).

    H = (12 / (N(N+1))) * Σ(Rᵢ² / nᵢ) - 3(N+1)
    """
    rank_sums = rank_all(groups)
    total_n = sum(len(g) for g in groups)
    h = (12.0 / (total_n * (total_n + 1))) * sum(
        rs ** 2 / len(g) for rs, g in zip(rank_sums, groups)
    ) - 3 * (total_n + 1)
    return h


def tie_correction_factor(groups):
    """Compute tie correction factor: 1 - Σ(t³ - t) / (N³ - N).

    t = number of tied values in each tie group.
    Returns 1.0 when there are no ties.
    """
    # Flatten all values
    all_vals = []
    for g in groups:
        all_vals.extend(g)
    total_n = len(all_vals)

    counts = Counter(all_vals)
    tie_sum = sum(t ** 3 - t for t in counts.values() if t > 1)

    if tie_sum == 0:
        return 1.0

    return 1.0 - tie_sum / (total_n ** 3 - total_n)


def kruskal_wallis_df(k):
    """Degrees of freedom for the Kruskal-Wallis test: df = k - 1."""
    return k - 1


if __name__ == "__main__":
    rs = rank_all(GROUPS)
    print(f"Rank sums: A={rs[0]:.1f}, B={rs[1]:.1f}, C={rs[2]:.1f}")
    h = kruskal_wallis_h(GROUPS)
    print(f"H = {h:.4f}  (expected {H_STAT:.4f})")
    tc = tie_correction_factor(GROUPS)
    print(f"Tie correction = {tc:.6f}  (no ties -> 1.0)")
    print(f"df = {kruskal_wallis_df(K)}  (expected {DF})")
