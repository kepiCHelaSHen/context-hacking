"""cat-phys-compton — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_compton_constants import *
IMPL = Path(__file__).parent.parent / "phys_compton.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_uses_1_minus_cos(self):
        mod = _import_impl()
        shift = mod.compton_shift(90)
        assert abs(shift - SHIFT_90DEG) < 1e-15
    def test_zero_at_forward(self):
        mod = _import_impl()
        assert mod.compton_shift(0) < 1e-20
    def test_max_at_180(self):
        mod = _import_impl()
        assert abs(mod.compton_shift(180) - MAX_SHIFT) < 1e-15
class TestCorrectness:
    def test_shift_60deg(self):
        mod = _import_impl()
        shift = mod.compton_shift(60)
        assert abs(shift - SHIFT_60DEG) / SHIFT_60DEG < 0.001
    def test_wavelength_not_rounded(self):
        assert abs(COMPTON_WAVELENGTH - 2.4263e-12) < 1e-15
