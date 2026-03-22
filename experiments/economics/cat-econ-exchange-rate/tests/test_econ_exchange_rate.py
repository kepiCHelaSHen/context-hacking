"""econ-exchange-rate — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_exchange_rate_constants import *

IMPL = Path(__file__).parent.parent / "econ_exchange_rate.py"


def _import_impl():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ── Prior-Error Tests ──────────────────────────────────────────────

class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_ppp_not_inverted(self):
        """PPP must be P_domestic/P_foreign, NOT P_foreign/P_domestic."""
        mod = _import_impl()
        rate = mod.ppp_rate(P_US, P_UK)
        # Correct: 120/100 = 1.20. Inverted would give 100/120 ≈ 0.833
        assert rate > 1.0, "PPP appears inverted (P_foreign/P_domestic)"
        assert abs(rate - PPP_RATE_USD_PER_GBP) < 0.001

    def test_higher_inflation_causes_depreciation(self):
        """Higher domestic inflation -> positive %ΔE (depreciation), NOT negative."""
        mod = _import_impl()
        pct = mod.relative_ppp(INFLATION_US, INFLATION_UK)
        # US has higher inflation -> $ should depreciate -> pct > 0
        assert pct > 0, "Higher domestic inflation should cause depreciation (positive %ΔE)"
        assert abs(pct - EXPECTED_PCT_CHANGE) < 0.001

    def test_irp_higher_interest_means_depreciation(self):
        """Higher domestic interest rate -> expected depreciation, NOT appreciation."""
        mod = _import_impl()
        change = mod.irp_expected_change(I_US, I_UK)
        # US has higher interest -> $ expected to depreciate -> change > 0
        assert change > 0, "Higher domestic interest rate should mean expected depreciation"
        assert abs(change - IRP_EXPECTED_CHANGE) < 0.001


# ── Correctness Tests ──────────────────────────────────────────────

class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_ppp_rate_exact(self):
        mod = _import_impl()
        rate = mod.ppp_rate(P_US, P_UK)
        assert abs(rate - PPP_RATE_USD_PER_GBP) < 1e-10

    def test_relative_ppp_exact(self):
        mod = _import_impl()
        pct = mod.relative_ppp(INFLATION_US, INFLATION_UK)
        assert abs(pct - EXPECTED_PCT_CHANGE) < 1e-10

    def test_expected_exchange_rate_exact(self):
        mod = _import_impl()
        E_next = mod.expected_exchange_rate(PPP_RATE_USD_PER_GBP, EXPECTED_PCT_CHANGE)
        assert abs(E_next - EXPECTED_NEXT_E) < 1e-10

    def test_real_exchange_rate_ppp_holds(self):
        """When PPP holds, real exchange rate = 1."""
        mod = _import_impl()
        q = mod.real_exchange_rate(PPP_RATE_USD_PER_GBP, P_UK, P_US)
        assert abs(q - REAL_EXCHANGE_RATE_PPP) < 1e-10

    def test_irp_expected_change_exact(self):
        mod = _import_impl()
        change = mod.irp_expected_change(I_US, I_UK)
        expected = (1 + I_US) / (1 + I_UK) - 1
        assert abs(change - expected) < 1e-10

    def test_ppp_symmetric_currencies(self):
        """Equal price levels -> E = 1 (no advantage either way)."""
        mod = _import_impl()
        rate = mod.ppp_rate(100, 100)
        assert abs(rate - 1.0) < 1e-10

    def test_relative_ppp_equal_inflation(self):
        """Equal inflation -> %ΔE = 0 (no change expected)."""
        mod = _import_impl()
        pct = mod.relative_ppp(0.02, 0.02)
        assert abs(pct) < 1e-10

    def test_irp_equal_interest_rates(self):
        """Equal interest rates -> no expected change."""
        mod = _import_impl()
        change = mod.irp_expected_change(0.05, 0.05)
        assert abs(change) < 1e-10

    def test_real_exchange_rate_overvalued(self):
        """When E < PPP rate, domestic currency is overvalued (q < 1)."""
        mod = _import_impl()
        # PPP says 1.20 but actual is 1.10 -> q = 1.10*100/120 ≈ 0.917
        q = mod.real_exchange_rate(1.10, P_UK, P_US)
        assert q < 1.0, "Domestic currency should be overvalued (q < 1)"
