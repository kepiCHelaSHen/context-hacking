"""cat-eng-ohm-kirchhoff — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from eng_ohm_kirchhoff_constants import *
IMPL = Path(__file__).parent.parent / "eng_ohm_kirchhoff.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_kvl_signs_correct(self):
        """KVL loop must sum to zero — catches 'all positive' bug."""
        m = _i()
        I = m.ohms_law_current(V_SOURCE, m.series_resistance(R1, R2, R3))
        voltages = [V_SOURCE, -I*R1, -I*R2, -I*R3]
        assert m.kvl_check(voltages)
    def test_kcl_node_balance(self):
        """Currents into a node must equal currents out."""
        m = _i()
        V = 12.0; I_total = m.ohms_law_current(V, m.parallel_resistance(R_A, R_B))
        I_a = V / R_A; I_b = V / R_B
        assert abs(I_total - I_a - I_b) < 1e-9
    def test_parallel_not_direct_sum(self):
        """Parallel R must be LESS than smallest branch."""
        m = _i(); Rp = m.parallel_resistance(R_A, R_B)
        assert Rp < min(R_A, R_B)

class TestCorrectness:
    def test_series_resistance(self):
        m = _i(); assert abs(m.series_resistance(R1, R2, R3) - R_SERIES) < 1e-9
    def test_parallel_resistance(self):
        m = _i(); assert abs(m.parallel_resistance(R_A, R_B) - R_PARALLEL) < 1e-9
    def test_ohms_law(self):
        m = _i(); assert abs(m.ohms_law_current(V_SOURCE, R_SERIES) - I_SERIES) < 1e-9
    def test_voltage_divider(self):
        m = _i(); assert abs(m.voltage_divider(V_DIV_IN, R_DIV1, R_DIV2) - V_DIV_OUT) < 1e-9
    def test_kvl_sum_zero(self):
        m = _i(); assert abs(KVL_SUM) < 1e-9
