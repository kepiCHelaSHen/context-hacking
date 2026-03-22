"""cat-astro-redshift — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_redshift_constants import *
IMPL = Path(__file__).parent.parent / "astro_redshift.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Tests that catch the three known LLM errors."""

    def test_v_cz_all_z_rejected_at_z1(self):
        """v=cz at z=1 gives v=c; SR Doppler gives 0.6c — must not match."""
        m = _i()
        v_sr = m.velocity_sr_doppler(Z1)
        v_cz_ratio = m.velocity_low_z(Z1) / C_KMS
        # The naive v=cz gives 1.0c; SR Doppler gives 0.6c — big difference
        assert abs(v_sr - V_SR_DOPPLER_1) < 1e-10
        assert abs(v_cz_ratio - 1.0) < 1e-10  # confirms v=cz gives c
        assert v_sr < v_cz_ratio  # SR answer must be less than naive answer

    def test_superluminal_not_physical_at_z3(self):
        """v=cz at z=3 gives 3c; SR Doppler must stay below c."""
        m = _i()
        v_sr = m.velocity_sr_doppler(Z3)
        assert v_sr < 1.0  # must be sub-luminal
        assert abs(v_sr - V_SR_DOPPLER_3) < 1e-6

    def test_low_z_flag_rejects_large_z(self):
        """is_low_z_valid must return False for z >= threshold."""
        m = _i()
        assert m.is_low_z_valid(Z1) is False
        assert m.is_low_z_valid(Z3) is False
        assert m.is_low_z_valid(0.5) is False
        assert m.is_low_z_valid(0.1) is False  # boundary: 0.1 is NOT < 0.1


class TestCorrectness:
    """Tests for correct formulas and edge cases."""

    def test_redshift_from_wavelengths(self):
        m = _i()
        z = m.redshift(LAMBDA_OBS_TEST, LAMBDA_EMIT_TEST)
        assert abs(z - Z_TEST) < 1e-6

    def test_redshift_zero(self):
        m = _i()
        z = m.redshift(500.0, 500.0)
        assert abs(z) < 1e-15

    def test_velocity_low_z_value(self):
        m = _i()
        v = m.velocity_low_z(Z_LOW)
        assert abs(v - V_LOW_Z_LOW) < 0.1  # km/s

    def test_sr_doppler_z0(self):
        """At z=0, velocity must be zero."""
        m = _i()
        assert abs(m.velocity_sr_doppler(0.0)) < 1e-15

    def test_sr_doppler_z1(self):
        m = _i()
        v = m.velocity_sr_doppler(Z1)
        assert abs(v - 0.6) < 1e-12  # exactly 3/5

    def test_sr_doppler_z3(self):
        m = _i()
        v = m.velocity_sr_doppler(Z3)
        assert abs(v - 15.0/17.0) < 1e-12  # exactly 15/17

    def test_low_z_valid_small(self):
        m = _i()
        assert m.is_low_z_valid(0.01) is True
        assert m.is_low_z_valid(0.05) is True
        assert m.is_low_z_valid(Z_LOW) is True

    def test_sr_doppler_always_below_c(self):
        """SR Doppler v/c must be < 1 for any finite z."""
        m = _i()
        for z in [0.5, 1.0, 2.0, 5.0, 10.0, 100.0, 1000.0]:
            assert m.velocity_sr_doppler(z) < 1.0

    def test_low_z_and_sr_agree_for_small_z(self):
        """For z << 1, cz and SR Doppler should approximately agree."""
        m = _i()
        z = 0.01
        v_cz = m.velocity_low_z(z) / C_KMS   # v/c ratio
        v_sr = m.velocity_sr_doppler(z)
        assert abs(v_cz - v_sr) < 0.001  # agree to < 0.1% for tiny z
