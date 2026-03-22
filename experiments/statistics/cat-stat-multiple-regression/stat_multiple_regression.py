"""Multiple Regression — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_multiple_regression_constants import *


def mean(data):
    """Arithmetic mean."""
    return sum(data) / len(data)


def ss(data):
    """Sum of squared deviations from the mean."""
    m = mean(data)
    return sum((x - m) ** 2 for x in data)


def pearson_r(x, y):
    """Pearson correlation coefficient between x and y."""
    n = len(x)
    mx = mean(x)
    my = mean(y)
    num = sum((xi - mx) * (yi - my) for xi, yi in zip(x, y))
    den = math.sqrt(ss(x) * ss(y))
    if den == 0:
        return 0.0
    return num / den


def vif(r_squared_j):
    """Variance Inflation Factor: VIF = 1 / (1 - R^2_j)."""
    if r_squared_j >= 1.0:
        return float('inf')
    return 1.0 / (1.0 - r_squared_j)


def is_collinear(vif_value, threshold=10):
    """Return True if VIF exceeds the collinearity threshold."""
    return vif_value > threshold


if __name__ == "__main__":
    r = pearson_r(X1_DATA, X2_DATA)
    r_sq = r ** 2
    v = vif(r_sq)
    print(f"Pearson r(X1, X2) = {r:.5f}")
    print(f"R^2(X1 on X2)     = {r_sq:.5f}")
    print(f"VIF(X1)            = {v:.1f}")
    print(f"Severe collinearity (VIF > {VIF_THRESHOLD_SEVERE})? {is_collinear(v, VIF_THRESHOLD_SEVERE)}")
    print(f"Moderate collinearity (VIF > {VIF_THRESHOLD_MODERATE})? {is_collinear(v, VIF_THRESHOLD_MODERATE)}")
