"""cat-earth-lapse-rate — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_lapse_rate_constants import *
IMPL = Path(__file__).parent.parent / "earth_lapse_rate.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    """Guard against known LLM confusions about lapse rates."""

    def test_dalr_not_equal_malr(self):
        """Prior error: dry_moist_same — DALR != MALR."""
        m = _i()
        assert abs(m.dalr() - MALR_PER_KM) > 3.0, "DALR and MALR should differ by ~4°C/km"

    def test_dalr_is_not_env(self):
        """Prior error: env_is_dry — DALR (9.8) != environmental (6.5)."""
        m = _i()
        assert abs(m.dalr() - ENV_LAPSE_PER_KM) > 2.0, "DALR should not equal environmental lapse rate"

    def test_dalr_value_correct(self):
        """Prior error: dalr_wrong_value — DALR must be ~9.8, not 6.5 or 5."""
        m = _i()
        assert 9.5 < m.dalr() < 10.1, f"DALR should be ~9.8 °C/km, got {m.dalr()}"

    def test_ordering_dalr_gt_env_gt_malr(self):
        """KEY invariant: DALR > environmental > MALR."""
        m = _i()
        assert m.dalr() > ENV_LAPSE_PER_KM > MALR_PER_KM

class TestTemperatureAtAltitude:
    def test_dry_3km(self):
        m = _i()
        T = m.temperature_at_altitude(T_SURFACE, DALR_CONV, ALT_KM)
        assert abs(T - T_DRY_3KM_CONV) < 0.01, f"Expected {T_DRY_3KM_CONV}, got {T}"

    def test_moist_3km(self):
        m = _i()
        T = m.temperature_at_altitude(T_SURFACE, MALR_PER_KM, ALT_KM)
        assert abs(T - T_MOIST_3KM) < 0.01, f"Expected {T_MOIST_3KM}, got {T}"

    def test_env_3km(self):
        m = _i()
        T = m.temperature_at_altitude(T_SURFACE, ENV_LAPSE_PER_KM, ALT_KM)
        assert abs(T - T_ENV_3KM) < 0.01, f"Expected {T_ENV_3KM}, got {T}"

    def test_zero_altitude_returns_surface(self):
        m = _i()
        T = m.temperature_at_altitude(15.0, DALR_CONV, 0.0)
        assert abs(T - 15.0) < 1e-9

class TestStability:
    def test_stable_env(self):
        """env_lapse=5.0 < DALR=9.8 → stable."""
        m = _i()
        assert m.is_stable(STABLE_ENV) is True

    def test_unstable_env(self):
        """env_lapse=11.0 > DALR=9.8 → absolutely unstable."""
        m = _i()
        assert m.is_stable(UNSTABLE_ENV) is False

    def test_conditional_is_technically_stable_by_dalr(self):
        """env_lapse=7.0 < DALR=9.8 → stable by DALR criterion (conditionally unstable in full analysis)."""
        m = _i()
        assert m.is_stable(CONDITIONAL_ENV) is True

class TestLCL:
    def test_lcl_basic(self):
        m = _i()
        lcl = m.lifting_condensation_level(T_TEST_LCL, TD_TEST_LCL)
        assert abs(lcl - LCL_TEST) < 0.01, f"Expected {LCL_TEST} km, got {lcl}"

    def test_lcl_saturated(self):
        """If T == Td, LCL should be at the surface (0 km)."""
        m = _i()
        lcl = m.lifting_condensation_level(20.0, 20.0)
        assert abs(lcl) < 0.01
