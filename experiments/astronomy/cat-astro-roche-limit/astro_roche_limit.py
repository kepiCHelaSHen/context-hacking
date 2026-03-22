"""Roche Limit — CHP Astronomy Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from astro_roche_limit_constants import *

def density_ratio_cuberoot(rho_M, rho_m):
    """(rho_M / rho_m)^(1/3). KEY: exponent is 1/3 (cube root), NOT linear."""
    return (rho_M / rho_m) ** (1/3)

def roche_limit_rigid(R_M, rho_M, rho_m):
    """Rigid-body Roche limit: d = R_M * (2 * rho_M / rho_m)^(1/3)."""
    return R_M * (2.0 * rho_M / rho_m) ** (1/3)

def roche_limit_fluid(R_M, rho_M, rho_m):
    """Fluid-body Roche limit: d = 2.456 * R_M * (rho_M / rho_m)^(1/3).
    This is Roche's original (1849) result for a fluid satellite."""
    return 2.456 * R_M * (rho_M / rho_m) ** (1/3)

def is_inside_roche(d_actual, d_roche):
    """True if object is INSIDE Roche limit (d_actual < d_roche → tidal disruption).
    Inside = UNSTABLE. Outside = stable."""
    return d_actual < d_roche

if __name__ == "__main__":
    print("=== Roche Limit Calculator ===\n")

    # Earth-Moon system (fluid model)
    d_rigid = roche_limit_rigid(R_EARTH, RHO_EARTH, RHO_MOON)
    d_fluid = roche_limit_fluid(R_EARTH, RHO_EARTH, RHO_MOON)
    ratio = density_ratio_cuberoot(RHO_EARTH, RHO_MOON)
    print(f"Earth-Moon system:")
    print(f"  Density ratio cube root: ({RHO_EARTH}/{RHO_MOON})^(1/3) = {ratio:.4f}")
    print(f"  Rigid Roche limit:  {d_rigid/1e3:.0f} km")
    print(f"  Fluid Roche limit:  {d_fluid/1e3:.0f} km")
    print(f"  Actual Moon distance: {D_MOON_ACTUAL/1e3:.0f} km")
    print(f"  Moon inside Roche?  {is_inside_roche(D_MOON_ACTUAL, d_fluid)} (should be False)\n")

    # Saturn rings
    d_saturn = roche_limit_fluid(R_SATURN, RHO_SATURN, RHO_ICE)
    print(f"Saturn (ice particles):")
    print(f"  Fluid Roche limit:  {d_saturn/1e3:.0f} km")
    print(f"  B ring outer edge:  {D_SATURN_RING_OUTER/1e3:.0f} km")
    print(f"  Rings inside Roche? {is_inside_roche(D_SATURN_RING_OUTER, d_saturn)} (should be True)")
