"""cat-eng-pipe-flow — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_pipe_flow_constants import *
IMPL = Path(__file__).parent.parent / "eng_pipe_flow.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guards against known LLM mistakes in PRIOR_ERRORS."""

    def test_hp_only_laminar(self):
        """HP must NOT be trusted in turbulent regime."""
        m = _i()
        assert m.is_laminar(635) is True,   "Re=635 should be laminar"
        assert m.is_laminar(50000) is False, "Re=50000 must NOT be laminar"
        assert m.is_laminar(2300) is False,  "Re=2300 is transitional, not laminar"

    def test_diameter_not_radius(self):
        """Formula must use diameter d, not radius — verify d⁴ scaling."""
        m = _i()
        dP1 = m.hagen_poiseuille_dP(Q_TEST, D_TEST, MU_TEST, L_TEST)
        # If code wrongly used r=d (treating input as radius), dP would be 16x smaller
        assert abs(dP1 - DP_TEST) < 0.1, f"dP={dP1:.2f}, expected {DP_TEST:.2f}"

    def test_velocity_not_flow(self):
        """avg_velocity must return v=Q/A, not confuse Q and v."""
        m = _i()
        v = m.avg_velocity(Q_TEST, D_TEST)
        assert abs(v - V_TEST) < 1e-4, f"v={v}, expected {V_TEST}"


class TestCorrectness:
    """Golden-value tests against frozen constants."""

    def test_dP_from_Q(self):
        m = _i()
        dP = m.hagen_poiseuille_dP(Q_TEST, D_TEST, MU_TEST, L_TEST)
        assert abs(dP - DP_TEST) < 0.1

    def test_Q_from_dP(self):
        m = _i()
        Q = m.hagen_poiseuille_Q(DP_TEST, D_TEST, MU_TEST, L_TEST)
        assert abs(Q - Q_TEST) < 1e-8

    def test_roundtrip(self):
        """Q → ΔP → Q must round-trip."""
        m = _i()
        dP = m.hagen_poiseuille_dP(Q_TEST, D_TEST, MU_TEST, L_TEST)
        Q_back = m.hagen_poiseuille_Q(dP, D_TEST, MU_TEST, L_TEST)
        assert abs(Q_back - Q_TEST) < 1e-12

    def test_avg_velocity(self):
        m = _i()
        v = m.avg_velocity(Q_TEST, D_TEST)
        assert abs(v - V_TEST) < 1e-5

    def test_reynolds_laminar(self):
        m = _i()
        assert m.is_laminar(RE_TEST) is True, f"Re={RE_TEST:.1f} should be laminar"
