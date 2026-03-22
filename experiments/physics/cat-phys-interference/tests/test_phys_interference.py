"""cat-phys-interference — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_interference_constants import *
IMPL = Path(__file__).parent.parent / "phys_interference.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_phase_change_higher_n(self):
        m = _i(); assert m.phase_change_at_reflection(1.0, N_OIL) == True
    def test_no_phase_change_lower_n(self):
        m = _i(); assert m.phase_change_at_reflection(N_OIL, N_WATER) == False
    def test_constructive_with_phase_change(self):
        m = _i(); visible = m.constructive_wavelengths(N_OIL, T_FILM)
        lambdas = [lam for _, lam in visible]
        assert any(abs(l - LAMBDA_CONSTRUCTIVE_M1) < 5e-9 for l in lambdas)
class TestCorrectness:
    def test_path_difference(self):
        m = _i(); pd = m.path_difference(N_OIL, T_FILM)
        assert abs(pd - 2 * N_OIL * T_FILM) < 1e-12
