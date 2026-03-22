"""cat-earth-continental-drift — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_continental_drift_constants import *
IMPL = Path(__file__).parent.parent / "earth_continental_drift.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Each test catches one documented LLM error pattern."""

    def test_total_average_is_wrong(self):
        """PRIOR_ERROR: total_average — total dist/time gives wrong velocity across a bend."""
        m = _i()
        v_wrong = m.total_average_velocity(ISLAND_C_DIST_KM, ISLAND_C_AGE_MA)
        v_ab = m.segment_velocity(SEGMENT_AB_DIST_KM, SEGMENT_AB_AGE_DIFF_MA)
        v_bc = m.segment_velocity(SEGMENT_BC_DIST_KM, SEGMENT_BC_AGE_DIFF_MA)
        # The wrong total average must NOT equal either correct segment velocity
        assert abs(v_wrong - v_ab) > 1.0, "total avg should differ from segment AB"
        assert abs(v_wrong - v_bc) > 1.0, "total avg should differ from segment BC"

    def test_constant_velocity_rejected(self):
        """PRIOR_ERROR: constant_velocity — segments have different speeds."""
        m = _i()
        v_ab = m.segment_velocity(SEGMENT_AB_DIST_KM, SEGMENT_AB_AGE_DIFF_MA)
        v_bc = m.segment_velocity(SEGMENT_BC_DIST_KM, SEGMENT_BC_AGE_DIFF_MA)
        assert m.velocities_differ(v_ab, v_bc), "plate velocity changed at the bend"

    def test_age_direction_correct(self):
        """PRIOR_ERROR: wrong_age_direction — ages increase away from hotspot."""
        m = _i()
        assert m.age_increases_away_from_hotspot() is True


class TestCorrectness:
    """Numerical correctness against frozen constants."""

    def test_segment_ab_velocity(self):
        m = _i()
        v = m.segment_velocity(SEGMENT_AB_DIST_KM, SEGMENT_AB_AGE_DIFF_MA)
        assert abs(v - SEGMENT_AB_VELOCITY_MMYR) < 0.01

    def test_segment_bc_velocity(self):
        m = _i()
        v = m.segment_velocity(SEGMENT_BC_DIST_KM, SEGMENT_BC_AGE_DIFF_MA)
        assert abs(v - SEGMENT_BC_VELOCITY_MMYR) < 0.01

    def test_wrong_total_average(self):
        m = _i()
        v = m.total_average_velocity(ISLAND_C_DIST_KM, ISLAND_C_AGE_MA)
        assert abs(v - WRONG_TOTAL_AVG_MMYR) < 0.01

    def test_velocities_differ_true(self):
        m = _i()
        assert m.velocities_differ(SEGMENT_AB_VELOCITY_MMYR, SEGMENT_BC_VELOCITY_MMYR) is True

    def test_velocities_differ_false_within_threshold(self):
        m = _i()
        assert m.velocities_differ(50.0, 52.0) is False

    def test_segment_velocity_rejects_zero_age(self):
        m = _i()
        with pytest.raises(ValueError):
            m.segment_velocity(100, 0)

    def test_total_average_rejects_zero_age(self):
        m = _i()
        with pytest.raises(ValueError):
            m.total_average_velocity(100, 0)
