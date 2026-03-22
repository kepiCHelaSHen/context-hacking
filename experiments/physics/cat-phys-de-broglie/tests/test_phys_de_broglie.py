"""cat-phys-de-broglie — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_de_broglie_constants import *
IMPL = Path(__file__).parent.parent / "phys_de_broglie.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_heavier_particle_shorter_wavelength(self):
        mod = _import_impl()
        lam_e = mod.wavelength_from_voltage(M_ELECTRON, E_CHARGE, 100)
        lam_p = mod.wavelength_from_voltage(M_PROTON, E_CHARGE, 100)
        assert lam_e > lam_p
    def test_100eV_not_relativistic(self):
        mod = _import_impl()
        assert not mod.is_relativistic(M_ELECTRON, 100 * E_CHARGE)
class TestCorrectness:
    def test_electron_100V(self):
        mod = _import_impl()
        lam = mod.wavelength_from_voltage(M_ELECTRON, E_CHARGE, 100)
        assert abs(lam - LAMBDA_100EV) / LAMBDA_100EV < 0.001
    def test_wavelength_roundtrip(self):
        mod = _import_impl()
        v = V_ELECTRON_100EV
        lam = mod.de_broglie_wavelength(M_ELECTRON, v)
        assert abs(lam - LAMBDA_100EV) / LAMBDA_100EV < 0.001
