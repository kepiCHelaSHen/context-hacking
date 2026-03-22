"""Cobb-Douglas Production Function — CHP Economics Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from econ_cobb_douglas_constants import *


def cobb_douglas(A, K, alpha, L, beta):
    """Compute output Y = A * K^alpha * L^beta (general Cobb-Douglas)."""
    return A * K ** alpha * L ** beta


def returns_to_scale(alpha, beta):
    """Classify returns to scale based on sum of exponents.

    alpha + beta > 1  => 'increasing'
    alpha + beta == 1 => 'constant'
    alpha + beta < 1  => 'decreasing'
    """
    s = alpha + beta
    if abs(s - 1.0) < 1e-9:
        return "constant"
    elif s > 1.0:
        return "increasing"
    else:
        return "decreasing"


def mpk(A, K, alpha, L, beta):
    """Marginal product of capital: dY/dK = alpha * A * K^(alpha-1) * L^beta."""
    return alpha * A * K ** (alpha - 1) * L ** beta


def mpl(A, K, alpha, L, beta):
    """Marginal product of labor: dY/dL = beta * A * K^alpha * L^(beta-1)."""
    return beta * A * K ** alpha * L ** (beta - 1)


if __name__ == "__main__":
    # IRS test case
    Y_base = cobb_douglas(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST)
    Y_double = cobb_douglas(A_TEST, K2, ALPHA_TEST, L2, BETA_TEST)
    ratio = Y_double / Y_base
    rts = returns_to_scale(ALPHA_TEST, BETA_TEST)
    print(f"alpha={ALPHA_TEST}, beta={BETA_TEST}, sum={SUM_EXPONENTS}")
    print(f"Y(K={K1}, L={L1}) = {Y_base:.2f}")
    print(f"Y(K={K2}, L={L2}) = {Y_double:.2f}")
    print(f"Ratio when inputs doubled: {ratio:.4f}  (2^{SUM_EXPONENTS} = {THEORETICAL_RATIO:.4f})")
    print(f"Returns to scale: {rts}")
    print(f"\nMPK = {mpk(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST):.6f}")
    print(f"MPL = {mpl(A_TEST, K1, ALPHA_TEST, L1, BETA_TEST):.6f}")

    # CRS case
    print(f"\nCRS case: alpha={ALPHA_CRS}, beta={BETA_CRS}")
    print(f"Returns to scale: {returns_to_scale(ALPHA_CRS, BETA_CRS)}")
    K, L = 50, 100
    Y_crs = cobb_douglas(1, K, ALPHA_CRS, L, BETA_CRS)
    labor_sh = mpl(1, K, ALPHA_CRS, L, BETA_CRS) * L / Y_crs
    capital_sh = mpk(1, K, ALPHA_CRS, L, BETA_CRS) * K / Y_crs
    print(f"Labor share: {labor_sh:.4f} (should be {BETA_CRS})")
    print(f"Capital share: {capital_sh:.4f} (should be {ALPHA_CRS})")
