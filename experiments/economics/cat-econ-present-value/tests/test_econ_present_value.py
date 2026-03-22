"""econ-present-value -- Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from econ_present_value_constants import *

IMPL = Path(__file__).parent.parent / "econ_present_value.py"


def _import_impl():
    if not IMPL.exists():
        pytest.skip("implementation not yet written")
    import importlib.util
    spec = importlib.util.spec_from_file_location("impl", IMPL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class TestPriorErrors:
    """Each test catches one known LLM prior error."""

    def test_discrete_not_continuous(self):
        """PRIOR_ERROR: continuous_discrete_swap
        Discrete PV must use (1+r)^n, NOT e^(-rn)."""
        mod = _import_impl()
        pv = mod.pv_discrete(TEST_FV, TEST_RATE, TEST_N)
        # Continuous would give 606.53; discrete must give 620.92
        assert abs(pv - DISCRETE_PV) < 0.01, (
            f"pv_discrete returned {pv:.2f}, expected {DISCRETE_PV:.2f} "
            f"-- got continuous result?"
        )

    def test_continuous_not_discrete(self):
        """PRIOR_ERROR: continuous_discrete_swap (reverse direction)
        Continuous PV must use e^(-rn), NOT 1/(1+r)^n."""
        mod = _import_impl()
        pv = mod.pv_continuous(TEST_FV, TEST_RATE, TEST_N)
        # Discrete would give 620.92; continuous must give 606.53
        assert abs(pv - CONTINUOUS_PV) < 0.01, (
            f"pv_continuous returned {pv:.2f}, expected {CONTINUOUS_PV:.2f} "
            f"-- got discrete result?"
        )

    def test_annuity_not_perpetuity(self):
        """PRIOR_ERROR: annuity_perpetuity
        Finite annuity must use [1-(1+r)^(-n)]/r, NOT just 1/r."""
        mod = _import_impl()
        pv = mod.annuity_pv(TEST_PMT, TEST_RATE, TEST_N)
        # Perpetuity would give 1000; annuity must give 379.08
        assert abs(pv - ANNUITY_PV) < 0.01, (
            f"annuity_pv returned {pv:.2f}, expected {ANNUITY_PV:.2f} "
            f"-- used perpetuity formula?"
        )

    def test_npv_includes_initial_cost(self):
        """PRIOR_ERROR: npv_no_initial
        NPV must include C0 (cashflows[0]); forgetting it inflates NPV by |C0|."""
        mod = _import_impl()
        result = mod.npv(TEST_CASHFLOWS, TEST_RATE)
        # Without C0 the result would be ~568.62; correct is ~68.62
        assert abs(result - NPV_EXPECTED) < 0.01, (
            f"npv returned {result:.2f}, expected {NPV_EXPECTED:.2f} "
            f"-- forgot to include C0?"
        )


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_discrete_pv_value(self):
        mod = _import_impl()
        pv = mod.pv_discrete(TEST_FV, TEST_RATE, TEST_N)
        assert abs(pv - DISCRETE_PV) < 0.01

    def test_continuous_pv_value(self):
        mod = _import_impl()
        pv = mod.pv_continuous(TEST_FV, TEST_RATE, TEST_N)
        assert abs(pv - CONTINUOUS_PV) < 0.01

    def test_discrete_greater_than_continuous(self):
        """For same nominal r, discrete PV > continuous PV."""
        mod = _import_impl()
        d = mod.pv_discrete(TEST_FV, TEST_RATE, TEST_N)
        c = mod.pv_continuous(TEST_FV, TEST_RATE, TEST_N)
        assert d > c, "Discrete PV should exceed continuous PV for same nominal rate"

    def test_annuity_less_than_perpetuity(self):
        """Finite annuity PV must be less than perpetuity PV."""
        mod = _import_impl()
        ann = mod.annuity_pv(TEST_PMT, TEST_RATE, TEST_N)
        perp = mod.perpetuity_pv(TEST_PMT, TEST_RATE)
        assert ann < perp, "Annuity PV must be < perpetuity PV for finite n"

    def test_perpetuity_pv_value(self):
        mod = _import_impl()
        pv = mod.perpetuity_pv(TEST_PMT, TEST_RATE)
        assert abs(pv - PERPETUITY_PV) < 0.01
