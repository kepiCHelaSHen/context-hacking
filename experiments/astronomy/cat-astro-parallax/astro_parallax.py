"""Stellar Parallax — CHP Astronomy Sprint. All constants from frozen spec."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_parallax_constants import PC_IN_LY, PC_IN_METERS, ARCSEC_PER_RADIAN


def parallax_distance_pc(p_arcsec):
    """Distance in parsecs from parallax semi-angle.
    d(pc) = 1 / p(arcsec)
    KEY: p is the SEMI-ANGLE (half the total annual shift), not the full shift."""
    if p_arcsec <= 0:
        raise ValueError("Parallax angle must be positive")
    return 1.0 / p_arcsec


def pc_to_ly(d_pc):
    """Convert parsecs to light-years.  1 pc = 3.26156 ly."""
    return d_pc * PC_IN_LY


def pc_to_m(d_pc):
    """Convert parsecs to metres.  1 pc = 3.08567758e16 m."""
    return d_pc * PC_IN_METERS


def arcsec_to_rad(arcsec):
    """Convert arcseconds to radians.
    1 arcsec = 1/206265 rad (NOT 1/3600 — that is degrees-to-arcsec)."""
    return arcsec / ARCSEC_PER_RADIAN


if __name__ == "__main__":
    from astro_parallax_constants import (
        P_PROXIMA_ARCSEC, D_PROXIMA_PC, D_PROXIMA_LY,
        P_TEST_ARCSEC, D_TEST_PC, D_TEST_LY,
        P_BARNARD_ARCSEC, P_SIRIUS_ARCSEC,
    )
    # Proxima Centauri
    d = parallax_distance_pc(P_PROXIMA_ARCSEC)
    print(f"Proxima Centauri: p={P_PROXIMA_ARCSEC}\" -> d={d:.4f} pc = {pc_to_ly(d):.3f} ly")

    # Test case: p = 0.1"
    d2 = parallax_distance_pc(P_TEST_ARCSEC)
    print(f"Test (p=0.1\"): d={d2:.1f} pc = {pc_to_ly(d2):.2f} ly = {pc_to_m(d2):.4e} m")

    # Barnard's Star
    d3 = parallax_distance_pc(P_BARNARD_ARCSEC)
    print(f"Barnard's Star: p={P_BARNARD_ARCSEC}\" -> d={d3:.4f} pc = {pc_to_ly(d3):.3f} ly")

    # Sirius
    d4 = parallax_distance_pc(P_SIRIUS_ARCSEC)
    print(f"Sirius: p={P_SIRIUS_ARCSEC}\" -> d={d4:.4f} pc = {pc_to_ly(d4):.3f} ly")

    # Conversion check
    print(f"\narcsec_to_rad(1.0) = {arcsec_to_rad(1.0):.6e} rad")
    print(f"Expected: 1/206265 = {1/206265:.6e} rad")
