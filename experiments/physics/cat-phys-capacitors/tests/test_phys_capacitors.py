"""cat-phys-capacitors — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_capacitors_constants import *
IMPL = Path(__file__).parent.parent / "phys_capacitors.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_series_less_than_smallest(self):
        m = _i(); Cs = m.series_capacitance(C1, C2, C3)
        assert Cs < min(C1, C2, C3)
    def test_parallel_is_sum(self):
        m = _i(); Cp = m.parallel_capacitance(C1, C2, C3)
        assert abs(Cp - C_PARALLEL) < 1e-10
    def test_energy_has_half(self):
        m = _i(); U = m.energy(100e-6, 12.0)
        assert abs(U - U_TEST) < 1e-6
class TestCorrectness:
    def test_series_value(self):
        m = _i(); Cs = m.series_capacitance(C1, C2, C3)
        assert abs(Cs - C_SERIES) < 1e-9
    def test_charge(self):
        m = _i(); Q = m.charge(100e-6, 12.0)
        assert abs(Q - Q_TEST) < 1e-7
