"""Seismic Waves — CHP Earth Science Sprint."""
import sys, math
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_seismic_waves_constants import *


def p_wave_velocity(K, G, rho):
    """P-wave velocity Vp = sqrt((K + 4G/3) / rho). Returns m/s."""
    return math.sqrt((K + 4 * G / 3) / rho)


def s_wave_velocity(G, rho):
    """S-wave velocity Vs = sqrt(G / rho). Returns m/s. Zero in fluids (G=0)."""
    if G <= 0:
        return 0.0
    return math.sqrt(G / rho)


def can_propagate_s(G):
    """Return True if S-waves can propagate (requires G > 0). Fluids have G=0."""
    return G > 0


def vp_vs_ratio(K, G):
    """Return Vp/Vs ratio = sqrt((K + 4G/3) / G). Undefined if G=0."""
    if G <= 0:
        return float('inf')
    return math.sqrt((K + 4 * G / 3) / G)


if __name__ == "__main__":
    print("=== Seismic Wave Velocities ===\n")
    print("Upper Mantle:")
    vp = p_wave_velocity(TEST_K, TEST_G, TEST_RHO)
    vs = s_wave_velocity(TEST_G, TEST_RHO)
    ratio = vp_vs_ratio(TEST_K, TEST_G)
    print(f"  Vp  = {vp:.1f} m/s  ({vp/1000:.2f} km/s)")
    print(f"  Vs  = {vs:.1f} m/s  ({vs/1000:.2f} km/s)")
    print(f"  Vp/Vs = {ratio:.3f}")
    print(f"  S-wave propagates? {can_propagate_s(TEST_G)}")

    print("\nOuter Core (liquid):")
    vp_oc = p_wave_velocity(K_OUTER_CORE, G_LIQUID, RHO_OUTER_CORE)
    vs_oc = s_wave_velocity(G_LIQUID, RHO_OUTER_CORE)
    print(f"  Vp  = {vp_oc:.1f} m/s  ({vp_oc/1000:.2f} km/s)")
    print(f"  Vs  = {vs_oc:.1f} m/s  (ZERO — no S-waves in liquid!)")
    print(f"  S-wave propagates? {can_propagate_s(G_LIQUID)}")

    print(f"\nS-wave shadow zone: {SHADOW_ZONE_MIN_DEG}°–{SHADOW_ZONE_MAX_DEG}° from epicenter")
    print("  This proves the outer core is liquid!")
