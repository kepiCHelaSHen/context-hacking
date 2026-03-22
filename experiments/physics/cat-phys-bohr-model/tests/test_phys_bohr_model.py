"""cat-phys-bohr-model — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_bohr_model_constants import *
IMPL = Path(__file__).parent.parent / "phys_bohr_model.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_energy_negative(self):
        mod = _import_impl()
        for n in [1, 2, 3]:
            assert mod.energy_level(n) < 0
    def test_energy_n_squared(self):
        mod = _import_impl()
        E1 = mod.energy_level(1)
        E2 = mod.energy_level(2)
        assert abs(E2 / E1 - 1/4) < 0.001
    def test_rydberg_precise(self):
        assert R_INF != 1.097e7
        assert abs(R_INF - 1.0973731568160e7) < 1e3
class TestCorrectness:
    def test_h_alpha(self):
        mod = _import_impl()
        lam = mod.transition_wavelength(3, 2)
        assert abs(lam * 1e9 - 656.3) < 0.5
    def test_lyman_alpha(self):
        mod = _import_impl()
        lam = mod.transition_wavelength(2, 1)
        assert abs(lam * 1e9 - 121.6) < 0.5
    def test_ionization_energy(self):
        mod = _import_impl()
        assert abs(mod.energy_level(1) + RY_EV) < 0.001
