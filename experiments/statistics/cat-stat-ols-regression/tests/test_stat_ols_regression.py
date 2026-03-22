"""cat-stat-ols-regression — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_ols_regression_constants import *
IMPL = Path(__file__).parent.parent / "stat_ols_regression.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_adj_r2_less_than_r2(self):
        """Adjusted R^2 must be < R^2 when p >= 1 — using R^2 alone hides overfitting."""
        m = _i()
        preds = [m.predict(xi, BETA1, BETA0) for xi in X_DATA]
        r2 = m.r_squared(Y_DATA, preds)
        adj = m.adjusted_r_squared(r2, N, P)
        assert adj < r2, (
            f"Adjusted R^2 ({adj}) must be strictly less than R^2 ({r2}) when p>=1"
        )

    def test_r2_uses_correct_ssr_sst_ratio(self):
        """R^2 = 1 - SSR/SST, NOT SSR/SST (the swap error)."""
        m = _i()
        preds = [m.predict(xi, BETA1, BETA0) for xi in X_DATA]
        r2 = m.r_squared(Y_DATA, preds)
        # R^2 for this near-linear data must be close to 1, not close to 0
        assert r2 > 0.99, f"R^2={r2} too low — possible SSR/SST swap"
        # Also verify it is NOT just SSR/SST (which would be ~0.0027)
        assert r2 > 0.5, "R^2 appears to be SSR/SST rather than 1 - SSR/SST"


class TestCorrectness:
    def test_slope_value(self):
        """beta1 must match the frozen constant."""
        m = _i()
        slope = m.ols_slope(X_DATA, Y_DATA)
        assert abs(slope - BETA1) < 1e-6, f"slope={slope}, expected {BETA1}"

    def test_intercept_value(self):
        """beta0 must match the frozen constant."""
        m = _i()
        slope = m.ols_slope(X_DATA, Y_DATA)
        intercept = m.ols_intercept(X_DATA, Y_DATA, slope)
        assert abs(intercept - BETA0) < 1e-4, f"intercept={intercept}, expected {BETA0}"

    def test_r_squared_value(self):
        """R^2 must match the frozen constant within tolerance."""
        m = _i()
        preds = [m.predict(xi, BETA1, BETA0) for xi in X_DATA]
        r2 = m.r_squared(Y_DATA, preds)
        assert abs(r2 - R_SQUARED) < 1e-4, f"R^2={r2}, expected {R_SQUARED}"
