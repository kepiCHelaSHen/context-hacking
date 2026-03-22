"""chem-electrochemistry — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_electrochemistry_constants import *

IMPL = Path(__file__).parent.parent / "chem_electrochemistry.py"


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

    def test_nernst_Q_gt_1_decreases_E(self):
        mod = _import_impl()
        E_Q1 = mod.nernst(1.0, 2, 1.0)
        E_Q10 = mod.nernst(1.0, 2, 10.0)
        assert E_Q10 < E_Q1

    def test_nernst_Q_lt_1_increases_E(self):
        mod = _import_impl()
        E_Q1 = mod.nernst(1.0, 2, 1.0)
        E_Q01 = mod.nernst(1.0, 2, 0.1)
        assert E_Q01 > E_Q1

    def test_delta_G_negative_spontaneous(self):
        mod = _import_impl()
        E0_cell = mod.cell_potential("Cu2+/Cu", "Zn2+/Zn")
        dG = mod.delta_G(E0_cell, 2)
        assert dG < 0

    def test_cell_cathode_minus_anode(self):
        mod = _import_impl()
        E = mod.cell_potential("Cu2+/Cu", "Zn2+/Zn")
        assert E > 0


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_daniell_cell(self):
        mod = _import_impl()
        E = mod.cell_potential("Cu2+/Cu", "Zn2+/Zn")
        assert abs(E - 1.1037) < 0.001

    def test_nernst_Q1_is_E0(self):
        mod = _import_impl()
        E = mod.nernst(1.1037, 2, 1.0)
        assert abs(E - 1.1037) < 0.001

    def test_SHE_is_zero(self):
        assert E0["H+/H2"] == 0.0
