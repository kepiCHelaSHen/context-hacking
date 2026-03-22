"""chem-spectrophotometry — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_spectrophotometry_constants import *

IMPL = Path(__file__).parent.parent / "chem_spectrophotometry.py"


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

    def test_uses_log10_not_ln(self):
        mod = _import_impl()
        assert abs(mod.absorbance_from_T(0.01) - 2.0) < 0.001

    def test_sign_correct(self):
        mod = _import_impl()
        A = mod.absorbance_from_T(0.5)
        assert A > 0

    def test_path_length_doubles_absorbance(self):
        mod = _import_impl()
        A1 = mod.absorbance(0.001, 2360, 1.0)
        A2 = mod.absorbance(0.001, 2360, 2.0)
        assert abs(A2 / A1 - 2.0) < 0.001

    def test_dna_not_rna_factor(self):
        mod = _import_impl()
        assert mod.dna_conc(1.0, "dsDNA") == 50.0


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_T1_gives_A0(self):
        mod = _import_impl()
        assert abs(mod.absorbance_from_T(1.0)) < 0.001

    def test_roundtrip(self):
        mod = _import_impl()
        A = 1.5
        T = mod.T_from_absorbance(A)
        A_back = mod.absorbance_from_T(T)
        assert abs(A_back - A) < 0.001

    def test_percent_T_conversion(self):
        mod = _import_impl()
        A = mod.percent_T_to_A(10.0)
        assert abs(A - 1.0) < 0.001
