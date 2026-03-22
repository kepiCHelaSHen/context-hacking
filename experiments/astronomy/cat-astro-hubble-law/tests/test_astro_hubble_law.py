"""cat-astro-hubble-law — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_hubble_law_constants import *
IMPL = Path(__file__).parent.parent / "astro_hubble_law.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that catch the known LLM errors."""

    def test_h0_not_outdated_50(self):
        """H₀=50 gives d=140 Mpc for v=7000 — wrong by 40%."""
        m = _i()
        d_correct = m.hubble_distance(V_TEST, H0=H0_DEFAULT)
        d_wrong = m.hubble_distance(V_TEST, H0=50)
        assert abs(d_correct - D_TEST_MPC) < 0.01
        assert abs(d_wrong - D_TEST_MPC) > 30   # 140 vs 100 — far off

    def test_h0_not_outdated_100(self):
        """H₀=100 gives d=70 Mpc for v=7000 — wrong by 30%."""
        m = _i()
        d_wrong = m.hubble_distance(V_TEST, H0=100)
        assert abs(d_wrong - D_TEST_MPC) > 20   # 70 vs 100

    def test_hubble_time_correct_order(self):
        """t_H should be ~14 Gyr, not ~20 or ~10 from wrong H₀."""
        m = _i()
        t = m.hubble_time_gyr(H0_DEFAULT)
        assert 13.0 < t < 15.0, f"t_H = {t} Gyr — should be ~14"

    def test_hubble_time_not_naive_division(self):
        """1/70 = 0.0143 — must convert units, not just invert the number."""
        m = _i()
        t = m.hubble_time_gyr(H0_DEFAULT)
        assert t > 1.0, "t_H must be in Gyr, not raw 1/H₀"


class TestCorrectness:
    """Core correctness tests for Hubble's law functions."""

    def test_distance_basic(self):
        m = _i()
        assert abs(m.hubble_distance(V_TEST) - D_TEST_MPC) < 0.01

    def test_distance_second_vector(self):
        m = _i()
        assert abs(m.hubble_distance(V_TEST2) - D_TEST2_MPC) < 0.01

    def test_velocity_basic(self):
        m = _i()
        assert abs(m.hubble_velocity(D_TEST_MPC) - V_TEST) < 0.01

    def test_round_trip(self):
        """d = v/H₀ then v = H₀·d should recover original v."""
        m = _i()
        d = m.hubble_distance(V_TEST)
        v_back = m.hubble_velocity(d)
        assert abs(v_back - V_TEST) < 0.001

    def test_mpc_to_ly(self):
        m = _i()
        ly = m.mpc_to_ly(1.0)
        assert abs(ly - MPC_TO_LY) < 100   # within 100 ly of 3.26e6

    def test_mpc_to_ly_100(self):
        m = _i()
        ly = m.mpc_to_ly(D_TEST_MPC)
        assert abs(ly - D_TEST_LY) / D_TEST_LY < 0.001  # <0.1% error

    def test_hubble_time_planck(self):
        m = _i()
        t = m.hubble_time_gyr(H0_PLANCK)
        assert abs(t - HUBBLE_TIME_PLANCK_GYR) / HUBBLE_TIME_PLANCK_GYR < 0.001

    def test_hubble_time_shoes(self):
        m = _i()
        t = m.hubble_time_gyr(H0_SHOES)
        assert abs(t - HUBBLE_TIME_SHOES_GYR) / HUBBLE_TIME_SHOES_GYR < 0.001

    def test_hubble_tension_direction(self):
        """Planck (lower H₀) gives LONGER Hubble time than SH0ES (higher H₀)."""
        m = _i()
        t_planck = m.hubble_time_gyr(H0_PLANCK)
        t_shoes = m.hubble_time_gyr(H0_SHOES)
        assert t_planck > t_shoes
