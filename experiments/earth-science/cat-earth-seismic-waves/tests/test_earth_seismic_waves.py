"""cat-earth-seismic-waves — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from earth_seismic_waves_constants import *
IMPL = Path(__file__).parent.parent / "earth_seismic_waves.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three known LLM errors."""

    def test_s_wave_zero_in_liquid(self):
        """PRIOR_ERROR: s_through_liquid — S-waves CANNOT travel through liquid (G=0)."""
        m = _i()
        vs = m.s_wave_velocity(0.0, RHO_OUTER_CORE)
        assert vs == 0.0, f"S-wave in liquid must be 0, got {vs}"

    def test_s_wave_cannot_propagate_in_liquid(self):
        """PRIOR_ERROR: s_through_liquid — can_propagate_s must return False for G=0."""
        m = _i()
        assert m.can_propagate_s(0.0) is False, "S-waves must NOT propagate in liquid (G=0)"

    def test_vp_faster_than_vs(self):
        """PRIOR_ERROR: vp_vs_equal — P-wave is always faster than S-wave."""
        m = _i()
        vp = m.p_wave_velocity(TEST_K, TEST_G, TEST_RHO)
        vs = m.s_wave_velocity(TEST_G, TEST_RHO)
        assert vp > vs, f"Vp ({vp}) must exceed Vs ({vs})"

    def test_vp_vs_ratio_gt_one(self):
        """PRIOR_ERROR: vp_vs_equal — Vp/Vs ratio must be > 1."""
        m = _i()
        ratio = m.vp_vs_ratio(TEST_K, TEST_G)
        assert ratio > 1.0, f"Vp/Vs ratio must be > 1, got {ratio}"

    def test_shadow_zone_range(self):
        """PRIOR_ERROR: shadow_zone_wrong — S-wave shadow zone is 104-140 degrees."""
        assert SHADOW_ZONE_MIN_DEG == 104.0, f"Shadow zone min should be 104, got {SHADOW_ZONE_MIN_DEG}"
        assert SHADOW_ZONE_MAX_DEG == 140.0, f"Shadow zone max should be 140, got {SHADOW_ZONE_MAX_DEG}"


class TestCorrectness:
    """Verify computed values against frozen constants."""

    def test_p_wave_upper_mantle(self):
        m = _i()
        vp = m.p_wave_velocity(K_UPPER_MANTLE, G_UPPER_MANTLE, RHO_UPPER_MANTLE)
        assert abs(vp - VP_UPPER_MANTLE) < 0.01, f"Vp mismatch: {vp} vs {VP_UPPER_MANTLE}"

    def test_s_wave_upper_mantle(self):
        m = _i()
        vs = m.s_wave_velocity(G_UPPER_MANTLE, RHO_UPPER_MANTLE)
        assert abs(vs - VS_UPPER_MANTLE) < 0.01, f"Vs mismatch: {vs} vs {VS_UPPER_MANTLE}"

    def test_p_wave_outer_core(self):
        m = _i()
        vp = m.p_wave_velocity(K_OUTER_CORE, G_LIQUID, RHO_OUTER_CORE)
        assert abs(vp - VP_OUTER_CORE) < 0.01, f"Vp outer core mismatch: {vp} vs {VP_OUTER_CORE}"

    def test_s_wave_outer_core_zero(self):
        m = _i()
        vs = m.s_wave_velocity(G_LIQUID, RHO_OUTER_CORE)
        assert vs == 0.0, f"Vs in outer core must be 0, got {vs}"

    def test_vp_vs_ratio_upper_mantle(self):
        m = _i()
        ratio = m.vp_vs_ratio(K_UPPER_MANTLE, G_UPPER_MANTLE)
        assert abs(ratio - VP_VS_RATIO_UPPER_MANTLE) < 1e-10

    def test_vp_vs_ratio_liquid_infinite(self):
        """Vp/Vs in liquid should be infinite (G=0)."""
        m = _i()
        ratio = m.vp_vs_ratio(K_OUTER_CORE, G_LIQUID)
        assert ratio == float('inf'), f"Vp/Vs in liquid should be inf, got {ratio}"

    def test_can_propagate_s_solid(self):
        m = _i()
        assert m.can_propagate_s(G_UPPER_MANTLE) is True

    def test_can_propagate_s_liquid(self):
        m = _i()
        assert m.can_propagate_s(G_LIQUID) is False

    def test_vp_range_realistic(self):
        """Upper mantle Vp should be roughly 8-9 km/s."""
        m = _i()
        vp = m.p_wave_velocity(K_UPPER_MANTLE, G_UPPER_MANTLE, RHO_UPPER_MANTLE)
        assert 8000 < vp < 9000, f"Vp = {vp} m/s outside realistic range"

    def test_vs_range_realistic(self):
        """Upper mantle Vs should be roughly 4.5-5.5 km/s."""
        m = _i()
        vs = m.s_wave_velocity(G_UPPER_MANTLE, RHO_UPPER_MANTLE)
        assert 4500 < vs < 5500, f"Vs = {vs} m/s outside realistic range"

    def test_poisson_ratio_approx(self):
        """For Poisson solid (nu=0.25), Vp/Vs ~ sqrt(3) ~ 1.732."""
        assert abs(VP_VS_RATIO_POISSON - math.sqrt(3)) < 1e-12
