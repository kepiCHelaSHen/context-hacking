"""cat-phys-diffraction — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_diffraction_constants import *
IMPL = Path(__file__).parent.parent / "phys_diffraction.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_single_slit_first_min(self):
        m = _i(); theta = m.single_slit_minima(A_SLIT, LAMBDA_HENE, 1)
        assert abs(theta - THETA_FIRST_MIN) < 1e-5
    def test_rayleigh_has_1_22(self):
        m = _i(); theta = m.rayleigh_criterion(LAMBDA_HENE, D_APERTURE)
        assert abs(theta - THETA_RAYLEIGH) / THETA_RAYLEIGH < 0.001
class TestCorrectness:
    def test_double_slit_first_max(self):
        m = _i(); theta = m.double_slit_maxima(D_SLITS, LAMBDA_HENE, 1)
        assert abs(theta - THETA_FIRST_MAX) < 1e-5
