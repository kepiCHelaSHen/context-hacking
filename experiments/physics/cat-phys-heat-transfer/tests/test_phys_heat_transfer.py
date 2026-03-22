"""cat-phys-heat-transfer — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from phys_heat_transfer_constants import *
IMPL = Path(__file__).parent.parent / "phys_heat_transfer.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_radiation_uses_T4(self):
        m = _i(); q = m.radiation(1.0, 1.0, 500, 300)
        assert abs(q - Q_RAD_TEST) / Q_RAD_TEST < 0.001
    def test_radiation_needs_kelvin(self):
        m = _i()
        q_K = m.radiation(1.0, 1.0, 500, 300)
        q_C = m.radiation(1.0, 1.0, 227, 27)  # same temps in C — WRONG result
        assert q_K != q_C  # must use Kelvin
class TestCorrectness:
    def test_conduction(self):
        m = _i(); q = m.conduction(K_COPPER, 0.01, 400, 300, 0.1)
        assert abs(q - K_COPPER * 0.01 * 100 / 0.1) < 0.1
