"""chem-crystal-packing — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from chem_crystal_packing_constants import *

IMPL = Path(__file__).parent.parent / "chem_crystal_packing.py"


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

    def test_fcc_4_atoms_not_8(self):
        mod = _import_impl()
        assert mod.atoms_per_cell("FCC") == 4

    def test_fcc_beats_bcc(self):
        mod = _import_impl()
        assert mod.packing_efficiency("FCC") > mod.packing_efficiency("BCC")

    def test_fcc_is_maximum(self):
        mod = _import_impl()
        for s in ["SC", "BCC", "diamond"]:
            assert mod.packing_efficiency(s) < mod.packing_efficiency("FCC")

    def test_fcc_packing_exact(self):
        mod = _import_impl()
        expected = math.pi / (3 * math.sqrt(2))
        assert abs(mod.packing_efficiency("FCC") - expected) < 1e-10


class TestCorrectness:
    """Each test verifies result against frozen spec."""

    def test_bcc_packing_exact(self):
        mod = _import_impl()
        expected = math.pi * math.sqrt(3) / 8
        assert abs(mod.packing_efficiency("BCC") - expected) < 0.0001

    def test_copper_density(self):
        mod = _import_impl()
        rho = mod.density("Cu", 63.546)
        assert abs(rho - 8.96) < 0.5
