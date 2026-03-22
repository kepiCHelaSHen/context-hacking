"""Fisher's Exact Test — CHP Statistics Sprint."""
import sys
import math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_fisher_exact_constants import *


def table_margins(table):
    """Compute margins of a 2x2 contingency table.

    Returns (R1, R2, C1, C2, N).
    """
    a, b = table[0]
    c, d = table[1]
    return a + b, c + d, a + c, b + d, a + b + c + d


def hypergeom_pmf(a, R1, R2, C1, N):
    """Hypergeometric probability for cell count a.

    P(a) = C(R1, a) * C(R2, C1 - a) / C(N, C1)
    """
    if a < 0 or a > R1 or (C1 - a) < 0 or (C1 - a) > R2:
        return 0.0
    return math.comb(R1, a) * math.comb(R2, C1 - a) / math.comb(N, C1)


def fisher_one_tail(table, direction="greater"):
    """One-tailed Fisher exact test.

    direction='greater': P(X >= observed a)
    direction='less':    P(X <= observed a)
    """
    a_obs = table[0][0]
    r1, r2, c1, c2, n = table_margins(table)
    a_min = max(0, c1 - r2)
    a_max = min(r1, c1)

    if direction == "greater":
        return sum(hypergeom_pmf(a, r1, r2, c1, n)
                   for a in range(a_obs, a_max + 1))
    else:
        return sum(hypergeom_pmf(a, r1, r2, c1, n)
                   for a in range(a_min, a_obs + 1))


def fisher_two_tail(table):
    """Two-tailed Fisher exact test.

    Sums probabilities of all tables whose probability <= observed probability.
    """
    a_obs = table[0][0]
    r1, r2, c1, c2, n = table_margins(table)
    a_min = max(0, c1 - r2)
    a_max = min(r1, c1)

    p_obs = hypergeom_pmf(a_obs, r1, r2, c1, n)
    return sum(p for a in range(a_min, a_max + 1)
               if (p := hypergeom_pmf(a, r1, r2, c1, n)) <= p_obs + 1e-15)


if __name__ == "__main__":
    r1, r2, c1, c2, n = table_margins(TABLE)
    print(f"Table: {TABLE}")
    print(f"Margins: R1={r1}, R2={r2}, C1={c1}, C2={c2}, N={n}")
    print(f"P(a=3) = {hypergeom_pmf(3, r1, r2, c1, n):.10f}  (expect {P_EXACT:.10f})")
    print(f"One-tail (>=3): {fisher_one_tail(TABLE):.10f}  (expect {P_ONE_TAIL:.10f})")
    print(f"Two-tail:       {fisher_two_tail(TABLE):.10f}  (expect {P_TWO_TAIL:.10f})")
