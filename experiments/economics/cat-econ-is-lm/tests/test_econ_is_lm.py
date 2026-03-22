"""cat-econ-is-lm — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_is_lm_constants import *
IMPL = Path(__file__).parent.parent / "econ_is_lm.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_is_slopes_down(self):
        """IS slope must be negative — LLMs often make it positive."""
        m = _i(); slope = m.is_slope(c, t, b)
        assert slope < 0, f"IS slope = {slope}, should be negative"

    def test_lm_slopes_up(self):
        """LM slope must be positive — LLMs often make it negative."""
        m = _i(); slope = m.lm_slope(k, h)
        assert slope > 0, f"LM slope = {slope}, should be positive"

    def test_is_slope_value(self):
        m = _i(); slope = m.is_slope(c, t, b)
        assert abs(slope - IS_SLOPE) < 1e-10

    def test_lm_slope_value(self):
        m = _i(); slope = m.lm_slope(k, h)
        assert abs(slope - LM_SLOPE) < 1e-10

    def test_equilibrium_not_wrong(self):
        """Equilibrium must match frozen constants — catches algebra errors."""
        m = _i(); Y_eq, r_eq = m.is_lm_equilibrium(A, c, t, b, k, h, M_P)
        assert abs(Y_eq - Y_STAR) < 0.01, f"Y* = {Y_eq}, expected {Y_STAR:.4f}"
        assert abs(r_eq - R_STAR) < 0.001, f"r* = {r_eq}, expected {R_STAR:.6f}"


class TestCorrectness:
    def test_is_curve_at_zero(self):
        m = _i(); r = m.is_curve(0, A, c, t, b)
        assert abs(r - IS_AT_0) < 1e-10

    def test_is_curve_at_1000(self):
        m = _i(); r = m.is_curve(1000, A, c, t, b)
        assert abs(r - IS_AT_1000) < 1e-10

    def test_lm_curve_at_zero(self):
        m = _i(); r = m.lm_curve(0, k, h, M_P)
        assert abs(r - LM_AT_0) < 1e-10

    def test_lm_curve_at_1000(self):
        m = _i(); r = m.lm_curve(1000, k, h, M_P)
        assert abs(r - LM_AT_1000) < 1e-10

    def test_equilibrium_is_eq_lm(self):
        """At equilibrium, IS(Y*) must equal LM(Y*) must equal r*."""
        m = _i(); Y_eq, r_eq = m.is_lm_equilibrium(A, c, t, b, k, h, M_P)
        r_is = m.is_curve(Y_eq, A, c, t, b)
        r_lm = m.lm_curve(Y_eq, k, h, M_P)
        assert abs(r_is - r_eq) < 1e-10
        assert abs(r_lm - r_eq) < 1e-10

    def test_equilibrium_positive(self):
        """Both Y* and r* should be positive with the test params."""
        m = _i(); Y_eq, r_eq = m.is_lm_equilibrium(A, c, t, b, k, h, M_P)
        assert Y_eq > 0
        assert r_eq > 0
