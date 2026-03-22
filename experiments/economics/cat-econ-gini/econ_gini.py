"""Gini Coefficient — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_gini_constants import (
    INCOMES, INCOMES_UNSORTED, GINI_TEST,
    CUM_POP_SHARES, CUM_INCOME_SHARES,
    EQUAL_INCOMES, GINI_EQUAL,
    EXTREME_INCOMES, GINI_EXTREME,
)


def lorenz_curve(incomes):
    """Compute Lorenz curve from income data.

    Returns (cum_pop, cum_income) lists including origin (0, 0).
    KEY: Sorts incomes ascending before computing cumulative shares.
    """
    sorted_inc = sorted(incomes)
    n = len(sorted_inc)
    total = sum(sorted_inc)

    cum_pop = [0.0]
    cum_income = [0.0]
    running_sum = 0.0

    for i, inc in enumerate(sorted_inc):
        running_sum += inc
        cum_pop.append((i + 1) / n)
        cum_income.append(running_sum / total if total > 0 else (i + 1) / n)

    return cum_pop, cum_income


def gini_coefficient(incomes):
    """Compute Gini coefficient using the trapezoid method on the Lorenz curve.

    G = 1 - Σᵢ (Xᵢ - Xᵢ₋₁)(Yᵢ + Yᵢ₋₁)
    where X = cumulative pop share, Y = cumulative income share.
    Returns value in [0, 1].
    """
    cum_pop, cum_income = lorenz_curve(incomes)

    # Trapezoid rule: area B under Lorenz curve
    area_b = 0.0
    for i in range(1, len(cum_pop)):
        dx = cum_pop[i] - cum_pop[i - 1]
        area_b += dx * (cum_income[i] + cum_income[i - 1]) / 2.0

    return 1.0 - 2.0 * area_b


def is_perfectly_equal(g, tol=0.01):
    """Check if Gini coefficient indicates perfect equality."""
    return g <= tol


if __name__ == "__main__":
    g = gini_coefficient(INCOMES)
    print(f"Gini({INCOMES}) = {g:.4f}  (expected {GINI_TEST})")

    g_unsorted = gini_coefficient(INCOMES_UNSORTED)
    print(f"Gini({INCOMES_UNSORTED}) = {g_unsorted:.4f}  (should match above)")

    g_eq = gini_coefficient(EQUAL_INCOMES)
    print(f"Gini({EQUAL_INCOMES}) = {g_eq:.4f}  (expected {GINI_EQUAL})")

    g_ext = gini_coefficient(EXTREME_INCOMES)
    print(f"Gini({EXTREME_INCOMES}) = {g_ext:.4f}  (expected {GINI_EXTREME})")

    cum_pop, cum_inc = lorenz_curve(INCOMES)
    print(f"\nLorenz curve for {INCOMES}:")
    print(f"  Pop shares:    {cum_pop}")
    print(f"  Income shares: {cum_inc}")
    print(f"  Perfectly equal? {is_perfectly_equal(g)}")
