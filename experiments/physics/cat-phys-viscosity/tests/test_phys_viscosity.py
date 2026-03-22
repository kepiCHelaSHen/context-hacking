"""cat-phys-viscosity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_viscosity_constants import *
IMPL = Path(__file__).parent.parent / "phys_viscosity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_stokes_uses_radius(self):
        m = _i(); F = m.stokes_drag(MU_WATER, 0.001, 1.0)
        expected = 6 * math.pi * MU_WATER * 0.001 * 1.0
        assert abs(F - expected) < 1e-10
    def test_reynolds_uses_diameter(self):
        m = _i(); Re = m.reynolds_number(RHO_WATER, 1.0, 0.002, MU_WATER)
        assert Re > 1000  # high Re
class TestCorrectness:
    def test_terminal_velocity(self):
        m = _i(); vt = m.terminal_velocity(R_TEST, RHO_STEEL, RHO_WATER, MU_WATER)
        assert abs(vt - V_TERMINAL) / V_TERMINAL < 0.01
