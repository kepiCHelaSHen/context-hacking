"""chem-kinetics — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_kinetics_constants import *

IMPL = Path(__file__).parent.parent / "chem_kinetics.py"


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

    def test_ea_units_guard(self):
        mod = _import_impl()
        with pytest.raises(ValueError):
            mod.arrhenius_k(H2I2_A, 165.0, 700)

    def test_k_increases_with_T(self):
        mod = _import_impl()
        k600 = mod.arrhenius_k(H2I2_A, H2I2_Ea, 600)
        k800 = mod.arrhenius_k(H2I2_A, H2I2_Ea, 800)
        assert k800 > k600

    def test_ea_recovery_correct_sign(self):
        mod = _import_impl()
        k600 = mod.arrhenius_k(H2I2_A, H2I2_Ea, 600)
        k800 = mod.arrhenius_k(H2I2_A, H2I2_Ea, 800)
        Ea = mod.ea_from_two_temps(k600, 600, k800, 800)
        assert Ea > 0

    def test_second_order_differs_from_zero_order(self):
        mod = _import_impl()
        c_zero = mod.integrated_rate_law(1.0, 0.1, 5.0, 0)
        c_second = mod.integrated_rate_law(1.0, 0.1, 5.0, 2)
        assert abs(c_zero - c_second) > 0.01


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_k700_within_tolerance(self):
        mod = _import_impl()
        k = mod.arrhenius_k(H2I2_A, H2I2_Ea, 700)
        # Verify Arrhenius formula is correctly applied: k = A*exp(-Ea/RT)
        import math
        expected = H2I2_A * math.exp(-H2I2_Ea / (R * 700))
        assert abs(k - expected) / expected < 0.001
        # Verify k is positive and finite
        assert k > 0 and math.isfinite(k)

    def test_half_life_definition(self):
        mod = _import_impl()
        k = 0.05
        t_half = mod.half_life_first_order(k)
        C = mod.integrated_rate_law(1.0, k, t_half, 1)
        assert abs(C - 0.5) < 0.001
