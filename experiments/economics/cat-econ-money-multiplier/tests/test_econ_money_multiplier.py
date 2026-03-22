"""cat-econ-money-multiplier — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_money_multiplier_constants import *
IMPL = Path(__file__).parent.parent / "econ_money_multiplier.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that specifically catch known LLM errors."""

    def test_multiplier_is_1_over_rr_not_1_over_1_minus_rr(self):
        """PRIOR: multiplier_1_minus_rr — must use 1/rr, NOT 1/(1-rr)."""
        m = _i()
        result = m.simple_multiplier(RR)
        wrong = 1.0 / (1.0 - RR)  # 1.1111 — fiscal multiplier formula
        assert abs(result - wrong) > 1.0, (
            f"Got {result:.4f}, which is close to WRONG formula 1/(1-rr)={wrong:.4f}"
        )
        assert abs(result - SIMPLE_MULTIPLIER) < 1e-9, (
            f"Expected 1/rr = {SIMPLE_MULTIPLIER}, got {result}"
        )

    def test_extended_multiplier_uses_currency_drain(self):
        """PRIOR: no_currency_drain — must account for cr in extended model."""
        m = _i()
        result = m.extended_multiplier(RR, CR)
        simple = m.simple_multiplier(RR)
        assert result < simple, (
            f"Extended multiplier ({result}) should be < simple ({simple}) when cr > 0"
        )
        assert abs(result - EXTENDED_MULTIPLIER) < 1e-9, (
            f"Expected (1+cr)/(rr+cr) = {EXTENDED_MULTIPLIER}, got {result}"
        )

    def test_reserve_ratio_not_zero(self):
        """PRIOR: reserves_lent_fully — rr=0 should be rejected, not produce infinity."""
        m = _i()
        with pytest.raises((ValueError, ZeroDivisionError)):
            m.simple_multiplier(0.0)


class TestCorrectness:
    """Numerical verification against frozen constants."""

    def test_simple_multiplier_value(self):
        m = _i()
        result = m.simple_multiplier(RR)
        assert abs(result - SIMPLE_MULTIPLIER) < 1e-9, (
            f"Expected {SIMPLE_MULTIPLIER}, got {result}"
        )

    def test_simple_multiplier_exact(self):
        """1/0.10 must equal exactly 10.0."""
        m = _i()
        result = m.simple_multiplier(RR)
        assert result == 10.0

    def test_extended_multiplier_value(self):
        m = _i()
        result = m.extended_multiplier(RR, CR)
        assert abs(result - EXTENDED_MULTIPLIER) < 1e-9, (
            f"Expected {EXTENDED_MULTIPLIER}, got {result}"
        )

    def test_extended_multiplier_exact_rational(self):
        m = _i()
        result = m.extended_multiplier(RR, CR)
        expected = EXTENDED_EXACT_NUMER / EXTENDED_EXACT_DENOM
        assert abs(result - expected) < 1e-12

    def test_total_deposits(self):
        m = _i()
        result = m.total_deposits(INITIAL_DEPOSIT, RR)
        assert abs(result - TOTAL_DEPOSITS) < 1e-9, (
            f"Expected {TOTAL_DEPOSITS}, got {result}"
        )

    def test_total_reserves_equals_initial_deposit(self):
        """Total reserves must equal initial deposit (conservation of base money)."""
        m = _i()
        td = m.total_deposits(INITIAL_DEPOSIT, RR)
        tr = m.total_reserves(td, RR)
        assert abs(tr - INITIAL_DEPOSIT) < 1e-9, (
            f"Total reserves ({tr}) should equal initial deposit ({INITIAL_DEPOSIT})"
        )

    def test_money_supply_simple(self):
        m = _i()
        mult = m.simple_multiplier(RR)
        ms = m.money_supply(MB, mult)
        assert abs(ms - MONEY_SUPPLY_SIMPLE) < 1e-9, (
            f"Expected {MONEY_SUPPLY_SIMPLE}, got {ms}"
        )

    def test_money_supply_extended(self):
        m = _i()
        mult = m.extended_multiplier(RR, CR)
        ms = m.money_supply(MB, mult)
        assert abs(ms - MONEY_SUPPLY_EXTENDED) < 1e-9, (
            f"Expected {MONEY_SUPPLY_EXTENDED}, got {ms}"
        )

    def test_extended_cr_zero_equals_simple(self):
        """When cr=0, extended formula (1+0)/(rr+0) = 1/rr = simple."""
        m = _i()
        ext = m.extended_multiplier(RR, 0.0)
        simp = m.simple_multiplier(RR)
        assert abs(ext - simp) < 1e-12

    def test_various_reserve_ratios(self):
        """Verify multiplier for several standard reserve ratios."""
        m = _i()
        cases = [
            (0.05, 20.0),
            (0.10, 10.0),
            (0.20,  5.0),
            (0.25,  4.0),
            (0.50,  2.0),
            (1.00,  1.0),
        ]
        for rr, expected in cases:
            result = m.simple_multiplier(rr)
            assert abs(result - expected) < 1e-9, (
                f"rr={rr}: expected {expected}, got {result}"
            )
