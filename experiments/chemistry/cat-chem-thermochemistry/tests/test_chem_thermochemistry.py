"""chem-thermochemistry — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_thermochemistry_constants import *

IMPL = Path(__file__).parent.parent / "chem_thermochemistry.py"


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

    def test_hess_products_minus_reactants(self):
        mod = _import_impl()
        dH = mod.hess_law(
            [("H2O(l)", 1)],
            [("H2(g)", 1), ("O2(g)", 0.5)]
        )
        assert dH < 0

    def test_c2h4_positive(self):
        assert DHF["C2H4(g)"] > 0

    def test_no_positive(self):
        assert DHF["NO(g)"] > 0

    def test_h2o_gas_not_liquid(self):
        assert abs(DHF["H2O(g)"] - (-241.826)) < 0.01
        assert abs(DHF["H2O(g)"] - DHF["H2O(l)"]) > 40

    def test_bond_breaking_endothermic(self):
        mod = _import_impl()
        dH = mod.bond_enthalpy_dH([("H-H", 1)], [])
        assert dH > 0


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_water_formation(self):
        mod = _import_impl()
        dH = mod.hess_law(
            [("H2O(l)", 1)],
            [("H2(g)", 1), ("O2(g)", 0.5)]
        )
        assert abs(dH - (-285.830)) < 0.01

    def test_methane_combustion(self):
        mod = _import_impl()
        dH = mod.hess_law(
            [("CO2(g)", 1), ("H2O(l)", 2)],
            [("CH4(g)", 1), ("O2(g)", 2)]
        )
        assert -950 < dH < -830
