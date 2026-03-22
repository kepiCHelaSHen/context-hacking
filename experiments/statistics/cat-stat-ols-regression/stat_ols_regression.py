"""OLS Regression — CHP Statistics Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from stat_ols_regression_constants import *


def ols_slope(x, y):
    """beta1 = sum((xi - x_bar)(yi - y_bar)) / sum((xi - x_bar)^2)"""
    n = len(x)
    x_bar = sum(x) / n
    y_bar = sum(y) / n
    num = sum((xi - x_bar) * (yi - y_bar) for xi, yi in zip(x, y))
    den = sum((xi - x_bar) ** 2 for xi in x)
    return num / den


def ols_intercept(x, y, slope):
    """beta0 = y_bar - beta1 * x_bar"""
    return sum(y) / len(y) - slope * (sum(x) / len(x))


def predict(x_val, slope, intercept):
    """y_hat = beta0 + beta1 * x"""
    return intercept + slope * x_val


def r_squared(y, y_pred):
    """R^2 = 1 - SSR / SST"""
    y_bar = sum(y) / len(y)
    ssr = sum((yi - yp) ** 2 for yi, yp in zip(y, y_pred))
    sst = sum((yi - y_bar) ** 2 for yi in y)
    return 1 - ssr / sst


def adjusted_r_squared(r2, n, p):
    """Adjusted R^2 = 1 - (1 - R^2)(n-1)/(n-p-1)"""
    return 1 - (1 - r2) * (n - 1) / (n - p - 1)


def residuals(y, y_pred):
    """Return list of residuals (yi - y_hat_i)."""
    return [yi - yp for yi, yp in zip(y, y_pred)]


if __name__ == "__main__":
    slope = ols_slope(X_DATA, Y_DATA)
    intercept = ols_intercept(X_DATA, Y_DATA, slope)
    preds = [predict(xi, slope, intercept) for xi in X_DATA]
    r2 = r_squared(Y_DATA, preds)
    adj_r2 = adjusted_r_squared(r2, N, P)
    res = residuals(Y_DATA, preds)
    print(f"beta1={slope:.4f}, beta0={intercept:.4f}")
    print(f"predictions: {[round(p, 2) for p in preds]}")
    print(f"residuals:   {[round(r, 4) for r in res]}")
    print(f"R^2={r2:.5f}, Adj R^2={adj_r2:.5f}")
