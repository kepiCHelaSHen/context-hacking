"""cat-phys-photoelectric — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_photoelectric_constants import *
IMPL = Path(__file__).parent.parent / "phys_photoelectric.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_below_threshold_no_emission(self):
        mod = _import_impl()
        ke = mod.ke_max(600e-9, "Na")  # 600nm > threshold ~526nm
        assert ke < 0
    def test_above_threshold_emission(self):
        mod = _import_impl()
        ke = mod.ke_max(400e-9, "Na")
        assert ke > 0
    def test_work_function_precise(self):
        assert WORK_FUNCTION["Na"] == 2.36  # not rounded to 2.4
class TestCorrectness:
    def test_ke_max_na_400nm(self):
        mod = _import_impl()
        ke = mod.ke_max(400e-9, "Na")
        assert abs(ke - KE_MAX_NA_400NM) / KE_MAX_NA_400NM < 0.001
    def test_threshold_na(self):
        mod = _import_impl()
        lam = mod.threshold_wavelength("Na")
        assert abs(lam - LAMBDA_THRESHOLD_NA) / LAMBDA_THRESHOLD_NA < 0.001
