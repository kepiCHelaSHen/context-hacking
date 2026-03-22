"""cat-econ-elasticity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_elasticity_constants import *
IMPL = Path(__file__).parent.parent / "econ_elasticity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that specifically catch known LLM errors."""

    def test_ped_is_negative(self):
        """PRIOR: ped_positive — PED must be negative for normal goods."""
        m = _i()
        ped = m.price_elasticity_midpoint(P1, Q1, P2, Q2)
        assert ped < 0, f"PED should be NEGATIVE for normal goods, got {ped}"

    def test_elastic_means_abs_gt_1(self):
        """PRIOR: elastic_less_than_1 — elastic requires |PED| > 1."""
        m = _i()
        assert m.classify_elasticity(-1.5) == "elastic"
        assert m.classify_elasticity(-0.5) == "inelastic"
        assert m.classify_elasticity(-1.0) == "unit elastic"

    def test_midpoint_not_endpoint(self):
        """PRIOR: midpoint_wrong — must use midpoint averages, not P1/Q1."""
        m = _i()
        ped = m.price_elasticity_midpoint(P1, Q1, P2, Q2)
        # Endpoint method would give: (-20/100)/(2/10) = -0.2/0.2 = -1.0
        endpoint_ped = ((Q2 - Q1) / Q1) / ((P2 - P1) / P1)
        assert abs(ped - endpoint_ped) > 0.01, "Appears to use endpoint method, not midpoint"


class TestCorrectness:
    """Numerical verification against frozen constants."""

    def test_ped_value(self):
        m = _i()
        ped = m.price_elasticity_midpoint(P1, Q1, P2, Q2)
        assert abs(ped - PED_TEST) < 1e-9, f"Expected {PED_TEST}, got {ped}"

    def test_ped_exact_rational(self):
        m = _i()
        ped = m.price_elasticity_midpoint(P1, Q1, P2, Q2)
        expected = PED_EXACT_NUMER / PED_EXACT_DENOM
        assert abs(ped - expected) < 1e-12

    def test_ped_classification(self):
        m = _i()
        ped = m.price_elasticity_midpoint(P1, Q1, P2, Q2)
        assert m.classify_elasticity(ped) == PED_CLASSIFICATION

    def test_income_elasticity(self):
        m = _i()
        yed = m.income_elasticity(QY1, QY2, Y1, Y2)
        assert abs(yed - YED_TEST) < 1e-9, f"Expected {YED_TEST}, got {yed}"

    def test_income_positive_normal_good(self):
        m = _i()
        yed = m.income_elasticity(QY1, QY2, Y1, Y2)
        assert yed > 0, "Income elasticity should be positive for normal goods"

    def test_cross_elasticity(self):
        m = _i()
        xed = m.cross_elasticity(QA1, QA2, PB1, PB2)
        assert abs(xed - XED_TEST) < 1e-9, f"Expected {XED_TEST}, got {xed}"

    def test_cross_positive_substitutes(self):
        m = _i()
        xed = m.cross_elasticity(QA1, QA2, PB1, PB2)
        assert xed > 0, "Cross-price elasticity should be positive for substitutes"

    def test_classify_edge_cases(self):
        m = _i()
        assert m.classify_elasticity(0.0) == "inelastic"
        assert m.classify_elasticity(-100.0) == "elastic"
        assert m.classify_elasticity(1.0) == "unit elastic"
        assert m.classify_elasticity(-1.0) == "unit elastic"
