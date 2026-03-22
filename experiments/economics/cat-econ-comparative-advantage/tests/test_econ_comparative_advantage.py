"""cat-econ-comparative-advantage — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_comparative_advantage_constants import *
IMPL = Path(__file__).parent.parent / "econ_comparative_advantage.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


# ── Prior-Error Guards ───────────────────────────────────────────────

class TestPriorErrors:
    """Guard against known LLM failure modes."""

    def test_absolute_is_not_comparative(self):
        """Absolute advantage ≠ comparative advantage.
        A has absolute advantage in BOTH goods, but comparative in only ONE."""
        m = _i()
        # A has lower hours for both goods (absolute advantage in both)
        assert A_HOURS_WINE < B_HOURS_WINE
        assert A_HOURS_CLOTH < B_HOURS_CLOTH
        # But comparative advantage splits: A→cloth, B→wine
        oc_a_cloth = m.opportunity_cost(A_HOURS_CLOTH, A_HOURS_WINE)
        oc_b_cloth = m.opportunity_cost(B_HOURS_CLOTH, B_HOURS_WINE)
        oc_a_wine  = m.opportunity_cost(A_HOURS_WINE, A_HOURS_CLOTH)
        oc_b_wine  = m.opportunity_cost(B_HOURS_WINE, B_HOURS_CLOTH)
        assert m.has_comparative_advantage(oc_a_cloth, oc_b_cloth)   # A wins cloth
        assert not m.has_comparative_advantage(oc_a_wine, oc_b_wine) # A does NOT win wine

    def test_both_advantage_one_country_impossible(self):
        """No country can have comparative advantage in BOTH goods."""
        m = _i()
        a_cloth = m.has_comparative_advantage(OC_A_CLOTH, OC_B_CLOTH)
        a_wine  = m.has_comparative_advantage(OC_A_WINE,  OC_B_WINE)
        # A cannot win both
        assert not (a_cloth and a_wine), "One country cannot have comp. adv. in both goods"
        # And at least one must hold for each country
        assert a_cloth or a_wine, "At least one good must show comp. adv."

    def test_opportunity_cost_correct(self):
        """OC(X) = hours_X / hours_Y, NOT hours_Y / hours_X."""
        m = _i()
        assert abs(m.opportunity_cost(A_HOURS_WINE, A_HOURS_CLOTH) - OC_A_WINE) < 1e-9
        assert abs(m.opportunity_cost(A_HOURS_CLOTH, A_HOURS_WINE) - OC_A_CLOTH) < 1e-9
        assert abs(m.opportunity_cost(B_HOURS_WINE, B_HOURS_CLOTH) - OC_B_WINE) < 1e-9
        assert abs(m.opportunity_cost(B_HOURS_CLOTH, B_HOURS_WINE) - OC_B_CLOTH) < 1e-9


# ── Correctness Tests ────────────────────────────────────────────────

class TestCorrectness:
    """Verify numerical results and function contracts."""

    def test_opportunity_cost_values(self):
        m = _i()
        assert abs(m.opportunity_cost(10, 5) - 2.0) < 1e-9       # A: wine costs 2 cloth
        assert abs(m.opportunity_cost(5, 10) - 0.5) < 1e-9       # A: cloth costs 0.5 wine
        assert abs(m.opportunity_cost(20, 15) - 4/3) < 1e-9      # B: wine costs 1.333 cloth
        assert abs(m.opportunity_cost(15, 20) - 0.75) < 1e-9     # B: cloth costs 0.75 wine

    def test_comparative_advantage_cloth(self):
        m = _i()
        assert m.has_comparative_advantage(OC_A_CLOTH, OC_B_CLOTH) is True   # A wins cloth

    def test_comparative_advantage_wine(self):
        m = _i()
        assert m.has_comparative_advantage(OC_B_WINE, OC_A_WINE) is True     # B wins wine

    def test_gains_from_trade_exist(self):
        m = _i()
        assert m.gains_from_trade(OC_A_WINE, OC_B_WINE) is True

    def test_no_gains_when_equal(self):
        m = _i()
        assert m.gains_from_trade(2.0, 2.0) is False

    def test_terms_of_trade_range(self):
        m = _i()
        lo, hi = m.terms_of_trade_range(OC_A_WINE, OC_B_WINE)
        assert abs(lo - OC_B_WINE) < 1e-9    # 1.333 cloth per wine
        assert abs(hi - OC_A_WINE) < 1e-9    # 2.0   cloth per wine
        assert lo < hi

    def test_terms_of_trade_range_commutative(self):
        """Order of arguments shouldn't matter."""
        m = _i()
        lo1, hi1 = m.terms_of_trade_range(OC_A_WINE, OC_B_WINE)
        lo2, hi2 = m.terms_of_trade_range(OC_B_WINE, OC_A_WINE)
        assert abs(lo1 - lo2) < 1e-9
        assert abs(hi1 - hi2) < 1e-9

    def test_reciprocal_opportunity_costs(self):
        """OC(wine)*OC(cloth) = 1 for any country (they are reciprocals)."""
        m = _i()
        oc_a_w = m.opportunity_cost(A_HOURS_WINE, A_HOURS_CLOTH)
        oc_a_c = m.opportunity_cost(A_HOURS_CLOTH, A_HOURS_WINE)
        assert abs(oc_a_w * oc_a_c - 1.0) < 1e-9
        oc_b_w = m.opportunity_cost(B_HOURS_WINE, B_HOURS_CLOTH)
        oc_b_c = m.opportunity_cost(B_HOURS_CLOTH, B_HOURS_WINE)
        assert abs(oc_b_w * oc_b_c - 1.0) < 1e-9
