"""cat-phys-magnetic-force — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_magnetic_force_constants import *
IMPL = Path(__file__).parent.parent / "phys_magnetic_force.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_no_force_parallel(self):
        m = _i(); F = m.lorentz_force(E_CHARGE, 1e6, 1.0, 0)
        assert F < 1e-30  # zero when v parallel B
    def test_cyclotron_freq_independent_of_v(self):
        m = _i()
        f1 = m.cyclotron_frequency(E_CHARGE, 1.0, M_PROTON)
        f2 = m.cyclotron_frequency(E_CHARGE, 1.0, M_PROTON)  # same regardless of v
        assert f1 == f2
class TestCorrectness:
    def test_proton_force(self):
        m = _i(); F = m.lorentz_force(E_CHARGE, 1e6, 1.0)
        assert abs(F - F_PROTON) / F_PROTON < 0.001
    def test_proton_radius(self):
        m = _i(); r = m.cyclotron_radius(M_PROTON, 1e6, E_CHARGE, 1.0)
        assert abs(r - R_PROTON) / R_PROTON < 0.001
