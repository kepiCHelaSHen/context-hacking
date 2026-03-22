"""cat-econ-bond-pricing — Sigma Gate Tests"""
import sys
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_bond_pricing_constants import *

IMPL = Path(__file__).parent.parent / "econ_bond_pricing.py"


def _i():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Prior-Error Guards ──────────────────────────────────────────────


class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_semi_annual_not_annual(self):
        """PRIOR: annual_not_semi — must use m=2 for US bonds, not m=1."""
        mod = _i()
        P = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        # Annual convention gives 920.1458 — must NOT match that
        assert abs(P - BOND_PRICE_ANNUAL_WRONG) > 0.50, (
            f"Price {P:.4f} matches annual convention {BOND_PRICE_ANNUAL_WRONG} — "
            "must use semi-annual (m=2) for US bonds"
        )
        # Must match the correct semi-annual price
        assert abs(P - BOND_PRICE_SEMI) < 0.01, (
            f"Price {P:.4f} != {BOND_PRICE_SEMI}: semi-annual bond price wrong"
        )

    def test_ytm_halved_per_period(self):
        """PRIOR: ytm_not_halved — yield per period must be ytm/m, not ytm."""
        mod = _i()
        P = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        # Using full YTM per period gives 664.4959 — must NOT match that
        assert abs(P - BOND_PRICE_YTM_WRONG) > 1.0, (
            f"Price {P:.4f} matches ytm-not-halved result {BOND_PRICE_YTM_WRONG} — "
            "must divide YTM by m for per-period yield"
        )

    def test_duration_discounts_cash_flows(self):
        """PRIOR: duration_no_discount — Macaulay duration must discount CF_t."""
        mod = _i()
        D = mod.macaulay_duration(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        # Without discounting, duration = 6.3392 years (WRONG)
        assert abs(D - MACAULAY_DURATION_NO_DISCOUNT_WRONG) > 0.50, (
            f"Duration {D:.4f} matches undiscounted result "
            f"{MACAULAY_DURATION_NO_DISCOUNT_WRONG} — must discount cash flows"
        )
        # Must match the correct duration
        assert abs(D - MACAULAY_DURATION_YEARS) < 0.01, (
            f"Duration {D:.4f} != {MACAULAY_DURATION_YEARS}: Macaulay duration wrong"
        )


# ── Correctness Tests ───────────────────────────────────────────────


class TestCorrectness:
    """Verify results against frozen spec values."""

    def test_coupon_per_period(self):
        mod = _i()
        C = mod.coupon_per_period(FACE_VALUE, COUPON_RATE, M)
        assert abs(C - COUPON_PER_PERIOD) < 1e-9, (
            f"Coupon/period={C}, expected {COUPON_PER_PERIOD}"
        )

    def test_bond_price_semi_annual(self):
        mod = _i()
        P = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        assert abs(P - BOND_PRICE_SEMI) < 0.01, (
            f"Price={P:.4f}, expected {BOND_PRICE_SEMI}"
        )

    def test_bond_price_annual_differs(self):
        """Annual price must differ from semi-annual price."""
        mod = _i()
        P_semi = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=2)
        P_annual = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=1)
        assert abs(P_semi - P_annual) > 0.50, (
            "Semi-annual and annual prices should differ"
        )

    def test_bond_price_at_par(self):
        """When coupon rate == YTM, bond should trade at par."""
        mod = _i()
        P = mod.bond_price(1000, 0.08, 0.08, 10, m=2)
        assert abs(P - 1000.0) < 0.01, (
            f"At-par bond price={P:.4f}, expected 1000.00"
        )

    def test_bond_price_premium_discount(self):
        """Coupon > YTM => premium; coupon < YTM => discount."""
        mod = _i()
        P_premium = mod.bond_price(1000, 0.10, 0.08, 5, m=2)
        P_discount = mod.bond_price(1000, 0.06, 0.08, 5, m=2)
        assert P_premium > 1000, "Coupon > YTM should give premium bond"
        assert P_discount < 1000, "Coupon < YTM should give discount bond"

    def test_macaulay_duration_value(self):
        mod = _i()
        D = mod.macaulay_duration(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        assert abs(D - MACAULAY_DURATION_YEARS) < 0.01, (
            f"Duration={D:.4f}, expected {MACAULAY_DURATION_YEARS}"
        )

    def test_duration_less_than_maturity(self):
        """For coupon bond, Macaulay duration < maturity."""
        mod = _i()
        D = mod.macaulay_duration(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        assert D < YEARS, (
            f"Duration {D:.4f} >= maturity {YEARS}: impossible for coupon bond"
        )

    def test_duration_positive(self):
        mod = _i()
        D = mod.macaulay_duration(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        assert D > 0, "Duration must be positive"

    def test_current_yield_value(self):
        mod = _i()
        P = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        cy = mod.current_yield(FACE_VALUE, COUPON_RATE, P)
        assert abs(cy - CURRENT_YIELD) < 0.0001, (
            f"Current yield={cy:.6f}, expected {CURRENT_YIELD}"
        )

    def test_current_yield_between_coupon_and_ytm(self):
        """For discount bond: coupon_rate < current_yield < YTM."""
        mod = _i()
        P = mod.bond_price(FACE_VALUE, COUPON_RATE, YTM, YEARS, m=M)
        cy = mod.current_yield(FACE_VALUE, COUPON_RATE, P)
        assert COUPON_RATE < cy < YTM, (
            f"For discount bond, should have {COUPON_RATE} < {cy:.6f} < {YTM}"
        )
