"""chem-vdw-gas — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_vdw_gas_constants import *

IMPL = Path(__file__).parent.parent / "chem_vdw_gas.py"


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

    def test_co2_vdw_differs_from_ideal(self):
        mod = _import_impl()
        ideal = mod.ideal_gas_P(1, 0.5, 500)
        vdw = mod.vdw_P(1, 0.5, 500, "CO2")
        deviation = abs(ideal - vdw) / ideal
        assert deviation > 0.05

    def test_critical_T_has_8_over_27(self):
        mod = _import_impl()
        Tc = mod.critical_temperature("CO2")
        assert abs(Tc - 304.2) < 5

    def test_n_squared_in_attraction(self):
        mod = _import_impl()
        P1 = mod.vdw_P(1, 1.0, 300, "CO2")
        P2 = mod.vdw_P(2, 2.0, 300, "CO2")
        assert abs(P1 - P2) / P1 < 0.01


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_h2_nearly_ideal(self):
        mod = _import_impl()
        ideal = mod.ideal_gas_P(1, 22.4, 273.15)
        vdw = mod.vdw_P(1, 22.4, 273.15, "H2")
        assert abs(ideal - vdw) / ideal < 0.01

    def test_compression_factor_ideal(self):
        mod = _import_impl()
        P = mod.ideal_gas_P(1, 22.4, 273.15)
        Z = mod.compression_factor(P, 22.4, 1, 273.15)
        assert abs(Z - 1.0) < 0.001
