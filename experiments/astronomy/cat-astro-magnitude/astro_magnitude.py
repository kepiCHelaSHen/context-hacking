"""Stellar Magnitude — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_magnitude_constants import *


def distance_modulus(d_pc):
    """m - M = 5*log10(d) - 5, where d in parsecs.
    The -5 comes from the 10 pc reference distance: 5*log10(d/10) = 5*log10(d) - 5.
    NOT just 5*log10(d) — that omits the 10 pc reference!
    """
    return 5 * math.log10(d_pc) - 5


def apparent_from_absolute(M, d_pc):
    """m = M + distance_modulus. Apparent magnitude from absolute magnitude and distance."""
    return M + distance_modulus(d_pc)


def absolute_from_apparent(m, d_pc):
    """M = m - distance_modulus. Absolute magnitude from apparent magnitude and distance."""
    return m - distance_modulus(d_pc)


def flux_ratio(m1, m2):
    """F1/F2 = 10^((m2 - m1) / 2.5).
    Pogson's ratio: brighter object has LOWER m, so if m1 < m2, F1 > F2.
    5 magnitudes = exactly 100x flux ratio.
    """
    return 10 ** ((m2 - m1) / 2.5)


if __name__ == "__main__":
    # Test star: d=100 pc, M=0
    dm = distance_modulus(D_TEST)
    m = apparent_from_absolute(M_TEST, D_TEST)
    print(f"Test star (d={D_TEST}pc, M={M_TEST}): dm={dm:.1f}, m={m:.1f} (should be 5.0)")
    print(f"WRONG formula (no -5) would give: {DM_TEST_WRONG:.1f} (5 mag too faint!)")

    # Sun
    dm_sun = distance_modulus(AU_IN_PC)
    print(f"\nSun: dm={dm_sun:.2f} (actual: {DM_SUN:.2f})")
    M_sun_calc = absolute_from_apparent(M_SUN_APP, AU_IN_PC)
    print(f"Sun M from m={M_SUN_APP}: {M_sun_calc:.2f} (actual: {M_SUN_ABS})")

    # Flux ratio
    fr = flux_ratio(0, 5)
    print(f"\nFlux ratio 5 mag: {fr:.0f}x (should be 100)")
    fr1 = flux_ratio(0, 1)
    print(f"Flux ratio 1 mag: {fr1:.4f}x (should be ~2.512)")
