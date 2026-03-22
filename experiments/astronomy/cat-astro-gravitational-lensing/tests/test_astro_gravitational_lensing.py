"""cat-astro-gravitational-lensing — Sigma Gate Tests"""
import sys, math
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).parent.parent / "frozen"))
from astro_gravitational_lensing_constants import *
IMPL = Path(__file__).parent.parent / "astro_gravitational_lensing.py"
def _i():
    if not IMPL.exists(): pytest.skip("not yet written")
    import importlib.util; s = importlib.util.spec_from_file_location("m", IMPL); m = importlib.util.module_from_spec(s); s.loader.exec_module(m); return m


class TestPriorErrors:
    """Catch the three documented LLM failure modes."""

    def test_deflection_is_gr_not_newtonian(self):
        """CRITICAL: deflection must be 4GM/(c^2*b), NOT 2GM/(c^2*b) — factor of 2!"""
        m = _i()
        alpha = m.deflection_angle(M_SUN, R_SUN)
        alpha_arcsec = m.rad_to_arcsec(alpha)
        # GR predicts ~1.751 arcsec at solar limb; Newtonian gives ~0.876
        assert abs(alpha_arcsec - DEFLECTION_SOLAR_LIMB_ARCSEC) / DEFLECTION_SOLAR_LIMB_ARCSEC < 1e-4, \
            f"Got {alpha_arcsec:.4f} arcsec, expected {DEFLECTION_SOLAR_LIMB_ARCSEC:.4f} (Newtonian instead of GR?)"
        assert alpha_arcsec > DEFLECTION_SOLAR_LIMB_NEWTONIAN_ARCSEC * 1.5, \
            "Result is too close to Newtonian 2GM/(c^2*b) — should be 4GM/(c^2*b)!"

    def test_einstein_ring_exists(self):
        """Must compute an Einstein ring angle, not just point deflection."""
        m = _i()
        theta = m.einstein_radius_angle(M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
        # theta_E ~ 4.89e-9 rad ~ 1.009 milliarcsec for stellar-mass lens
        assert theta > 0, "Einstein ring angle must be positive"
        theta_mas = m.rad_to_arcsec(theta) * 1000
        assert abs(theta_mas - THETA_E_TEST_MAS) / THETA_E_TEST_MAS < 1e-3, \
            f"Got {theta_mas:.4f} mas, expected {THETA_E_TEST_MAS:.4f} mas"

    def test_distance_subtraction_trap(self):
        """D_ls is an independent parameter, NOT forced to D_s - D_l.
        For cosmological distances, D_ls != D_s - D_l."""
        m = _i()
        # Use D_ls that differs from D_s - D_l to verify function uses D_ls directly
        D_l = 4 * KPC
        D_s = 10 * KPC
        D_ls_actual = 5 * KPC  # NOT equal to D_s - D_l = 6 kpc
        theta = m.einstein_radius_angle(M_SUN, D_l, D_s, D_ls_actual)
        # Expected: sqrt(4GM/c^2 * 5kpc / (4kpc * 10kpc))
        expected = math.sqrt(4 * G * M_SUN / C_SQUARED * D_ls_actual / (D_l * D_s))
        assert abs(theta - expected) / expected < 1e-6, \
            f"Got {theta}, expected {expected} — is function overriding D_ls with D_s - D_l?"


class TestCorrectness:
    """Verify numerical accuracy against precomputed constants."""

    def test_einstein_ring_solar_mass(self):
        """theta_E for M_sun at D_l=4kpc, D_s=8kpc, D_ls=4kpc."""
        m = _i()
        theta = m.einstein_radius_angle(M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
        assert abs(theta - THETA_E_TEST) / THETA_E_TEST < 1e-4

    def test_einstein_ring_milliarcsec_scale(self):
        """Stellar-mass lensing gives ~1 milliarcsecond Einstein ring."""
        m = _i()
        theta = m.einstein_radius_angle(M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
        theta_mas = m.rad_to_arcsec(theta) * 1000
        assert 0.5 < theta_mas < 2.0, f"theta_E = {theta_mas:.4f} mas — expected ~1 mas for stellar-mass lens"

    def test_solar_limb_deflection(self):
        """Deflection at solar limb: ~1.75 arcsec (Eddington 1919)."""
        m = _i()
        alpha = m.deflection_angle(M_SUN, R_SUN)
        alpha_arcsec = m.rad_to_arcsec(alpha)
        assert abs(alpha_arcsec - 1.751) < 0.01, f"Got {alpha_arcsec:.4f}, expected ~1.751 arcsec"

    def test_newtonian_is_half_gr(self):
        """Newtonian deflection must be exactly half of GR deflection."""
        m = _i()
        alpha_gr = m.deflection_angle(M_SUN, R_SUN)
        alpha_newt = m.newtonian_deflection(M_SUN, R_SUN)
        ratio = alpha_gr / alpha_newt
        assert abs(ratio - 2.0) < 1e-10, f"GR/Newtonian ratio = {ratio}, expected exactly 2.0"

    def test_rad_to_arcsec_conversion(self):
        """1 radian = 206265 arcseconds."""
        m = _i()
        assert abs(m.rad_to_arcsec(1.0) - 206265) < 1

    def test_scaling_with_mass(self):
        """theta_E scales as sqrt(M) — doubling mass increases angle by sqrt(2)."""
        m = _i()
        theta1 = m.einstein_radius_angle(M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
        theta2 = m.einstein_radius_angle(2 * M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
        assert abs(theta2 / theta1 - math.sqrt(2)) < 1e-10

    def test_deflection_scaling_with_impact(self):
        """Deflection alpha = 4GM/(c^2*b) scales as 1/b."""
        m = _i()
        alpha1 = m.deflection_angle(M_SUN, R_SUN)
        alpha2 = m.deflection_angle(M_SUN, 2 * R_SUN)
        assert abs(alpha1 / alpha2 - 2.0) < 1e-10
