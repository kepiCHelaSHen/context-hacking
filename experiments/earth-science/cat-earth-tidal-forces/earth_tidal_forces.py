"""Tidal Forces (Lunar & Solar Tidal Bulge) — CHP Earth Science Sprint. All constants from frozen spec."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "frozen"))
from earth_tidal_forces_constants import (
    M_MOON, D_MOON, M_SUN, D_SUN,
    SUN_MOON_RATIO, SPRING_FACTOR, NEAP_FACTOR,
)


def tidal_force_ratio(M, d):
    """Tidal force factor ∝ M / d³ (relative, not absolute). Returns M/d³."""
    return M / d**3


def sun_moon_ratio():
    """Ratio of Sun's tidal force to Moon's tidal force. Returns ~0.46."""
    return tidal_force_ratio(M_SUN, D_SUN) / tidal_force_ratio(M_MOON, D_MOON)


def spring_tide_factor():
    """Spring tide: Moon + Sun aligned. Returns 1 + sun_moon_ratio ≈ 1.46."""
    return 1.0 + sun_moon_ratio()


def neap_tide_factor():
    """Neap tide: Moon + Sun perpendicular. Returns 1 - sun_moon_ratio ≈ 0.54."""
    return 1.0 - sun_moon_ratio()


if __name__ == "__main__":
    print(f"Moon tidal factor (M/d³): {tidal_force_ratio(M_MOON, D_MOON):.6e}")
    print(f"Sun  tidal factor (M/d³): {tidal_force_ratio(M_SUN, D_SUN):.6e}")
    print(f"Sun/Moon tidal ratio:     {sun_moon_ratio():.4f}")
    print(f"Spring tide factor:       {spring_tide_factor():.4f}")
    print(f"Neap tide factor:         {neap_tide_factor():.4f}")
