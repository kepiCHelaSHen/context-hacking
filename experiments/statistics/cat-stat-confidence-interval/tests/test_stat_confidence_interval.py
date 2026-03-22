"""cat-stat-confidence-interval — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_confidence_interval_constants import *
IMPL = Path(__file__).parent.parent / "stat_confidence_interval.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_99ci_wider_than_95ci(self):
        """99% CI must be WIDER than 95% CI — wider is NOT more precise."""
        m = _i()
        se = m.standard_error(SIGMA, N)
        w95 = m.ci_width(Z_95, se)
        w99 = m.ci_width(Z_99, se)
        assert w99 > w95, "99% CI should be wider than 95% CI"

    def test_ci_width_scales_inverse_sqrt_n(self):
        """CI width scales with 1/√n, not with n."""
        m = _i()
        se_36  = m.standard_error(SIGMA, 36)
        se_144 = m.standard_error(SIGMA, 144)
        # Quadrupling n should halve SE (and thus halve width)
        assert abs(se_36 / se_144 - 2.0) < 1e-10


class TestCorrectness:
    def test_standard_error(self):
        m = _i()
        assert abs(m.standard_error(SIGMA, N) - SE) < 1e-10

    def test_95_ci_bounds(self):
        m = _i()
        lo, hi = m.ci_bounds(XBAR, Z_95, SE)
        assert abs(lo - CI_95_LOWER) < 1e-10
        assert abs(hi - CI_95_UPPER) < 1e-10

    def test_99_ci_bounds(self):
        m = _i()
        lo, hi = m.ci_bounds(XBAR, Z_99, SE)
        assert abs(lo - CI_99_LOWER) < 1e-10
        assert abs(hi - CI_99_UPPER) < 1e-10

    def test_margin_of_error_95(self):
        m = _i()
        moe = m.margin_of_error(Z_95, SE)
        assert abs(moe - Z_95 * SE) < 1e-10

    def test_ci_width_value(self):
        m = _i()
        w = m.ci_width(Z_95, SE)
        assert abs(w - 2 * Z_95 * SE) < 1e-10
