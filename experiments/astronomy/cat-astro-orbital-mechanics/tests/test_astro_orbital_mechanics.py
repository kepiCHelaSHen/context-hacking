"""cat-astro-orbital-mechanics — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_orbital_mechanics_constants import *
IMPL = Path(__file__).parent.parent / "astro_orbital_mechanics.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    def test_two_burns_not_one(self):
        """Catches single_burn: total dv must include BOTH departure and arrival burns."""
        m = _i()
        dv1 = m.hohmann_dv1(MU_SUN, R_EARTH, R_MARS)
        dv2 = m.hohmann_dv2(MU_SUN, R_EARTH, R_MARS)
        total = m.hohmann_total_dv(MU_SUN, R_EARTH, R_MARS)
        # Total must be strictly greater than either individual burn
        assert total > abs(dv1) + 100, "total dv must include both burns, not just dv1"
        assert total > abs(dv2) + 100, "total dv must include both burns, not just dv2"
        assert abs(total - (abs(dv1) + abs(dv2))) < 1.0

    def test_transfer_time_is_half_period(self):
        """Catches transfer_time_wrong: transfer time = pi*sqrt(a^3/mu), NOT 2*pi*sqrt(a^3/mu)."""
        m = _i()
        a_t = m.transfer_semi_major(R_EARTH, R_MARS)
        t = m.transfer_time(MU_SUN, a_t)
        full_period = 2 * math.pi * math.sqrt(a_t**3 / MU_SUN)
        half_period = math.pi * math.sqrt(a_t**3 / MU_SUN)
        # Must be half period, not full
        assert abs(t - half_period) < 1.0, "transfer time must be half the orbit period"
        assert abs(t - full_period) > 1e6, "transfer time must NOT be the full orbit period"

    def test_vis_viva_not_circular(self):
        """Catches delta_v_wrong_formula: transfer orbit velocity != circular velocity."""
        m = _i()
        # dv1 should NOT be zero (it would be if v_t1 were computed as v_c1)
        dv1 = m.hohmann_dv1(MU_SUN, R_EARTH, R_MARS)
        assert abs(dv1) > 100, "dv1 must be nonzero — transfer orbit speed != circular speed"
        # dv2 should NOT be zero either
        dv2 = m.hohmann_dv2(MU_SUN, R_EARTH, R_MARS)
        assert abs(dv2) > 100, "dv2 must be nonzero — transfer orbit speed != circular speed"


class TestCorrectness:
    def test_transfer_semi_major(self):
        m = _i()
        a_t = m.transfer_semi_major(R_EARTH, R_MARS)
        assert abs(a_t - A_TRANSFER) < 1e6  # within 1000 km

    def test_dv1_earth_mars(self):
        m = _i()
        dv1 = m.hohmann_dv1(MU_SUN, R_EARTH, R_MARS)
        assert abs(dv1 - DV1) < 5.0  # within 5 m/s

    def test_dv2_earth_mars(self):
        m = _i()
        dv2 = m.hohmann_dv2(MU_SUN, R_EARTH, R_MARS)
        assert abs(dv2 - DV2) < 5.0

    def test_total_dv_earth_mars(self):
        m = _i()
        total = m.hohmann_total_dv(MU_SUN, R_EARTH, R_MARS)
        assert abs(total - TOTAL_DV) < 10.0

    def test_transfer_time_earth_mars(self):
        m = _i()
        a_t = m.transfer_semi_major(R_EARTH, R_MARS)
        t = m.transfer_time(MU_SUN, a_t)
        assert abs(t - T_TRANSFER) < 60.0  # within 1 minute

    def test_transfer_time_days(self):
        """Transfer time Earth-Mars ~ 259 days."""
        m = _i()
        a_t = m.transfer_semi_major(R_EARTH, R_MARS)
        t_days = m.transfer_time(MU_SUN, a_t) / 86400
        assert 255 < t_days < 265

    def test_dv1_positive(self):
        """Departure burn is prograde (speed up) for outward transfer."""
        m = _i()
        dv1 = m.hohmann_dv1(MU_SUN, R_EARTH, R_MARS)
        assert dv1 > 0

    def test_dv2_positive(self):
        """Arrival burn is prograde (speed up) for outward transfer."""
        m = _i()
        dv2 = m.hohmann_dv2(MU_SUN, R_EARTH, R_MARS)
        assert dv2 > 0

    def test_dv1_approx_3_kms(self):
        """dv1 ~ 2.94 km/s for Earth-Mars."""
        m = _i()
        dv1_kms = m.hohmann_dv1(MU_SUN, R_EARTH, R_MARS) / 1000
        assert 2.5 < dv1_kms < 3.5

    def test_dv2_approx_2p6_kms(self):
        """dv2 ~ 2.65 km/s for Earth-Mars."""
        m = _i()
        dv2_kms = m.hohmann_dv2(MU_SUN, R_EARTH, R_MARS) / 1000
        assert 2.2 < dv2_kms < 3.2

    def test_total_dv_approx_5p6_kms(self):
        """Total ~ 5.59 km/s for Earth-Mars."""
        m = _i()
        total_kms = m.hohmann_total_dv(MU_SUN, R_EARTH, R_MARS) / 1000
        assert 5.0 < total_kms < 6.5

    def test_symmetry_same_radius(self):
        """If r1 == r2, no transfer needed: all delta-v should be zero."""
        m = _i()
        dv1 = m.hohmann_dv1(MU_SUN, R_EARTH, R_EARTH)
        dv2 = m.hohmann_dv2(MU_SUN, R_EARTH, R_EARTH)
        total = m.hohmann_total_dv(MU_SUN, R_EARTH, R_EARTH)
        assert abs(dv1) < 0.01
        assert abs(dv2) < 0.01
        assert abs(total) < 0.01
