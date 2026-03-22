"""cat-phys-bernoulli — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_bernoulli_constants import *
IMPL = Path(__file__).parent.parent / "phys_bernoulli.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_continuity(self):
        m = _i(); v2 = m.continuity_v2(V1_TEST, A1_TEST, A2_TEST)
        assert abs(v2 - V2_TEST) < 0.01
    def test_pressure_drops_at_constriction(self):
        m = _i(); dp = m.bernoulli_pressure_drop(RHO_WATER, V1_TEST, V2_TEST)
        assert dp > 0
class TestCorrectness:
    def test_pressure_drop_value(self):
        m = _i(); dp = m.bernoulli_pressure_drop(RHO_WATER, V1_TEST, V2_TEST)
        assert abs(dp - DP_TEST) < 1.0
    def test_torricelli(self):
        m = _i(); assert abs(m.torricelli(1.0) - V_TORRICELLI_1M) < 0.01
