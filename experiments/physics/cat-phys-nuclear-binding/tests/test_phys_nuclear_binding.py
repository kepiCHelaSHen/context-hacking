"""cat-phys-nuclear-binding — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_nuclear_binding_constants import *
IMPL = Path(__file__).parent.parent / "phys_nuclear_binding.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_binding_energy_positive(self):
        mod = _import_impl()
        BE = mod.binding_energy(26, 30, ATOMIC_MASS["Fe56"])
        assert BE > 0
    def test_fe56_highest_per_nucleon(self):
        mod = _import_impl()
        be_fe = mod.binding_energy_per_nucleon(26, 30, ATOMIC_MASS["Fe56"])
        be_he = mod.binding_energy_per_nucleon(2, 2, ATOMIC_MASS["He4"])
        assert be_fe > be_he
    def test_u_to_mev_precise(self):
        assert U_TO_MEV != 931
        assert U_TO_MEV != 931.5
        assert abs(U_TO_MEV - 931.494) < 0.001
class TestCorrectness:
    def test_fe56_be_per_nucleon(self):
        mod = _import_impl()
        be = mod.binding_energy_per_nucleon(26, 30, ATOMIC_MASS["Fe56"])
        assert abs(be - BE_PER_NUCLEON_FE56) < 0.1
    def test_he4_be(self):
        mod = _import_impl()
        be = mod.binding_energy(2, 2, ATOMIC_MASS["He4"])
        assert abs(be - BE_HE4) < 0.5
