"""cat-earth-plate-velocity — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_plate_velocity_constants import *
IMPL = Path(__file__).parent.parent / "earth_plate_velocity.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m

class TestPriorErrors:
    def test_units_not_m_per_yr(self):
        """LLM trap: 600 km / 10 Ma = 60 mm/yr, NOT 60 m/yr."""
        m = _i(); v = m.plate_velocity_mmyr(TEST_DIST_KM, TEST_AGE_MA)
        assert abs(v - 60.0) < 0.01, "Must be 60 mm/yr"
        v_cm = m.plate_velocity_cmyr(TEST_DIST_KM, TEST_AGE_MA)
        assert abs(v_cm - 6.0) < 0.01, "Must be 6.0 cm/yr"
        # If someone returns m/yr, value would be 60000 — way off
        assert v < 200, "Velocity > 200 mm/yr is unrealistic for plates"

    def test_great_circle_not_straight_line(self):
        """LLM trap: must use haversine, not Euclidean distance on flat map."""
        m = _i()
        gc = m.great_circle_distance(LAT1_HON, LON1_HON, LAT2_MID, LON2_MID)
        assert abs(gc - GC_DIST_HON_MID) < 1.0, f"GC dist should be ~{GC_DIST_HON_MID:.0f} km"
        # Naive Euclidean in degrees -> km would give very wrong answer
        naive_dlat = (LAT2_MID - LAT1_HON) * 111.0
        naive_dlon = (LON2_MID - LON1_HON) * 111.0
        naive_dist = math.sqrt(naive_dlat**2 + naive_dlon**2)
        assert abs(gc - naive_dist) > 50, "Should differ from naive Euclidean significantly"

    def test_euler_pole_velocity_varies(self):
        """LLM trap: velocity depends on angular distance from Euler pole."""
        m = _i()
        v30 = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, 30.0)
        v60 = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, 60.0)
        v90 = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, 90.0)
        assert v60 > v30, "Velocity at 60° must exceed velocity at 30°"
        assert v90 > v60, "Velocity at 90° must exceed velocity at 60°"
        # At pole (0°), velocity should be zero
        v0 = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, 0.0)
        assert abs(v0) < 0.01

class TestCorrectness:
    def test_hawaiian_chain_velocity_mmyr(self):
        m = _i(); v = m.plate_velocity_mmyr(HAWAII_DIST_KM, HAWAII_AGE_MA)
        assert abs(v - HAWAII_V_MMYR) < 0.1

    def test_hawaiian_chain_velocity_cmyr(self):
        m = _i(); v = m.plate_velocity_cmyr(HAWAII_DIST_KM, HAWAII_AGE_MA)
        assert abs(v - HAWAII_V_CMYR) < 0.01

    def test_simple_case_600km_10Ma(self):
        m = _i(); v = m.plate_velocity_mmyr(TEST_DIST_KM, TEST_AGE_MA)
        assert abs(v - TEST_V_MMYR) < 0.01

    def test_gc_distance_honolulu_midway(self):
        m = _i(); d = m.great_circle_distance(LAT1_HON, LON1_HON, LAT2_MID, LON2_MID)
        assert abs(d - GC_DIST_HON_MID) < 1.0

    def test_gc_zero_distance(self):
        m = _i(); d = m.great_circle_distance(0, 0, 0, 0)
        assert abs(d) < 0.001

    def test_gc_antipodal(self):
        """Half circumference: 0,0 to 0,180 should be pi*R."""
        m = _i(); d = m.great_circle_distance(0, 0, 0, 180)
        assert abs(d - math.pi * R_EARTH) < 1.0

    def test_euler_velocity_at_test_theta(self):
        m = _i(); v = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, TEST_THETA_DEG)
        assert abs(v - EULER_V_TEST) < 0.5

    def test_euler_velocity_at_equator_max(self):
        """At 90° from pole, velocity is maximum: v = ω·R."""
        m = _i(); v = m.euler_velocity(OMEGA_PACIFIC_DEG_MYR, R_EARTH, 90.0)
        v_max = math.radians(OMEGA_PACIFIC_DEG_MYR) * R_EARTH
        assert abs(v - v_max) < 0.1

    def test_plate_velocity_rejects_zero_age(self):
        m = _i()
        with pytest.raises(ValueError):
            m.plate_velocity_mmyr(100, 0)
