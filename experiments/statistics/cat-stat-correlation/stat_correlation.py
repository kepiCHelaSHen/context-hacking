"""Correlation — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_correlation_constants import *


def pearson_r(x, y):
    """Pearson r = sum((xi-x_bar)(yi-y_bar)) / sqrt(sum((xi-x_bar)^2) * sum((yi-y_bar)^2))"""
    n = len(x)
    x_bar = sum(x) / n
    y_bar = sum(y) / n
    num = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    den_x = sum((xi - x_bar) ** 2 for xi in x)
    den_y = sum((yi - y_bar) ** 2 for yi in y)
    return num / math.sqrt(den_x * den_y)


def r_squared(r):
    """r^2 = proportion of variance explained."""
    return r ** 2


def rank_data(data):
    """Rank data using the average-rank method (handles ties correctly)."""
    n = len(data)
    # pair each value with its original index, sort by value
    indexed = sorted(range(n), key=lambda i: data[i])
    ranks = [0.0] * n
    i = 0
    while i < n:
        # find the run of tied values
        j = i + 1
        while j < n and data[indexed[j]] == data[indexed[i]]:
            j += 1
        # average rank for positions i..j-1 (1-based)
        avg_rank = sum(range(i + 1, j + 1)) / (j - i)
        for k in range(i, j):
            ranks[indexed[k]] = avg_rank
        i = j
    return ranks


def spearman_rho(x, y):
    """Spearman rho = Pearson r computed on ranks (handles ties via average-rank)."""
    return pearson_r(rank_data(x), rank_data(y))


if __name__ == "__main__":
    r = pearson_r(X_DATA, Y_DATA)
    r2 = r_squared(r)
    rho = spearman_rho(X_DATA, Y_DATA)
    print(f"Pearson r  = {r:.6f}")
    print(f"r^2        = {r2:.6f}")
    print(f"Spearman rho = {rho:.6f}")
