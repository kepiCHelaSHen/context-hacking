"""Einstein Ring — Gravitational Lensing Radius — CHP Astronomy Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_gravitational_lensing_constants import *


def einstein_radius_angle(M, D_l, D_s, D_ls, G_val=G, c=C):
    """theta_E = sqrt(4GM/c^2 * D_ls / (D_l * D_s)) — Einstein ring angular radius in radians.

    For cosmological distances: D_ls != D_s - D_l (angular diameter distances don't subtract).
    For nearby (non-cosmological) lensing: D_ls ~ D_s - D_l is acceptable.
    """
    return math.sqrt(4 * G_val * M / c ** 2 * D_ls / (D_l * D_s))


def deflection_angle(M, b, G_val=G, c=C):
    """alpha = 4GM / (c^2 * b) — GR deflection angle by a point mass.

    This is Einstein's result: 2x the Newtonian prediction.
    Confirmed by Eddington's 1919 solar eclipse expedition (~1.75 arcsec at solar limb).
    """
    return 4 * G_val * M / (c ** 2 * b)


def rad_to_arcsec(rad):
    """Convert radians to arcseconds: 1 rad = 206265 arcsec."""
    return rad * RAD_TO_ARCSEC


def newtonian_deflection(M, b, G_val=G, c=C):
    """alpha_Newton = 2GM / (c^2 * b) — the WRONG Newtonian prediction (half of GR).

    This is the classical calculation that treats light as a particle.
    Einstein showed the correct value is TWICE this. The 1919 eclipse confirmed GR.
    """
    return 2 * G_val * M / (c ** 2 * b)


if __name__ == "__main__":
    # Einstein ring for stellar-mass lens
    theta = einstein_radius_angle(M_SUN, D_L_TEST, D_S_TEST, D_LS_TEST)
    print(f"Einstein ring (M_sun, D_l=4kpc, D_s=8kpc):")
    print(f"  theta_E = {theta:.4e} rad = {rad_to_arcsec(theta)*1000:.4f} milliarcsec")

    # Solar limb deflection
    alpha = deflection_angle(M_SUN, R_SUN)
    print(f"\nSolar limb deflection (GR):   {rad_to_arcsec(alpha):.4f} arcsec")
    alpha_n = newtonian_deflection(M_SUN, R_SUN)
    print(f"Solar limb deflection (Newt): {rad_to_arcsec(alpha_n):.4f} arcsec (WRONG)")
    print(f"GR / Newtonian = {alpha/alpha_n:.1f}x (Einstein's key prediction)")
