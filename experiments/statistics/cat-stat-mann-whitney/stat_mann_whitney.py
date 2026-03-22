"""Mann-Whitney U Test — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_mann_whitney_constants import *


def rank_combined(a, b):
    """Return dict mapping each value to its rank in the combined sample (1-based)."""
    combined = sorted(set(a) | set(b))
    # Simple ranking (no ties in test data; for ties, average rank)
    all_vals = sorted(list(a) + list(b))
    ranks = {}
    i = 0
    while i < len(all_vals):
        j = i + 1
        while j < len(all_vals) and all_vals[j] == all_vals[i]:
            j += 1
        avg_rank = sum(range(i + 1, j + 1)) / (j - i)
        ranks[all_vals[i]] = avg_rank
        i = j
    return ranks


def mann_whitney_u(a, b):
    """Compute (U1, U2, U) where U = min(U1, U2)."""
    n1, n2 = len(a), len(b)
    ranks = rank_combined(a, b)
    r1 = sum(ranks[v] for v in a)
    u1 = n1 * n2 + n1 * (n1 + 1) / 2 - r1
    u2 = n1 * n2 - u1
    return u1, u2, min(u1, u2)


def u_check(u1, u2, n1, n2):
    """Verify the identity U1 + U2 == n1 * n2."""
    return abs((u1 + u2) - n1 * n2) < 1e-9


if __name__ == "__main__":
    u1, u2, u = mann_whitney_u(GROUP_A, GROUP_B)
    print(f"Group A: {GROUP_A}  Group B: {GROUP_B}")
    print(f"U1={u1:.0f}, U2={u2:.0f}, U=min={u:.0f}")
    print(f"Identity check: U1+U2={u1+u2:.0f} == n1*n2={N1*N2} → {u_check(u1, u2, N1, N2)}")
