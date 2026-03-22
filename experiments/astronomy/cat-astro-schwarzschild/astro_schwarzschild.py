"""Schwarzschild Radius — CHP Astronomy Sprint."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_schwarzschild_constants import *


def schwarzschild_radius(M, G_val=G, c=C):
    """r_s = 2GM/c² — the factor of 2 is CRITICAL."""
    return 2 * G_val * M / c ** 2


def schwarzschild_solar_masses(M_solar, G_val=G, c=C):
    """Schwarzschild radius for mass given in solar masses."""
    return schwarzschild_radius(M_solar * M_SUN, G_val, c)


def is_black_hole(M, R, G_val=G, c=C):
    """True if object radius R < Schwarzschild radius for mass M."""
    return R < schwarzschild_radius(M, G_val, c)


if __name__ == "__main__":
    rs = schwarzschild_radius(M_SUN)
    print(f"Sun:    r_s = {rs:.1f} m = {rs/1000:.3f} km")
    rs_e = schwarzschild_radius(M_EARTH)
    print(f"Earth:  r_s = {rs_e:.4e} m = {rs_e*1000:.2f} mm")
    rs_sgr = schwarzschild_radius(M_SGR_A_STAR)
    print(f"Sgr A*: r_s = {rs_sgr:.3e} m = {rs_sgr/AU:.4f} AU")
    print(f"WRONG (no factor 2): {RS_SUN_WRONG:.1f} m = {RS_SUN_WRONG/1000:.3f} km")
