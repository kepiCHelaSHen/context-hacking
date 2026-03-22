"""Chi-Squared Distribution — CHP Statistics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_chi_squared_constants import *


def chi_squared_gof(observed, expected):
    """Compute χ² statistic for a goodness-of-fit test.

    χ² = Σ (O_i - E_i)² / E_i
    """
    if len(observed) != len(expected):
        raise ValueError("observed and expected must have the same length")
    return sum((o - e) ** 2 / e for o, e in zip(observed, expected))


def gof_df(k):
    """Degrees of freedom for goodness-of-fit: df = k - 1."""
    return k - 1


def contingency_expected(table):
    """Compute expected frequencies from marginal totals.

    E_ij = (row_i_total * col_j_total) / grand_total
    """
    rows = len(table)
    cols = len(table[0])
    row_totals = [sum(table[i]) for i in range(rows)]
    col_totals = [sum(table[i][j] for i in range(rows)) for j in range(cols)]
    grand = sum(row_totals)
    return [[row_totals[i] * col_totals[j] / grand
             for j in range(cols)]
            for i in range(rows)]


def chi_squared_independence(table):
    """Compute χ² statistic for a test of independence on a contingency table."""
    expected = contingency_expected(table)
    rows = len(table)
    cols = len(table[0])
    return sum((table[i][j] - expected[i][j]) ** 2 / expected[i][j]
               for i in range(rows) for j in range(cols))


def independence_df(r, c):
    """Degrees of freedom for independence test: df = (r-1)(c-1)."""
    return (r - 1) * (c - 1)


if __name__ == "__main__":
    chi2_gof = chi_squared_gof(GOF_OBSERVED, GOF_EXPECTED)
    print(f"GoF: chi2={chi2_gof:.4f}, df={gof_df(GOF_K)} (k={GOF_K})")
    chi2_ind = chi_squared_independence(IND_TABLE)
    print(f"Independence: chi2={chi2_ind:.4f}, df={independence_df(IND_ROWS, IND_COLS)} "
          f"({IND_ROWS}x{IND_COLS} table)")
    print(f"Expected table: {contingency_expected(IND_TABLE)}")
