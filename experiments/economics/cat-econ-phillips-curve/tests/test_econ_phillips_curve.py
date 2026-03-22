"""cat-econ-phillips-curve — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_phillips_curve_constants import *
IMPL = Path(__file__).parent.parent / "econ_phillips_curve.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_no_stable_long_run_tradeoff(self):
        """Long-run: at u=uₙ, inflation equals expected — no tradeoff."""
        m = _i(); pi = m.short_run_phillips(PI_E, BETA, U_N, U_N)
        assert abs(pi - PI_E) < 1e-10, "At NAIRU, π must equal πᵉ (vertical long-run curve)"
    def test_nairu_not_zero(self):
        """NAIRU should be positive, not zero."""
        m = _i()
        assert m.nairu() > 0, "NAIRU cannot be zero"
        assert abs(m.nairu() - U_N) < 1e-10
    def test_expectations_included(self):
        """Changing πᵉ must shift the short-run curve."""
        m = _i()
        pi_low = m.short_run_phillips(1.0, BETA, 4.0, U_N)
        pi_high = m.short_run_phillips(5.0, BETA, 4.0, U_N)
        assert pi_high > pi_low, "Higher πᵉ must raise inflation (expectations matter)"

class TestCorrectness:
    def test_below_nairu(self):
        m = _i(); pi = m.short_run_phillips(PI_E, BETA, 3.0, U_N)
        assert abs(pi - PI_AT_U3) < 1e-10
    def test_at_nairu(self):
        m = _i(); pi = m.short_run_phillips(PI_E, BETA, 5.0, U_N)
        assert abs(pi - PI_AT_U5) < 1e-10
    def test_above_nairu(self):
        m = _i(); pi = m.short_run_phillips(PI_E, BETA, 7.0, U_N)
        assert abs(pi - PI_AT_U7) < 1e-10
    def test_is_long_run_true(self):
        m = _i(); assert m.is_long_run(5.0, 5.0) is True
    def test_is_long_run_false(self):
        m = _i(); assert m.is_long_run(3.0, 5.0) is False
    def test_long_run_inflation(self):
        m = _i(); assert abs(m.long_run_inflation(PI_E) - LONG_RUN_PI) < 1e-10
    def test_long_run_inflation_different_expectation(self):
        m = _i(); assert abs(m.long_run_inflation(4.0) - 4.0) < 1e-10
