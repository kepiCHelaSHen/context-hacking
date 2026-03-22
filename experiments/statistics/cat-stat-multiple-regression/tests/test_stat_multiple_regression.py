"""cat-stat-multiple-regression — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_multiple_regression_constants import *
IMPL = Path(__file__).parent.parent / "stat_multiple_regression.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_vif_detects_collinearity(self):
        """VIF for r ≈ 0.995 must flag severe multicollinearity (VIF >> 10)."""
        m = _i()
        r = m.pearson_r(X1_DATA, X2_DATA)
        r_sq = r ** 2
        v = m.vif(r_sq)
        assert v > VIF_THRESHOLD_SEVERE, (
            f"VIF={v:.1f} should exceed severe threshold {VIF_THRESHOLD_SEVERE} "
            f"for r={r:.5f} — ignoring VIF leads to misinterpreting coefficients"
        )

    def test_vif_above_10_flags_severe(self):
        """Any VIF > 10 must be classified as collinear."""
        m = _i()
        assert m.is_collinear(VIF_X1, VIF_THRESHOLD_SEVERE), (
            f"VIF={VIF_X1} should be flagged as severe collinearity (threshold={VIF_THRESHOLD_SEVERE})"
        )

    def test_partial_not_total(self):
        """Correlation of X1 with X2 is very high — partial ≠ total effect."""
        m = _i()
        r = m.pearson_r(X1_DATA, X2_DATA)
        # If r(X1,X2) > 0.99, treating beta1 as the 'total effect of X1' is wrong
        assert abs(r) > 0.99, (
            f"r(X1,X2)={r:.5f} should be > 0.99, confirming confounding; "
            f"partial coefficient cannot be read as total effect"
        )


class TestCorrectness:
    def test_pearson_r_value(self):
        """Pearson r(X1, X2) must match frozen constant."""
        m = _i()
        r = m.pearson_r(X1_DATA, X2_DATA)
        assert abs(r - CORR_X1_X2) < 1e-4, (
            f"pearson_r={r:.5f}, expected {CORR_X1_X2}"
        )

    def test_vif_computation(self):
        """VIF(X1) must match frozen constant."""
        m = _i()
        v = m.vif(R_SQ_X1_ON_X2)
        assert abs(v - VIF_X1) < 1.0, (
            f"vif={v:.1f}, expected ≈{VIF_X1}"
        )

    def test_is_collinear_true(self):
        """VIF >> 10 → is_collinear must return True."""
        m = _i()
        assert m.is_collinear(VIF_X1) is True

    def test_is_collinear_false_below_threshold(self):
        """VIF = 1.0 (no collinearity) → is_collinear must return False."""
        m = _i()
        assert m.is_collinear(1.0) is False

    def test_mean(self):
        """mean() must compute the arithmetic average."""
        m = _i()
        assert abs(m.mean(X1_DATA) - MEAN_X1) < 1e-10
        assert abs(m.mean(X2_DATA) - MEAN_X2) < 1e-10

    def test_ss(self):
        """ss() must compute sum of squared deviations from mean."""
        m = _i()
        # ss(X1) = sum((xi - 3)^2) = 4+1+0+1+4 = 10
        assert abs(m.ss(X1_DATA) - 10.0) < 1e-10
