"""cat-phys-faraday-induction — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_faraday_induction_constants import *
IMPL = Path(__file__).parent.parent / "phys_faraday_induction.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_lenz_sign(self):
        m = _i(); emf = m.faraday_emf(1, 1.0)  # positive dPhi/dt
        assert emf < 0  # Lenz's law: EMF opposes change
    def test_N_matters(self):
        m = _i()
        emf1 = m.emf_changing_B(1, A_COIL, B_INITIAL, B_FINAL, DT)
        emf100 = m.emf_changing_B(100, A_COIL, B_INITIAL, B_FINAL, DT)
        assert abs(emf100) == 100 * abs(emf1)
class TestCorrectness:
    def test_coil_emf(self):
        m = _i(); emf = m.emf_changing_B(N_COIL, A_COIL, B_INITIAL, B_FINAL, DT)
        assert abs(emf - EMF_TEST) < 0.1
    def test_motional_emf(self):
        m = _i(); emf = m.motional_emf(B_ROD, L_ROD, V_ROD)
        assert abs(emf - EMF_MOTIONAL) < 0.01
