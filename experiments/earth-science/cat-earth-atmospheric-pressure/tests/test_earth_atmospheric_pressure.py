"""cat-earth-atmospheric-pressure — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_atmospheric_pressure_constants import *
IMPL = Path(__file__).parent.parent / "earth_atmospheric_pressure.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_scale_height_not_8000(self):
        """LLM trap: H must be ~8434.78, not the common 8000 approximation."""
        m = _i(); H = m.scale_height(T_STD, M_AIR, G_STD)
        assert abs(H - 8000) > 100, "Scale height should NOT be 8000"
        assert abs(H - H_SCALE) < 1.0
    def test_scale_height_not_10000(self):
        """LLM trap: H must be ~8434.78, not 10000."""
        m = _i(); H = m.scale_height(T_STD, M_AIR, G_STD)
        assert abs(H - 10000) > 1000, "Scale height should NOT be 10000"
    def test_uses_exponential_not_linear(self):
        """LLM trap: P = P₀·exp(−h/H), NOT P₀·(1−h/H)."""
        m = _i()
        P_exp = m.barometric_pressure(P0, 5500, H_SCALE)
        P_linear = P0 * (1 - 5500 / H_SCALE)  # wrong formula
        assert abs(P_exp - P_5500) < 1.0
        assert abs(P_exp - P_linear) > 500, "Should differ significantly from linear approx"
    def test_gas_constant_precise(self):
        """LLM trap: must use R=8.314462, not rounded 8.314."""
        assert R_GAS != 8.314
        assert abs(R_GAS - 8.314462) < 1e-6

class TestCorrectness:
    def test_scale_height_value(self):
        m = _i(); H = m.scale_height(T_STD, M_AIR, G_STD)
        assert abs(H - H_SCALE) < 0.1
    def test_pressure_at_5500m(self):
        m = _i(); P = m.barometric_pressure(P0, 5500, H_SCALE)
        assert abs(P - P_5500) < 1.0
    def test_pressure_at_everest(self):
        m = _i(); P = m.barometric_pressure(P0, 8848, H_SCALE)
        assert abs(P - P_EVEREST) < 1.0
    def test_altitude_roundtrip(self):
        m = _i(); h = m.altitude_from_pressure(P_5500, P0, H_SCALE)
        assert abs(h - 5500) < 0.1
    def test_pressure_ratio_sea_level(self):
        m = _i(); r = m.pressure_ratio(0, H_SCALE)
        assert abs(r - 1.0) < 1e-10
    def test_pressure_ratio_at_H(self):
        m = _i(); r = m.pressure_ratio(H_SCALE, H_SCALE)
        assert abs(r - 1/math.e) < 1e-6
