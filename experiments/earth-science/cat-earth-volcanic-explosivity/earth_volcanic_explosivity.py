"""
Volcanic Explosivity Index (VEI) — CHP Earth Science Sprint
VEI classification from ejecta volume, volume thresholds, unit conversion.
Logarithmic above VEI 2: each step = 10x ejecta volume.
All constants from frozen spec.
"""
import sys
import math
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_volcanic_explosivity_constants import (
    VEI_THRESHOLDS_M3, VEI_LOG_OFFSET, KM3_TO_M3,
)


def vei_from_volume_m3(volume):
    """Classify ejecta volume (m³) to VEI number (0-8).

    VEI 0: <1e4 m³, VEI 1: 1e4-1e6, VEI 2: 1e6-1e7
    For VEI n (n>=2): covers 10^(n+4) to 10^(n+5) m³.
    Logarithmic above VEI 2 — each step is 10x volume. NOT linear.
    """
    if volume <= 0:
        raise ValueError(f"Volume must be positive, got {volume}")
    if volume < VEI_THRESHOLDS_M3[1]:
        return 0
    if volume < VEI_THRESHOLDS_M3[2]:
        return 1
    # VEI 2-8: logarithmic. VEI n has lower bound 10^(n+4).
    log_vol = math.log10(volume)
    vei = int(log_vol) - VEI_LOG_OFFSET
    # Clamp to valid range
    if vei < 2:
        vei = 2
    if vei > 8:
        vei = 8
    return vei


def volume_threshold_m3(vei):
    """Return the lower bound volume (m³) for a given VEI level (0-8).

    For VEI n (n>=2): lower bound = 10^(n+4) m³.
    """
    if vei not in VEI_THRESHOLDS_M3:
        raise KeyError(f"VEI must be 0-8, got {vei!r}")
    return VEI_THRESHOLDS_M3[vei]


def km3_to_m3(km3):
    """Convert cubic kilometers to cubic meters.
    1 km³ = 10⁹ m³ (NOT 10⁶ — that is a common error)."""
    return km3 * KM3_TO_M3


def m3_to_km3(m3):
    """Convert cubic meters to cubic kilometers.
    Divides by 10⁹ (NOT 10⁶)."""
    return m3 / KM3_TO_M3


if __name__ == "__main__":
    print("=== Volcanic Explosivity Index (VEI) ===\n")

    # Print VEI thresholds
    print("VEI  Lower Bound (m³)   Lower Bound (km³)")
    print("-" * 50)
    for vei in range(9):
        thresh = volume_threshold_m3(vei)
        km3 = m3_to_km3(thresh)
        print(f"  {vei}   {thresh:>15.0e}   {km3:>12.3f}")

    # Test case: 50 km³
    vol_km3 = 50.0
    vol_m3 = km3_to_m3(vol_km3)
    result_vei = vei_from_volume_m3(vol_m3)
    print(f"\nTest: {vol_km3} km³ = {vol_m3:.0e} m³")
    print(f"  log10({vol_m3:.0e}) = {math.log10(vol_m3):.3f}")
    print(f"  VEI = {result_vei} (VEI 6 covers 10^10 to 10^11 m³)")

    # Notable eruptions
    print("\nNotable eruptions:")
    from earth_volcanic_explosivity_constants import NOTABLE_ERUPTIONS
    for name, info in NOTABLE_ERUPTIONS.items():
        vol = km3_to_m3(info["volume_km3"])
        calc_vei = vei_from_volume_m3(vol)
        print(f"  {name}: {info['volume_km3']} km³ -> VEI {calc_vei} (expected {info['vei']})")
