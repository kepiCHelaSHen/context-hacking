"""Glacial Rebound (Isostatic Adjustment) — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_glacial_rebound_constants import *


def depression_depth(h_ice, rho_ice=917, rho_mantle=3300):
    """Isostatic depression depth d = h_ice * rho_ice / rho_mantle. Returns metres."""
    return h_ice * rho_ice / rho_mantle


def rebound_remaining(d0, t, tau):
    """Remaining depression after time t: d(t) = d0 * exp(-t/tau). Returns metres."""
    return d0 * math.exp(-t / tau)


def uplift_rate(d0, t, tau):
    """Uplift rate |dd/dt| = (d0/tau) * exp(-t/tau). Returns m/yr."""
    return (d0 / tau) * math.exp(-t / tau)


def mantle_viscosity_order():
    """Return correct order of magnitude for mantle viscosity (log10 of Pa·s)."""
    return MANTLE_VISCOSITY_ORDER


if __name__ == "__main__":
    h = TEST_H_ICE
    d0 = depression_depth(h)
    print(f"Ice thickness: {h:.0f} m")
    print(f"Depression depth: {d0:.1f} m  (ratio = {DENSITY_RATIO:.4f})")
    print(f"\nRelaxation time tau = {TEST_TAU:.0f} yr")
    print(f"Uplift rate at t=0: {uplift_rate(d0, 0, TEST_TAU)*1000:.1f} mm/yr")
    print(f"\nAfter {TEST_T:.0f} years:")
    print(f"  Remaining depression: {rebound_remaining(d0, TEST_T, TEST_TAU):.1f} m")
    print(f"  Current uplift rate: {uplift_rate(d0, TEST_T, TEST_TAU)*1000:.1f} mm/yr")
    print(f"\nMantle viscosity: 10^{mantle_viscosity_order()} Pa·s")
