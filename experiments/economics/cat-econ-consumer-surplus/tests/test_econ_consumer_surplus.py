"""cat-econ-consumer-surplus — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_consumer_surplus_constants import *
IMPL = Path(__file__).parent.parent / "econ_consumer_surplus.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Guard against known LLM mistakes."""

    def test_cs_not_total_area(self):
        """CS must NOT equal total area under demand curve (0.5 * P_max * Q_eq)."""
        m = _i()
        cs = m.consumer_surplus_linear(P_MAX, P_EQ, Q_EQ)
        total_area_under_demand = 0.5 * P_MAX * Q_EQ  # = 1300 (WRONG)
        assert abs(cs - total_area_under_demand) > 1.0, \
            "CS equals total area under demand — should be area ABOVE P* only"

    def test_ps_not_zero_base(self):
        """PS base must be P_min (supply intercept), not 0."""
        m = _i()
        ps = m.producer_surplus_linear(P_MIN, P_EQ, Q_EQ)
        ps_wrong = 0.5 * P_EQ * Q_EQ  # uses 0 as base (WRONG) = 624
        assert abs(ps - ps_wrong) > 1.0, \
            "PS uses 0 as base price — should use supply intercept P_min"

    def test_surplus_correct_variable(self):
        """Surplus must be computed w.r.t. quantity (area of triangle in P-Q space)."""
        m = _i()
        cs = m.consumer_surplus_linear(P_MAX, P_EQ, Q_EQ)
        # Wrong approach: integrating Q w.r.t. P from 0 to P* gives different result
        assert abs(cs - CS_EXPECTED) < 0.01


class TestCorrectness:
    def test_demand_intercept(self):
        m = _i()
        assert abs(m.demand_intercept_price(A_DEMAND, B_DEMAND) - P_MAX) < 0.001

    def test_supply_intercept(self):
        m = _i()
        assert abs(m.supply_intercept_price(C_SUPPLY, D_SUPPLY) - P_MIN) < 0.001

    def test_consumer_surplus_value(self):
        m = _i()
        cs = m.consumer_surplus_linear(P_MAX, P_EQ, Q_EQ)
        assert abs(cs - CS_EXPECTED) < 0.01, f"CS={cs}, expected {CS_EXPECTED}"

    def test_producer_surplus_value(self):
        m = _i()
        ps = m.producer_surplus_linear(P_MIN, P_EQ, Q_EQ)
        assert abs(ps - PS_EXPECTED) < 0.01, f"PS={ps}, expected {PS_EXPECTED}"

    def test_total_surplus_value(self):
        m = _i()
        cs = m.consumer_surplus_linear(P_MAX, P_EQ, Q_EQ)
        ps = m.producer_surplus_linear(P_MIN, P_EQ, Q_EQ)
        ts = m.total_surplus(cs, ps)
        assert abs(ts - TOTAL_SURPLUS_EXPECTED) < 0.01, \
            f"Total={ts}, expected {TOTAL_SURPLUS_EXPECTED}"

    def test_cs_plus_ps_equals_total(self):
        m = _i()
        cs = m.consumer_surplus_linear(P_MAX, P_EQ, Q_EQ)
        ps = m.producer_surplus_linear(P_MIN, P_EQ, Q_EQ)
        assert abs(m.total_surplus(cs, ps) - (cs + ps)) < 0.001
