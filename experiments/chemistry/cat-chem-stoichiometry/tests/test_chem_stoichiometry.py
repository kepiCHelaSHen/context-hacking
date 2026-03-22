"""chem-stoichiometry — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_stoichiometry_constants import *

IMPL = Path(__file__).parent.parent / "chem_stoichiometry.py"


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

    def test_water_not_integer_mw(self):
        mod = _import_impl()
        mw = mod.molecular_weight("H2O")
        assert abs(mw - 18.015) < 0.001
        assert mw != 18.0

    def test_glucose_mw(self):
        mod = _import_impl()
        mw = mod.molecular_weight("C6H12O6")
        assert abs(mw - 180.156) < 0.01

    def test_limiting_reagent_found(self):
        mod = _import_impl()
        reagents = {
            "H2": {"grams": 4.0, "stoich": 2},
            "O2": {"grams": 16.0, "stoich": 1},
        }
        limiting, ratio = mod.limiting_reagent(reagents)
        assert limiting == "O2"


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_formula_parsing(self):
        mod = _import_impl()
        parsed = mod.parse_formula("H2O")
        assert parsed == {"H": 2, "O": 1}

    def test_moles_roundtrip(self):
        mod = _import_impl()
        mass = 36.030
        mol = mod.moles(mass, "H2O")
        mass_back = mod.grams(mol, "H2O")
        assert abs(mass_back - mass) < 0.01

    def test_aspirin_MW(self):
        mod = _import_impl()
        mw = mod.molecular_weight("C9H8O4")
        assert abs(mw - 180.157) < 0.01
