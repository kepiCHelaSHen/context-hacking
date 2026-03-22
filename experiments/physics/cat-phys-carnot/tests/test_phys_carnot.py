"""cat-phys-carnot — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_carnot_constants import *
IMPL = Path(__file__).parent.parent / "phys_carnot.py"
def _import_impl():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; spec = importlib.util.spec_from_file_location("impl", IMPL); mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod); return mod

class TestPriorErrors:
    def test_uses_kelvin(self):
        mod = _import_impl()
        eta = mod.carnot_efficiency(TH_TEST, TC_TEST)
        assert abs(eta - ETA_CARNOT) < 0.001
    def test_cop_can_exceed_1(self):
        mod = _import_impl()
        cop = mod.cop_heat_pump(TH_TEST, TC_TEST)
        assert cop > 1.0
    def test_cop_hp_equals_ref_plus_1(self):
        mod = _import_impl()
        assert abs(mod.cop_heat_pump(TH_TEST, TC_TEST) - mod.cop_refrigerator(TH_TEST, TC_TEST) - 1.0) < 0.001
class TestCorrectness:
    def test_efficiency_value(self):
        mod = _import_impl()
        assert abs(mod.carnot_efficiency(TH_TEST, TC_TEST) - 0.40) < 0.001
    def test_cop_values(self):
        mod = _import_impl()
        assert abs(mod.cop_heat_pump(TH_TEST, TC_TEST) - COP_HP) < 0.01
        assert abs(mod.cop_refrigerator(TH_TEST, TC_TEST) - COP_REF) < 0.01
