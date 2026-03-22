"""cat-stat-correlation — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from stat_correlation_constants import *
IMPL = Path(__file__).parent.parent / "stat_correlation.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_r_squared_is_not_r(self):
        """r^2 != r — they are distinct quantities (prior error: r_squared_is_r)."""
        m = _i()
        r = m.pearson_r(X_DATA, Y_DATA)
        r2 = m.r_squared(r)
        assert abs(r - r2) > 0.01, (
            f"r ({r:.6f}) and r^2 ({r2:.6f}) should differ — "
            "confusing them is a known LLM error"
        )

    def test_correlation_is_symmetric(self):
        """r(x,y) == r(y,x) — correlation is symmetric, causation is not."""
        m = _i()
        r_xy = m.pearson_r(X_DATA, Y_DATA)
        r_yx = m.pearson_r(Y_DATA, X_DATA)
        assert abs(r_xy - r_yx) < 1e-12, (
            f"r(x,y)={r_xy} != r(y,x)={r_yx} — Pearson r must be symmetric"
        )


class TestCorrectness:
    def test_pearson_r_value(self):
        """Pearson r must match the frozen constant."""
        m = _i()
        r = m.pearson_r(X_DATA, Y_DATA)
        assert abs(r - PEARSON_R) < 1e-10, f"r={r}, expected {PEARSON_R}"

    def test_r_squared_value(self):
        """r^2 must match the frozen constant."""
        m = _i()
        r = m.pearson_r(X_DATA, Y_DATA)
        r2 = m.r_squared(r)
        assert abs(r2 - R_SQUARED) < 1e-10, f"r^2={r2}, expected {R_SQUARED}"

    def test_spearman_rho_value(self):
        """Spearman rho (Pearson on ranks, with ties) must match the frozen constant."""
        m = _i()
        rho = m.spearman_rho(X_DATA, Y_DATA)
        assert abs(rho - SPEARMAN_RHO) < 1e-10, f"rho={rho}, expected {SPEARMAN_RHO}"
